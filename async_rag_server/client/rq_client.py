from redis import Redis
from rq import Queue, Worker

# Configure Redis connection
connection= Redis(
    host="valkey",
    port=6379,
    password="password",
)

# Initialize RQ queue
queue = Queue(
    connection=connection
)
# uses default Redis connection settings

def run_worker():
    '''
    Start an RQ worker to process jobs from the queue.
    '''
    worker = Worker([queue], connection=connection)
    worker.work()