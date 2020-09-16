worker_class = "uvicorn.workers.UvicornWorker"
workers = 2
bind = "0.0.0.0:8000"
accesslog = "-"
errorlog = "-"
access_log_format = (
    "%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s “%(r)s” %(s)s %(b)s “%(f)s” “%(a)s”"
)
timeout = 120
log_level = "info"
