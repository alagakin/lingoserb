import multiprocessing

bind = ":51001"
workers = multiprocessing.cpu_count() * 2 + 1
errorlog = "gunicorn_learn_serbian.log"
