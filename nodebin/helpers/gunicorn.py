import os
import multiprocessing


bind = '0.0.0.0:{}'.format(os.getenv('PORT', 8000))
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
