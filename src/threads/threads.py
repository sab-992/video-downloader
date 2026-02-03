import threading
from queue import Queue
from src.threads.task import Task
from src.utils.logger import Logger, Level
from src.utils.settings import MAX_POOL_THREADS, QUEUE_TIMEOUT_SECONDS
from typing import Any


results_lock = threading.Lock()

class Threads:
    def __init__(self, pool=True, thread_count=MAX_POOL_THREADS):
        self.stop_event = threading.Event()
        self.__td_pool: list[threading.Thread] = []
        self.__results: dict[int, Any] = {}
        self.__task_queue: Queue[Task] = Queue()

        if not pool:
            return

        for i in range(thread_count):
            self.__td_pool.append(threading.Thread(target=self.__loop, args=(i,)))

    def add_task(self, task: Task) -> None:
        self.__task_queue.put(task)

    def create_thread(self, task:Task, args=None, kwargs=None):
        return threading.Thread(target=task.execute, args=args, kwargs=kwargs)

    def __len__(self):
        return len(self.__td_pool)

    def start_all(self):
        if len(self.__td_pool) <= 0:
            return

        for th in self.__td_pool:
            th.start()

    def stop_all(self) -> dict[int, Any]:
        if len(self.__td_pool) <= 0:
            return

        self.stop_event.set()
        for th in self.__td_pool:
            th.join()

        return self.__results

    def __loop(self, id: int):
        while not self.stop_event.is_set():
            try:
                task: Task = self.__task_queue.get(block=True, timeout=QUEUE_TIMEOUT_SECONDS)
                result = task.execute(id)

                with results_lock:
                    self.__results[id] = result
            except:
                Logger.log(message=f"Thread #{id}: No tasks found!", level=Level.WARNING)