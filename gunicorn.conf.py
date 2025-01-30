# gunicorn.conf.py
import multiprocessing

bind = "0.0.0.0:$PORT"
workers = multiprocessing.cpu_count() * 2 + 1  # Adjust as needed
threads = 2  # Adjust as needed
