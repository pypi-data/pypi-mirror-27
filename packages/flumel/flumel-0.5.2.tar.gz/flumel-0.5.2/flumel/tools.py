"""
Boite à outils
"""
import imaplib
import smtplib
from email import message_from_bytes
from email.header import decode_header, make_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

import html2text
import pkg_resources
from premailer import transform

from . import settings


def format_template(name: str, **kwargs) -> str:
    """
    Formate le contenu du gabarit `name` avec kwargs + un extrait des settings.
    Utilise `string.Template`, les chaînes `$foo` seront remplacées par la valeur de `foo`.
    On essaye d'utiliser le gabarit personnalisé dans le répertoire `templates/`
    Si introuvable, replis sur celui du package.
    Note: pkg_resources.resource_string est utilisé pour récupérer le path de flumel
    """
    kwargs.update({
        'INSTANCE_NAME': settings.INSTANCE_NAME,
        'INSTANCE_URL': settings.INSTANCE_URL,
        'INSTANCE_BASELINE': settings.INSTANCE_BASELINE,
        'BOT_EMAIL': settings.BOT_EMAIL,
        'SUBSCRIBE_KEYWORD': settings.SUBSCRIBE_KEYWORD,
        'UNSUBSCRIBE_KEYWORD': settings.UNSUBSCRIBE_KEYWORD
    })
    path = '/'.join(['templates', name])
    try:
        with open(path, 'r') as fp_template:
            html = fp_template.read()
    except FileNotFoundError:
        html = pkg_resources.resource_string(__name__, path).decode('utf-8')
    return Template(html).safe_substitute(**kwargs)


def decode_email_header(value) -> str:
    """
    Les headers des emails sont encodés comme des sagouins
    https://docs.python.org/3/library/email.header.html#email.header.decode_header
    @see https://stackoverflow.com/a/12071098

    """
    return str(make_header(decode_header(value))).strip()


class IMAP:
    """
    Interface simplifiée pour imaplib.IMAP4
    La connexion est en SSL si BOT_IMAP_PORT == 993, sinon c'est en starttls
    """

    server = None

    def __init__(self):
        """
        Connexion + login
        """
        if settings.BOT_IMAP_PORT == 993:
            self.server = imaplib.IMAP4_SSL(settings.BOT_IMAP_HOST)
        else:
            self.server = imaplib.IMAP4(settings.BOT_IMAP_HOST)
            self.server.starttls()
        self.server.login(settings.BOT_IMAP_LOGIN, settings.BOT_IMAP_PASSWORD)

    @property
    def inbox(self) -> list:
        """
        Récupération de la liste des messages dans l’inbox, retourne un tableau iterable
        """
        self.server.select()  # ouverture inbox
        _, listing = self.server.search(None, 'ALL')  # (résultat, list)
        return listing[0].split()

    def get(self, number: int):
        """
        Retourne le message `number`
        """
        _, msg = self.server.fetch(number, '(RFC822)')  # (résultat, message)
        return message_from_bytes(msg[0][1])

    def delete(self, number: int):
        """
        Flag le message `number` à supprimer
        """
        return self.server.store(number, '+FLAGS', '\\Deleted')

    def purge(self):
        """
        Vide l’inbox après avoir marqué l’ensemble des messages à supprimer
        """
        for number in self.inbox:
            self.delete(number)
        return self.server.expunge()

    def close(self) -> None:
        """
        Efface les messages avec flag et clôture la connexion
        """
        self.server.select()  # command EXPUNGE only allowed in states SELECTED
        self.server.expunge()
        self.server.close()
        self.server.logout()


class SMTP:
    """
    Interface simplifiée pour smtplib.SMTP
    La connexion est en SSL si BOT_SMTP_PORT == 465, sinon c'est en starttls
    """

    server = None

    def __init__(self):
        """
        Connexion & login
        """
        if settings.BOT_SMTP_PORT == 465:
            self.server = smtplib.SMTP_SSL(settings.BOT_SMTP_HOST,
                                           settings.BOT_SMTP_PORT)
        else:
            self.server = smtplib.SMTP(settings.BOT_SMTP_HOST,
                                       settings.BOT_SMTP_PORT)
            if settings.BOT_SMTP_PORT == 587:
                self.server.starttls()
        try:
            self.server.login(settings.BOT_SMTP_LOGIN,
                              settings.BOT_SMTP_PASSWORD)
        except smtplib.SMTPNotSupportedError:
            pass

    def send(self,
             recipient: str,
             subject: str,
             html: str,
             preheader: str = None,
             **kwargs) -> None:
        """
        Envoi d'un email multipart intégré dans des gabarits
        Le corps du message est envoyé en html et sa conversion en texte brut par html2text
        Les kwargs permettent de personnaliser les entêtes du mail X-Flumel
        par ex. Title="Test" -> X-Flumel-Title = "Test"
        """

        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = settings.BOT_EMAIL
        message['To'] = recipient
        if kwargs:
            for key, value in kwargs.items():
                message['X-Flumel-' + key] = value

        text = html2text.html2text(html)
        full_txt = format_template('email.txt', **{
            'content': text,
        })
        message.attach(MIMEText(full_txt, 'plain'))

        full_html = format_template('email.html', **{
            'content': html,
            'preheader': preheader,
            'title': subject
        })
        inline_html = transform(full_html)
        message.attach(MIMEText(inline_html, 'html'))

        self.server.sendmail(settings.BOT_EMAIL, [recipient],
                             message.as_string())

    def close(self):
        """
        Clôture de la connexion
        """
        self.server.quit()
