import multiprocessing

bind = "0.0.0.0:8000"  # Listen on all interfaces
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
