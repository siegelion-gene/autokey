import threading
import time


class ThreadHandler(threading.Thread):
    def __init__(self, target_func):
        self.func = target_func
        threading.Thread.__init__(self)
        self.daemon = True
        # flag to pause thread
        self.paused = False
        self.event = threading.Event()
        # Explicitly using Lock over RLock since the use of self.paused
        # break reentrancy anyway, and I believe using Lock could allow
        # one thread to pause the worker, while another resumes; haven't
        # checked if Condition imposes additional limitations that would
        # prevent that. In Python 2, use of Lock instead of RLock also
        # boosts performance.
        self.pause_cond = threading.Condition(threading.Lock())

    def run(self):
        while not self.event.wait(1):
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
                self.func()

    def pause(self):
        if not self.paused:
            self.paused = True
            # If in sleep, we acquire immediately, otherwise we wait for thread
            # to release condition. In race, worker will still see self.paused
            # and begin waiting until it's set back to False
            self.pause_cond.acquire()

    def resume(self):
        if self.paused:
            self.paused = False
            # Notify so thread will wake after lock released
            self.pause_cond.notify()
            # Now release the lock
            self.pause_cond.release()

    def stop(self):
        if self.is_alive():
            self.event.set()
            self.join()


if __name__ == "__main__":
    def f():
        print("doing")
    me = ThreadHandler(target_func=f)
    me.start()
    print("ready")
    time.sleep(5)
    print("pausing")
    me.pause()
    time.sleep(5)
    print("resume")
    me.resume()
    time.sleep(5)
    me.stop()