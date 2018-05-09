from threading import Thread, Lock
from host import Host
import random
import time

class Medium(Thread):

    def __init__(self, length, latency):
        Thread.__init__(self)
        self.reset = False
        self.medium_array = [0] * length
        self.hosts = [None] * length
        self.latency = latency
        self.lock = Lock()
        self.jammed = False

    def add_host(self, host, position):
        host.set_position(position)
        self.hosts[position] = host

    def is_empty(self):
        with self.lock:
            empty = True
            for element in self.medium_array:
                if element != 0:
                    empty = False
        return empty

    def insert_bit(self, bit, position):
        with self.lock:
            cond = True
            if not self.jammed:
                print("Inserting new bit {}".format(bit))
                self.medium_array[position] = bit
            else:
                cond = False
        return cond

    def propagate_signal(self):
        if not self.is_empty() and not self.jammed:
            for i in range(len(self.medium_array)):
                if self.medium_array[i] != 0:
                    if (i+1) < len(self.medium_array):
                        if self.medium_array[i+1] == 0:
                            self.medium_array[i+1] = self.medium_array[i]
                            if self.hosts[i+1] != None:
                                self.hosts[i+1].receive(self.medium_array[i+1])
                            break
                else:
                    if (i+1) < len(self.medium_array):
                        if self.medium_array[i+1] != 0:
                            self.medium_array[i] = self.medium_array[i+1]
                            if self.hosts[i] != None:
                                self.hosts[i].receive(self.medium_array[i+1])
                            break
                if (i+1) < len(self.medium_array):
                    if (self.medium_array[i] != 0 and self.medium_array[i+1] != 0) and \
                    (self.medium_array[i] != self.medium_array[i+1]):
                        self.jammed = True
                        self.medium_array[i], self.medium_array[i+1] = "JAM", "JAM" 
                        break
            print("Propagation: {}".format(self.medium_array))
        pass

    def is_jammed(self):
        with self.lock:
            if self.jammed:
                for i in range(len(self.medium_array) - 1):
                    if self.medium_array[i] == "JAM":
                        self.medium_array[i+1] = "JAM"

                    if (i - 1) >= 0:
                        if self.medium_array[i] == "JAM":
                            self.medium_array[i-1] = "JAM"


                is_still_jammed = False

                for i in range(len(self.medium_array)):
                    if self.medium_array[i] != "JAM":
                        is_still_jammed = True
                
                if not is_still_jammed:
                    for i in range(len(self.medium_array)):
                        self.medium_array[i] = 0
                    self.jammed = False
                print("Propagation: {}".format(self.medium_array))

    def received(self, bit):
        with self.lock:
            received = True
            for i in range(len(self.medium_array)):
                if self.medium_array[i] != bit:
                    received = False
            if received:
                for i in range(len(self.medium_array)):
                    self.medium_array[i] = 0
                self.reset = True
        return received

    def clear(self):
        with self.lock:
            item = self.medium_array[0]
            clear = True
            for i in range(len(self.medium_array)):
                if self.medium_array[i] != item:
                    clear = False
            if clear:
                for i in range(len(self.medium_array)):
                    self.medium_array[i] = 0

    def is_finished(self):
        finished = True
        for host in self.hosts:
            if host != None:
                if not host.is_done:
                    finished = False
        return finished

    
    def run(self):
        print("Starting simulation!")

        for host in self.hosts:
            if host != None:
                print("Strating host {}".format(host.name))
                host.start()

        while not self.is_finished():
            time.sleep(random.uniform(0.001, self.latency))
            self.reset = False
            self.propagate_signal()
            self.is_jammed()
            self.clear()

        print("Simulation finished")
        pass