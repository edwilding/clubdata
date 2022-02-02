name = 'clubdata'
bind = '0.0.0.0:11111'
workers = 2
user = 'root'
group = 'www-data'
loglevel = 'debug'
errorlog = '/home/ubuntu/clubdata.gunicorn.error.log'
accesslog = '/home/ubuntu/clubdata.gunicorn.access.log'
