from threading import Thread
import random
import time

class Host(Thread):
    message = []
    attemps = 10
    position = -1

    def __init__(self, message, max_attemps, medium, name):
        Thread.__init__(self)
        self.name = name
        self.message = list(message)
        self.max_attemps = max_attemps
        self.medium = medium
        self.is_done = False
        pass

    def set_position(self, position):
        self.position = position
    
    def done(self):
        return self.is_done

    def receive(self, packet):
        print("received {} as {}".format(packet, self.name))

    def run(self):
        attemps = 0
        for bit in self.message:
            sent = False
            while attemps < self.max_attemps and not sent:
                attemps += 1
                bit_to_sent = "|{}|*{}*".format(self.name, bit)
                if not self.medium.jammed:
                    print("Trying to sent: {} as {}".format(bit_to_sent, self.name))
                    if self.medium.insert_bit(bit_to_sent, self.position):
                        while not self.medium.received(bit_to_sent) and not self.medium.is_empty():
                            print("checking if received")
                            if self.medium.jammed:
                                print("jammed")
                                sent = False
                                time.sleep(random.uniform(0.5, 2.0))
                                break
                            time.sleep(random.uniform(0.1, 0.2))
                            sent = True
                        if self.medium.reset:
                            time.sleep(random.uniform(0.2, 0.5))
                            sent = False
                
                if attemps >= self.max_attemps:
                    print("sending failed, to many tries, {} I surrender".format(self.name))
                    self.is_done = True
                    return
                time.sleep(random.uniform(0.3, 0.7))
        print("All data send, {} is finished".format(self.name))
        self.is_done = True
        return