"""
MULTIPROCESSING
===============
Process, Pool, Queue, Pipe, shared memory, Manager, and ProcessPoolExecutor.
Bypasses the GIL for true CPU-bound parallelism.

IMPORTANT: On macOS/Windows (spawn start method) child processes re-import this
module, so ALL worker functions must be at module level (not nested inside
other functions) to be picklable. Guard demo code in `if __name__ == "__main__"`.

Run: python 03_advanced/08_multiprocessing.py
"""

import os
import time
import random
from multiprocessing import (
    Process, Pool, Queue, Pipe, Value, Array, Lock,
    Manager, cpu_count
)
from concurrent.futures import ProcessPoolExecutor, as_completed


# ── Module-level worker functions (required for pickling on macOS/Windows) ───

def cpu_bound_task(n):
    """Purely CPU-bound — compute sum of squares."""
    return sum(i * i for i in range(n))

def process_child(name_value):
    """Worker for demo_process — receives (name, delay) tuple."""
    name, value = name_value
    print(f"  Child [{name}] PID={os.getpid()}")
    time.sleep(value)

def producer_q(q, items):
    for item in items:
        q.put(item)
        print(f"  [producer] put {item}")
    q.put(None)   # sentinel

def consumer_q(q, results_q):
    while True:
        item = q.get()
        if item is None:
            break
        result = item * item
        results_q.put(result)

def child_pipe(conn):
    for _ in range(5):
        msg = conn.recv()
        conn.send(msg.upper())
    conn.close()

def increment_value(val, lock, n):
    for _ in range(n):
        with lock:
            val.value += 1

def add_to_manager_dict(d, key, value):
    d[key] = value


# ── 1. Process — Low-Level API ────────────────────────────────────────────────

def demo_process():
    print("--- Process ---")

    p1 = Process(target=process_child, args=(("A", 0.05),), name="Child-A")
    p2 = Process(target=process_child, args=(("B", 0.02),), name="Child-B")

    p1.start()
    p2.start()

    p1.join()             # wait for p1 to finish
    p2.join(timeout=1.0)  # wait up to 1 second
    if p2.is_alive():
        p2.terminate()    # send SIGTERM
        p2.join()

    print(f"  p1 exit code: {p1.exitcode}")   # 0 = success
    print(f"  p2 exit code: {p2.exitcode}")


# ── 2. Pool — Parallel Map over Multiple Processes ────────────────────────────

def demo_pool():
    print("\n--- Pool ---")
    cpus = cpu_count()
    print(f"  CPU count: {cpus}")

    data = [2_000_000, 1_500_000, 3_000_000, 2_500_000]

    # Sequential:
    t0 = time.perf_counter()
    seq_results = [cpu_bound_task(n) for n in data]
    t1 = time.perf_counter()
    print(f"  Sequential: {t1-t0:.3f}s")

    # Parallel with Pool.map():
    t0 = time.perf_counter()
    with Pool(processes=min(cpus, 4)) as pool:
        par_results = pool.map(cpu_bound_task, data)
    t1 = time.perf_counter()
    print(f"  Parallel:   {t1-t0:.3f}s")

    assert seq_results == par_results, "Results mismatch!"
    print("  Results match ✓")


def demo_pool_async():
    print("\n--- Pool async ---")

    with Pool(processes=4) as pool:
        # apply_async submits one call, returns an AsyncResult
        ar = pool.apply_async(cpu_bound_task, (1_000_000,))
        result = ar.get(timeout=30)
        print(f"  apply_async: {result}")

        # map_async — non-blocking map
        ar_map = pool.map_async(cpu_bound_task, [500_000] * 4)
        results = ar_map.get(timeout=60)
        print(f"  map_async:   {results}")

        # starmap — multiple args per call
        tasks = [(i * 100_000,) for i in range(1, 5)]
        results = pool.starmap(cpu_bound_task, tasks)
        print(f"  starmap:     {results}")


# ── 3. Queue — Inter-Process Communication ────────────────────────────────────

def demo_queue():
    print("\n--- Queue ---")
    task_q   = Queue()
    result_q = Queue()

    p = Process(target=producer_q, args=(task_q, range(1, 6)))
    c = Process(target=consumer_q, args=(task_q, result_q))

    p.start(); c.start()
    p.join();  c.join()

    results = []
    while not result_q.empty():
        results.append(result_q.get())
    print(f"  Results: {sorted(results)}")


# ── 4. Pipe — Two-Endpoint Communication ──────────────────────────────────────

def demo_pipe():
    print("\n--- Pipe ---")
    parent_conn, child_conn = Pipe()   # returns two Connection objects

    p = Process(target=child_pipe, args=(child_conn,))
    p.start()

    messages = ["hello", "world", "python", "multi", "process"]
    for msg in messages:
        parent_conn.send(msg)
        reply = parent_conn.recv()
        print(f"  sent: {msg!r}, got: {reply!r}")

    p.join()
    parent_conn.close()


# ── 5. Shared Memory — Value and Array ───────────────────────────────────────

def demo_shared_memory():
    print("\n--- Shared Value/Array ---")
    # Value: single typed value shared across processes
    lock     = Lock()
    counter  = Value("i", 0)   # "i" = C signed int
    n_each   = 10_000

    processes = [Process(target=increment_value, args=(counter, lock, n_each))
                 for _ in range(4)]
    for p in processes: p.start()
    for p in processes: p.join()

    print(f"  Counter: {counter.value} (expected {4 * n_each})")

    # Array:
    shared_arr = Array("d", [0.0] * 5)   # "d" = C double
    with shared_arr.get_lock():
        for i in range(5):
            shared_arr[i] = float(i * i)
    print(f"  Shared array: {list(shared_arr)}")


# ── 6. Manager — High-Level Shared State ─────────────────────────────────────

def demo_manager():
    print("\n--- Manager ---")
    # Manager provides a proxy for shared objects (list, dict, Queue, etc.)
    with Manager() as manager:
        shared_dict = manager.dict()

        processes = [
            Process(target=add_to_manager_dict, args=(shared_dict, f"key{i}", i))
            for i in range(5)
        ]
        for p in processes: p.start()
        for p in processes: p.join()

        print(f"  Shared dict: {dict(shared_dict)}")


# ── 7. ProcessPoolExecutor — Higher-Level API ─────────────────────────────────

def demo_process_pool_executor():
    print("\n--- ProcessPoolExecutor ---")
    tasks = [500_000 * (i + 1) for i in range(4)]

    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, tasks))
    print(f"  Ordered results: {results}")

    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(cpu_bound_task, n): n for n in tasks}
        for future in as_completed(futures):
            n   = futures[future]
            res = future.result()
            print(f"  n={n} → {res}")


# ── 8. Guidance ───────────────────────────────────────────────────────────────

def demo_guidance():
    print("\n--- When to use what ---")
    table = [
        ("I/O-bound (network, file, DB)",      "threading or asyncio"),
        ("CPU-bound (compute, number crunch)",  "multiprocessing"),
        ("Simple parallel map",                 "Pool.map or ProcessPoolExecutor"),
        ("Shared mutable state needed",         "Manager (slow) or Value/Array"),
        ("Producer-consumer pipeline",          "multiprocessing.Queue"),
        ("Two-process bidirectional comm.",     "Pipe"),
        ("Inside async code",                   "asyncio.run_in_executor"),
    ]
    for scenario, choice in table:
        print(f"  {scenario:<40} → {choice}")


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    demo_process()
    demo_pool()
    demo_pool_async()
    demo_queue()
    demo_pipe()
    demo_shared_memory()
    demo_manager()
    demo_process_pool_executor()
    demo_guidance()
    print("\nDone: multiprocessing")
