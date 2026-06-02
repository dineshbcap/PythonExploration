"""
ASYNCIO
=======
async/await, coroutines, the event loop, Tasks, gather, wait,
timeouts, async generators, async context managers, streams,
and running sync code in executor.

Run: python 03_advanced/09_asyncio.py
"""

import asyncio
import time
import random
from typing import AsyncIterator

# ── 1. Coroutines and async/await ─────────────────────────────────────────────

print("--- Coroutines ---")
# A coroutine is defined with `async def`. Calling it returns a coroutine object.
# It runs only when awaited (or submitted to an event loop).

async def hello(name: str, delay: float) -> str:
    """A simple coroutine that waits then returns a greeting."""
    await asyncio.sleep(delay)   # non-blocking sleep — yields control to event loop
    return f"Hello, {name}!"

# Run a single coroutine:
result = asyncio.run(hello("Alice", 0.01))
print(result)

# asyncio.run() creates an event loop, runs the coroutine, then closes the loop.
# Never call asyncio.run() from inside an already-running loop.


# ── 2. Running Coroutines Concurrently ────────────────────────────────────────

async def demo_concurrent():
    print("\n--- Concurrent execution ---")

    # Sequential (one-at-a-time):
    t0 = time.perf_counter()
    r1 = await hello("Alice", 0.05)
    r2 = await hello("Bob",   0.05)
    print(f"Sequential: {time.perf_counter()-t0:.2f}s  {r1!r}, {r2!r}")

    # Concurrent with gather (run all at once, wait for ALL):
    t0 = time.perf_counter()
    r1, r2 = await asyncio.gather(
        hello("Alice", 0.05),
        hello("Bob",   0.05),
    )
    print(f"Concurrent: {time.perf_counter()-t0:.2f}s  {r1!r}, {r2!r}")

asyncio.run(demo_concurrent())


# ── 3. Tasks ──────────────────────────────────────────────────────────────────

async def demo_tasks():
    print("\n--- Tasks ---")
    # asyncio.create_task() schedules a coroutine for concurrent execution NOW.
    # It returns a Task object (a Future subclass).

    async def work(name, duration):
        print(f"  [{name}] starting")
        await asyncio.sleep(duration)
        print(f"  [{name}] done")
        return f"{name}-result"

    # Create tasks — they start running concurrently immediately
    task1 = asyncio.create_task(work("A", 0.05), name="TaskA")
    task2 = asyncio.create_task(work("B", 0.03), name="TaskB")
    task3 = asyncio.create_task(work("C", 0.07), name="TaskC")

    # await each task to get its result
    r1 = await task1
    r2 = await task2
    r3 = await task3
    print(f"  Results: {r1}, {r2}, {r3}")

    # Cancel a task:
    long_task = asyncio.create_task(asyncio.sleep(100))
    await asyncio.sleep(0)   # yield to let task start
    long_task.cancel()
    try:
        await long_task
    except asyncio.CancelledError:
        print("  Long task cancelled")

asyncio.run(demo_tasks())


# ── 4. gather() vs wait() ─────────────────────────────────────────────────────

async def demo_gather_wait():
    print("\n--- gather vs wait ---")

    async def task(n):
        await asyncio.sleep(random.uniform(0.01, 0.05))
        if n == 3:
            raise ValueError(f"Task {n} failed!")
        return n * n

    # gather() — raises on first exception unless return_exceptions=True
    results = await asyncio.gather(*[task(i) for i in range(5)], return_exceptions=True)
    for r in results:
        if isinstance(r, Exception):
            print(f"  Error: {r}")
        else:
            print(f"  OK: {r}")

    # wait() — more control: FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED
    coros = [task(i) for i in [1, 2, 4]]
    tasks = [asyncio.create_task(c) for c in coros]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    print(f"  First completed: {[t.result() for t in done]}")
    for t in pending: t.cancel()

asyncio.run(demo_gather_wait())


# ── 5. Timeouts ───────────────────────────────────────────────────────────────

async def demo_timeout():
    print("\n--- Timeouts ---")

    async def slow_op():
        await asyncio.sleep(5.0)
        return "done"

    # asyncio.wait_for — raises TimeoutError if coroutine doesn't complete in time
    try:
        result = await asyncio.wait_for(slow_op(), timeout=0.05)
    except asyncio.TimeoutError:
        print("  Timed out!")

    # Python 3.11+: asyncio.timeout context manager
    import sys
    if sys.version_info >= (3, 11):
        try:
            async with asyncio.timeout(0.05):
                await slow_op()
        except TimeoutError:
            print("  Timed out (3.11+ style)!")
    else:
        print(f"  asyncio.timeout() needs 3.11+, got {sys.version_info[:2]}")

asyncio.run(demo_timeout())


# ── 6. Async Context Managers ─────────────────────────────────────────────────

async def demo_async_cm():
    print("\n--- Async context managers ---")

    class AsyncDB:
        """Simulated async database connection."""

        async def __aenter__(self):
            print("  [DB] connecting...")
            await asyncio.sleep(0.01)
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            print("  [DB] closing...")
            await asyncio.sleep(0.005)
            return False   # don't suppress exceptions

        async def query(self, sql):
            await asyncio.sleep(0.01)
            return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

    async with AsyncDB() as db:
        rows = await db.query("SELECT * FROM users")
        print(f"  Got {len(rows)} rows")

    # contextlib.asynccontextmanager — generator-based async CM
    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def timer():
        start = time.perf_counter()
        try:
            yield
        finally:
            print(f"  elapsed: {time.perf_counter()-start:.4f}s")

    async with timer():
        await asyncio.sleep(0.02)

asyncio.run(demo_async_cm())


# ── 7. Async Iterators and Generators ────────────────────────────────────────

async def demo_async_gen():
    print("\n--- Async generators ---")

    async def stream_numbers(start: int, stop: int, delay: float = 0.01) -> AsyncIterator[int]:
        """Yields numbers with a delay between each (simulates streaming data)."""
        for i in range(start, stop):
            await asyncio.sleep(delay)
            yield i

    # async for — consumes an async iterable
    total = 0
    async for n in stream_numbers(1, 6):
        total += n
        print(f"  received {n}")
    print(f"  total: {total}")

    # Async comprehension:
    squares = [n**2 async for n in stream_numbers(1, 6)]
    print(f"  squares: {squares}")

    # aiter / anext (Python 3.10+):
    gen = stream_numbers(10, 13)
    print(await gen.__anext__())   # 10
    print(await gen.__anext__())   # 11

asyncio.run(demo_async_gen())


# ── 8. Async Queue — Producer/Consumer ────────────────────────────────────────

async def demo_async_queue():
    print("\n--- Async Queue ---")

    async def producer(q: asyncio.Queue, items):
        for item in items:
            await q.put(item)
            print(f"  produced: {item}")
        await q.put(None)   # sentinel

    async def consumer(q: asyncio.Queue, consumer_id: int):
        while True:
            item = await q.get()
            if item is None:
                await q.put(None)   # pass sentinel forward
                break
            await asyncio.sleep(0.01)  # simulate processing
            print(f"  consumer {consumer_id} processed: {item} → {item**2}")
            q.task_done()

    q = asyncio.Queue(maxsize=3)

    await asyncio.gather(
        producer(q, range(1, 8)),
        consumer(q, 1),
        consumer(q, 2),
    )

asyncio.run(demo_async_queue())


# ── 9. Run Blocking Code in Executor ──────────────────────────────────────────

async def demo_executor():
    print("\n--- run_in_executor ---")
    # Blocking calls (CPU-bound, legacy sync I/O) block the event loop.
    # run_in_executor() runs them in a thread pool, keeping the loop responsive.

    import concurrent.futures

    def blocking_cpu(n):
        return sum(i * i for i in range(n))

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_cpu, 500_000)
    print(f"  CPU result: {result}")

    # With explicit executor:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = await asyncio.gather(*[
            loop.run_in_executor(executor, blocking_cpu, 200_000)
            for _ in range(4)
        ])
    print(f"  Parallel results: {results}")

asyncio.run(demo_executor())


# ── 10. asyncio.Semaphore — Limit Concurrency ─────────────────────────────────

async def demo_semaphore():
    print("\n--- asyncio.Semaphore ---")
    semaphore = asyncio.Semaphore(2)   # max 2 concurrent

    async def limited(name):
        async with semaphore:
            print(f"  [{name}] running")
            await asyncio.sleep(0.02)
            print(f"  [{name}] done")

    await asyncio.gather(*[limited(f"T{i}") for i in range(5)])

asyncio.run(demo_semaphore())


print("\nDone: asyncio")
