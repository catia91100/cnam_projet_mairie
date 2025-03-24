# gunicorn.conf.py

bind = '0.0.0.0:5000'  # Adressage de l'interface d'écoute (ici le port 5000)
workers = 4  # Nombre de travailleurs
worker_class = 'sync'  # Classe du worker (tu peux aussi utiliser 'gevent', 'eventlet', etc.)
accesslog = '-'  # Journal d'accès
errorlog = '-'  # Journal d'erreurs
loglevel = 'info'  # Niveau de logs (info, warning, error)
timeout = 30  # Timeout des travailleurs
max_requests = 1000  # Nombre maximal de requêtes par travailleur avant le redémarrage
pidfile = '/tmp/gunicorn.pid'  # Fichier de PID (optionnel)
