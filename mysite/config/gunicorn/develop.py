import multiprocessing

bind = '127.0.0.1:8000'
workers = 2 # multiprocessing.cpu_count() * 2 + 1
pidfile = 'd/share/tmp/develop.pid'
max_requests = 1000
max_requests_jitter = 50
loglevel = 'debug'
