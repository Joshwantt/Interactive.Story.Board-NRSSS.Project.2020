from gpiozero import OutputDevice
from  multiprocessing import Process
from time import time
from settings import DEBUG

class CommonOutput(OutputDevice):

    def __init__(self, pin, duration, interval, total_pulses):
        if DEBUG:
            # Some dummy functions to prevent the game crashing on a non-raspberry pi.
            # THERE WILL BE WARNINGS BUT THIS IS ONLY FOR DEVELOPMENT.
            self.custom_toggle = lambda *args: None
            self.custom_off = lambda *args: None
        else:
            super(CommonOutput, self).__init__(pin)
            self.custom_toggle = self.toggle
            self.custom_off = self.off

        self.terminate = False
        self.duration = duration
        self.interval = interval
        self.total_pulses = total_pulses

    def send_pulses(self):
        start = time()
        pulses = []
        
        for pulse in range(self.total_pulses):
            pulses.append(self.duration)
            pulses.append(self.interval)

        # Remove last interval
        pulses.pop()

        for index, pulse in enumerate(pulses):
            self.custom_toggle()
            while pulses[index] > time() - start:
                if self.terminate:
                    exit()
            start = time()
        self.custom_off()

    def pulse(self):
        if DEBUG:
            return
        thread = Process(target=self.send_pulses)
        thread.start()

    def kill_all(self):
        """
        This function will kill any running threads.
        """
        self.terminate = True

class Fan(CommonOutput):
    pass

class VibeMat(CommonOutput):
    pass

class Rotors(CommonOutput):
    pass

class Custom(CommonOutput):
    pass

if __name__ == "__main__":
    o = VibeMat(13, 5, 5, 5)
    o.pulse()

