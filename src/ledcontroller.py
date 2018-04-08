# -*- coding:utf-8 -*-

from threading import Thread
import time

try:
    import speakerphat
except ImportError:
    exit("This library requires the speakerphat module")


class ControllerThread(Thread):
    def __init__(self, status):
        super(ControllerThread, self).__init__()
        self.status = status
        self.running = True

    def run(self):
        fps = 120
        wt = 1 / fps
        while self.running:
            t = time.perf_counter()
            self.flash()
            self.decrement()
            d = time.perf_counter() - t
            if d < wt:
                time.sleep(wt - d)

    def decrement(self):
        for i in range(10):
            self.status[i] -= 5 
            if self.status[i] < 0:
                self.status[i] = 0

    def flash(self):
        for i in range(10):
            speakerphat.set_led(i, self.status[i])
        speakerphat.show()

class Controller:
    def __init__(self):
        self.status = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.thread = ControllerThread(self.status)
        self.thread.start()

    def on(self, pos):
        self.status[pos] = 255

    def off(self, pos):
        self.status[pos] = 0

    def stop(self):
        self.thread.running = False

def main():
    c = Controller()
    c.on(1)
    c.on(2)
    time.sleep(1.3)
    c.off(1)
    c.on(4)
    time.sleep(0.3)
    c.on(0)
    c.on(5)
    c.on(8)
    c.on(9)
    time.sleep(3)
    c.stop()

if __name__== '__main__':
    main()

