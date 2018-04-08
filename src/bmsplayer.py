import time
import ledcontroller

class BMSPlayer:
    def __init__(self):
        self.controller = ledcontroller.Controller()

    def play(self, bmsr):
        print("start")
        t = 0.0
        for i, result in enumerate(bmsr):
            print(str(result.timing) + ":{0}".format(result.note))
            if t < result.timing:
                time.sleep(result.timing - t)
            t = result.timing
            self.__flash(result.note)
        print("end")
        time.sleep(1)
        self.controller.stop()

    def __flash(self, array):
        for i, v in enumerate(array):
            if v > 0:
                self.controller.on(i)
            #else:
            #    self.controller.off(i)

