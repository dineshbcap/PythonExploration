"""
CONCURRENCY — THREADING
========================
threading.Thread, daemon threads, Lock, RLock, Semaphore, Event, Condition,
Barrier, Queue, ThreadPoolExecutor, and the GIL.

Run: python 03_advanced/07_concurrency_threading.py
"""

import threading
import time
import queue
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── 1. The GIL (Global Interpreter Lock) ─────────────────────────────────────

print("--- GIL Overview ---")
# CPython's GIL allows only ONE thread to execute Python bytecode at a time.
# This means threading does NOT give true CPU parallelism for pure-Python code.
#
# Threading IS useful for:
#   - I/O-bound tasks (network, file I/O) — GIL is released during I/O waits
#   - Tasks that spend time in C extensions that release the GIL (numpy, etc.)
#
# For CPU-bound parallelism, use multiprocessing (see 08_multiprocessing.py).


# ── 2. Basic Thread Creation ──────────────────────────────────────────────────

print("\n--- Basic threads ---")

def task(name, delay):
    """A simple task that sleeps and prints."""
    print(f"  [{name}] starting")
    time.sleep(delay)
    print(f"  [{name}] done after {delay}s")

# Create Thread objects
t1 = threading.Thread(target=task, args=("A", 0.1), name="Thread-A")
t2 = threading.Thread(target=task, args=("B", 0.05), name="Thread-B")

t1.start()   # start() spawns the OS thread
t2.start()

t1.join()    # wait for t1 to finish before continuing
t2.join()
print("Both threads finished")


# ── 3. Thread Subclass ────────────────────────────────────────────────────────

print("\n--- Thread subclass ---")

class WorkerThread(threading.Thread):
    def __init__(self, item_id):
        super().__init__(name=f"Worker-{item_id}", daemon=True)
        self.item_id = item_id
        self.result  = None

    def run(self):
        # run() is called in the new thread when start() is called
        self.result = self.item_id ** 2
        print(f"  {self.name}: {self.item_id}² = {self.result}")

workers = [WorkerThread(i) for i in range(1, 6)]
for w in workers: w.start()
for w in workers: w.join()
print("Results:", [w.result for w in workers])


# ── 4. Daemon Threads ─────────────────────────────────────────────────────────

print("\n--- Daemon threads ---")
# Daemon threads are killed automatically when the main program exits.
# Non-daemon threads prevent program exit until they complete.

def background_monitor():
    while True:
        # print("  [monitor] heartbeat")   # would flood the output
        time.sleep(0.01)

monitor = threading.Thread(target=background_monitor, daemon=True)
monitor.start()
# We don't join() daemon threads — they just stop when main exits.
print(f"Monitor daemon: {monitor.daemon}")


# ── 5. Race Condition Without a Lock ──────────────────────────────────────────

print("\n--- Race condition ---")
shared_counter = 0

def increment_unsafe(n):
    global shared_counter
    for _ in range(n):
        # NOT atomic: read → add → write is THREE separate steps
        # Another thread can interleave between them.
        shared_counter += 1

threads = [threading.Thread(target=increment_unsafe, args=(10_000,)) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print(f"Expected 50000, got {shared_counter}")   # Often < 50000 due to race condition


# ── 6. threading.Lock — Mutual Exclusion ─────────────────────────────────────

print("\n--- Lock ---")
lock = threading.Lock()
safe_counter = 0

def increment_safe(n):
    global safe_counter
    for _ in range(n):
        with lock:           # acquire lock, release when exiting with-block
            safe_counter += 1   # critical section — only one thread at a time

threads = [threading.Thread(target=increment_safe, args=(10_000,)) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print(f"Expected 50000, got {safe_counter}")   # Always 50000


# ── 7. threading.RLock — Reentrant Lock ──────────────────────────────────────

print("\n--- RLock ---")
# RLock can be acquired multiple times by the SAME thread without deadlocking.
# Useful for recursive functions or methods that both hold the same lock.

rlock = threading.RLock()

def recursive_with_rlock(depth):
    if depth == 0:
        return
    with rlock:   # same thread can acquire again
        print(f"  depth {depth}")
        recursive_with_rlock(depth - 1)

recursive_with_rlock(3)


# ── 8. threading.Semaphore — Limit Concurrency ────────────────────────────────

print("\n--- Semaphore ---")
# A semaphore counts available "slots". acquire() decrements, release() increments.
# When count is 0, acquire() blocks until another thread calls release().

MAX_CONCURRENT = 2
semaphore = threading.Semaphore(MAX_CONCURRENT)
active = 0
active_lock = threading.Lock()

def limited_task(task_id):
    global active
    with semaphore:
        with active_lock:
            active += 1
            print(f"  Task {task_id} started (active={active})")
        time.sleep(0.02)
        with active_lock:
            active -= 1
            print(f"  Task {task_id} done    (active={active})")

threads = [threading.Thread(target=limited_task, args=(i,)) for i in range(5)]
for t in threads: t.start()
for t in threads: t.join()


# ── 9. threading.Event — Signaling Between Threads ───────────────────────────

print("\n--- Event ---")
# Event has an internal flag. wait() blocks until flag is set.

start_event = threading.Event()

def waiter(name):
    print(f"  [{name}] waiting for signal...")
    start_event.wait()   # blocks until event is set
    print(f"  [{name}] signal received, proceeding")

threads = [threading.Thread(target=waiter, args=(f"T{i}",)) for i in range(3)]
for t in threads: t.start()

time.sleep(0.05)
print("  Setting event...")
start_event.set()   # all waiting threads unblock simultaneously

for t in threads: t.join()


# ── 10. threading.Queue — Thread-Safe Producer/Consumer ───────────────────────

print("\n--- Queue ---")
# queue.Queue is the safest way to share data between threads.
# It handles locking internally.

work_queue  = queue.Queue(maxsize=10)
result_list = []
result_lock = threading.Lock()

def producer(items):
    for item in items:
        work_queue.put(item)   # blocks if queue is full
    work_queue.put(None)       # sentinel: tells consumers to stop

def consumer(worker_id):
    while True:
        item = work_queue.get()   # blocks if queue is empty
        if item is None:
            work_queue.put(None)  # pass sentinel to next consumer
            break
        result = item ** 2
        with result_lock:
            result_list.append(result)
        work_queue.task_done()    # signal that this item is processed

p  = threading.Thread(target=producer, args=(range(1, 11),))
cs = [threading.Thread(target=consumer, args=(i,)) for i in range(3)]

p.start()
for c in cs: c.start()

p.join()
for c in cs: c.join()

print(f"Results: {sorted(result_list)}")   # [1, 4, 9, ..., 100]


# ── 11. ThreadPoolExecutor ────────────────────────────────────────────────────

print("\n--- ThreadPoolExecutor ---")

def fetch_url(url_id):
    """Simulated I/O-bound task (network request)."""
    time.sleep(random.uniform(0.01, 0.05))
    return f"response-{url_id}"

url_ids = list(range(1, 11))

# Submit all tasks and collect results as they complete:
with ThreadPoolExecutor(max_workers=4) as executor:
    # map() returns results in the SAME ORDER as inputs
    results = list(executor.map(fetch_url, url_ids))
print(f"map results: {results}")

# submit() for finer control:
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(fetch_url, uid): uid for uid in url_ids}
    for future in as_completed(futures):
        uid    = futures[future]
        result = future.result()
        print(f"  {uid}: {result}")


# ── 12. threading.local — Thread-Local Storage ────────────────────────────────

print("\n--- thread-local storage ---")
# threading.local() holds per-thread values — each thread sees its own version.

local_data = threading.local()

def thread_task(value):
    local_data.value = value          # each thread has its own .value
    time.sleep(random.uniform(0, 0.01))
    print(f"  {threading.current_thread().name}: local_data.value = {local_data.value}")

threads = [threading.Thread(target=thread_task, args=(i,), name=f"T{i}") for i in range(4)]
for t in threads: t.start()
for t in threads: t.join()


print("\nDone: concurrency_threading")
