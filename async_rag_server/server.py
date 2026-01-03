from concurrent.futures import ProcessPoolExecutor
from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
import multiprocessing
from queues.worker import process_query
from client.rq_client import run_worker, queue


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Use multiprocessing instead of threading to allow signal handlers
#     worker_process = multiprocessing.Process(target=run_worker, daemon=True)
#     worker_process.start()
#     print("✅ RQ Worker started")

#     yield

#     # Shutdown: terminate the worker process
#     worker_process.terminate()
#     worker_process.join(timeout=5)
#     print("🛑 Shutting down RQ Worker")

# ad89fdef-8246-418c-aa15-83856a8e0637, 6532d534-b48f-40da-8ba9-5df6a57bba0d , 6a691052-22f0-4188-8a18-6ff764b60800 ,80cd25d2-1cec-4cb0-b571-733df388a623
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create a managed pool of worker processes
    num_workers = 4
    executor = ProcessPoolExecutor(max_workers=num_workers)

    # Submit worker tasks to the pool
    futures = [executor.submit(run_worker) for _ in range(num_workers)]

    print(f"✅ RQ Worker pool started with {num_workers} workers")

    yield

    # Shutdown: gracefully shutdown the executor
    executor.shutdown(wait=True, cancel_futures=True)
    print("🛑 Shutting down RQ Worker pool")


app = FastAPI(lifespan=lifespan)


@app.post("/chat")
def chat(query: str = Query(..., description="The user's query")):
    # Placeholder for chat processing logic
    job = queue.enqueue(process_query, query)
    return {"status": "queued", "job_id": job.id}


@app.get("/result/{job_id}")
def get_result(job_id: str):
    job = queue.fetch_job(job_id)
    if job is None:
        return {"status": "not found"}
    elif job.is_finished:
        return {"status": "finished", "result": job.result}
    elif job.is_queued:
        return {"status": "queued"}
    elif job.is_started:
        return {"status": "in progress"}
    else:
        return {"status": "unknown"}
