import time
import threading
import queue

from models.bpdu import BPDU


class Switch:

    TIMEOUT = 1  # timeout waited between bpdus, in seconds

    def __init__(self, given_id: str, mac_address: str, *, priority: int = 32768):
        self.given_id = (
            given_id  # the name given to the switch in the yaml configuration
        )
        self.mac_address = Switch.mac_to_int(mac_address)
        self.priority = priority
        self.neighbours: dict[Switch, int] = {}

        self.root_switch = self  # assume I am root on init
        self.root_costs = 0
        self.root_port: Switch = None

        self.queue = queue.Queue()
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.running = False

    def __repr__(self):
        return f"Switch(given_id={self.given_id}, mac_address={self.mac_address}, priority={self.priority})"

    def __lt__(self, other):
        return (self.priority, self.mac_address) < (other.priority, other.mac_address)

    @staticmethod
    def mac_to_int(mac_address: str) -> int:
        return int(mac_address.replace(":", ""), 16)

    def log(self, message: str):
        print(f"[{self.given_id}] {message}")

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def send_bpdu(self):
        """
        Send a BPDU to all neighbours.
        """
        bpdu = BPDU(self, self.root_switch, self.root_costs)
        for neighbour in self.neighbours:
            neighbour.queue.put(bpdu)

    def process_bpdu(self, bpdu: BPDU):
        """
        Process a BPDU received from a neighbour.
        """
        if bpdu.root_switch < self.root_switch:
            self.root_switch = bpdu.root_switch
            self.root_costs = bpdu.root_costs + self.neighbours[bpdu.sender]
            self.root_port = bpdu.sender
            self.log(f"updated root: {self.root_switch.given_id}")

        elif bpdu.root_switch == self.root_switch:
            if bpdu.root_costs + self.neighbours[bpdu.sender] < self.root_costs:
                self.root_costs = bpdu.root_costs + self.neighbours[bpdu.sender]
                self.root_port = bpdu.sender
                self.log(
                    f"updated root costs: {self.root_costs} via {self.root_port.given_id}"
                )

    def run(self):
        while self.running:
            self.send_bpdu()

            while not self.queue.empty():
                try:
                    bpdu = self.queue.get_nowait()
                    self.process_bpdu(bpdu)
                    self.queue.task_done()
                except queue.Empty:
                    pass
            time.sleep(Switch.TIMEOUT)
