import time
import threading
import queue

from models.bpdu import BPDU


class Switch:
    """
    Class representing a switch in a layer 2 network.
    Attributes:
        given_id (str): Human-readable identifier of the switch, taken as the key from the yaml configuration.
        mac_address (int): MAC address of the switch, converted to an integer.
        priority (int): Priority of the switch, used for root bridge election.
        neighbours (dict[Switch, int]): Dictionary mapping the neighbour switches to their respective edge costs.
        root_switch (Switch): The current root switch for this switch.
        root_costs (int): The cost to reach the root switch.
        root_port (Switch): The "port" (represented as a neighbour) to the root switch.
        queue (queue.Queue): Thread-safe Queue for processing received BPDUs.
        running (bool): Flag indicating whether the switch is running.

    """

    def __init__(self, given_id: str, mac_address: str, *, priority: int = 32768):
        self.given_id = given_id
        self.mac_address = mac_address
        self.priority = priority
        self.neighbours: dict[Switch, int] = {}

        self.root_switch = self  # assume I am root on init
        self.root_costs = 0
        self.root_port: Switch = None

        # attributes used for threading
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.run)
        self.running = False

    def __repr__(self):
        return f"Switch(given_id={self.given_id}, mac_address={self.mac_address}, priority={self.priority})"

    def __lt__(self, other):
        return (self.priority, Switch.mac_to_int(self.mac_address)) < (
            other.priority,
            Switch.mac_to_int(other.mac_address),
        )

    def start(self):
        self.running = True
        self.thread.start()
        self.log("Started")

    def stop(self):
        self.running = False
        self.thread.join()
        self.log("Stopped")

    def send_bpdu(self):
        """
        Broadcast a BPDU to all neighbours.
        """
        bpdu = BPDU(self, self.root_switch, self.root_costs)
        for neighbour in self.neighbours:
            neighbour.queue.put(bpdu)

    def process_bpdu(self, bpdu: BPDU):
        """
        Process a BPDU received from a neighbour.
        Decides whether to accept the bpdu and update root switch or root path accordingly.
        """
        if bpdu.root_switch > self.root_switch:
            return

        if (
            bpdu.root_switch == self.root_switch
            and bpdu.root_costs + self.neighbours[bpdu.sender] >= self.root_costs
        ):
            return

        if bpdu.root_switch < self.root_switch:
            self.root_switch = bpdu.root_switch
            self.log(f"new root: {self.root_switch.given_id}")
        self.root_costs = bpdu.root_costs + self.neighbours[bpdu.sender]
        self.root_port = bpdu.sender
        self.log(f"new root costs: {self.root_costs} via {self.root_port.given_id}")

    def run(self):
        """
        Main loop of the switch.
        Sends BPDUs and processes the BPDU queue.
        """
        for _ in range(Switch.ITERATIONS):
            if not self.running:
                break
            self.send_bpdu()

            while not self.queue.empty():
                try:
                    bpdu = self.queue.get_nowait()
                    self.process_bpdu(bpdu)
                    self.queue.task_done()
                except queue.Empty:
                    pass
            time.sleep(Switch.TIMEOUT)
        self.log("done")
        self.running = False

    # ------------------------------------------------------
    ## helper methods

    @staticmethod
    def mac_to_int(mac_address: str) -> int:
        return int(mac_address.replace(":", ""), 16)

    def log(self, message: str):
        print(f"[{self.given_id}] {message}")
