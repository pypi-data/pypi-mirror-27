# Changelog


## Next version

### New

* Slogan de l'instance. [Renaud Canarduck]

* Us: ajout variable INSTANCE_NAME. [Renaud Canarduck]

* Intégration premailer. [Renaud Canarduck]

* Système de personalisation des gabarits. [Renaud Canarduck]

* Init du support des gabarits personnalisés. [Renaud Canarduck]

### Fix

* Suppression des styles non standardisés dans html. [Renaud Canarduck]

* Gestion du on_delete cascade sur la clé feed des Subscription. [Renaud Canarduck]


## v0.3.0 (2017-11-29)

### New

* Utilisation de fake_useragent pour passer les bloquages des crawlers. [Renaud Canarduck]

  newspaper était bloqué par certains sites (OuestFrance par exemple)

### Changes

* Mise à jour de la documention dédiée à l'installation. [Renaud Canarduck]

* Amélioration de la CLI. [Renaud Canarduck]

* La tâche init execute les 3 tâches d'initialisation de flumel. [Renaud Canarduck]

* Amélioration documentation dédiée à l'installation. [Renaud Canarduck]

### Other

* Punkt. [Renaud Canarduck]


## v0.2.0 (2017-11-26)

### Fix

* Regex abo/désabo. [Renaud Canarduck]

* Décodage sujet emails. [Renaud Canarduck]

* Typo sur url ww2w. [Renaud Canarduck]

* Mode TESTING. [Renaud Canarduck]

* SetUpClass pour les tests fonctionnels. [Renaud Canarduck]

* Le résultat d'une task huey est un objet. [Renaud Canarduck]

* Huey en mode thread plutôt que greenlet. [Renaud Canarduck]


## v0.1.0 (2017-11-19)

### New

* Coverage html report sur gitlab. [Renaud Canarduck]

* CLI pour amorcer le fichier de configuration. [Renaud Canarduck]

* Découplage des tâches et mise en place de huey. [Renaud Canarduck]

* Detection de flux sur une page. [Renaud Canarduck]

* Init tests subscriptions. [Renaud Canarduck]

### Changes

* Docker dédié aux services mails. [Renaud Canarduck]

### Fix

* Test sur les modèles. [Renaud Canarduck]

* Nettoyage imap avant vérification désinscription. [Renaud Canarduck]

* Pour peewee delete_instance au lieu de delete. [Renaud Canarduck]

* Test get_or_create feed avec 2 titres différents.. [Renaud Canarduck]

* Code de retour désabonnement. [Renaud Canarduck]

* Gestion smtp sans auth. [Renaud Canarduck]

* Gestion smtp sur port 25. [Renaud Canarduck]

* Nettoyage dépendances. [Renaud Canarduck]

* Gestion flux invalide. [Renaud Canarduck]

* Decorateur tasks. [Renaud Canarduck]

* Mise à jour de la documentation. [Renaud Canarduck]

* Simplification du service flumel. [Renaud Canarduck]

  * timers délégués à huey
  * un seul service

* Refactorisation. [Renaud Canarduck]

  * remplacement ponyorm par peewee
  * restructuration des fichiers
  * tests HS

* Avancement tests subscribe / unsubscribe. [Renaud Canarduck]


## v0.0.2 (2017-11-12)

### New

* Logo. [Renaud Canarduck]

* Modèles de fichiers pour systemd. [Renaud Canarduck]

* Generateur de page d’info. [Renaud Canarduck]

* Interface en ligne de commande. [Renaud Canarduck]

* Init mkdocs sur readthedocs. [Renaud Canarduck]

* Boucle de traitement de la boite mail. [Renaud Canarduck]

* Settings pour logger. [Renaud Canarduck]

* Regex dans le fichier de config. [Renaud Canarduck]

* Envoi des articles par mail. [Renaud Canarduck]

* Templates pour les notifications de base. [Renaud Canarduck]

* Premier template de mail. [Renaud Canarduck]

* Mise en place d'un fichier de configuration. [Renaud Canarduck]

* Analyse des articles par newspaper. [Renaud Canarduck]

* Champs pour gérer les headers de modification des flux. [Renaud Canarduck]

* Vérification du flux avant abonnement. [Renaud Canarduck]

* Base pour les modèles & les notifications. [Renaud Canarduck]

* Init de la structure du projet. [Renaud Canarduck]

### Fix

* Amélioration template page. [Renaud Canarduck]

* Ignorer build pypi. [Renaud Canarduck]

* Typo settings. [Renaud Canarduck]

* Simplification accueil de la doc et création d'une page pourquoi. [Renaud Canarduck]

* Correctif template article. [Renaud Canarduck]

* Suppression d'un flux quand plus personne n'y est abonné. [Renaud Canarduck]

* Suppression debug inutile. [Renaud Canarduck]

* Refaco regex bot. [Renaud Canarduck]

* Nettoyage arborescence. [Renaud Canarduck]

* Amélioration des emails. [Renaud Canarduck]

  * suppression des titres inutiles dans le corps
  * amélioration des sujets

* Logger sur notification au lieu des print. [Renaud Canarduck]

* Simplification de la doc. [Renaud Canarduck]

* Simplification du model. [Renaud Canarduck]

### Other

* Init. [Renaud Canarduck]


