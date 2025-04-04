class BPDU:
    def __init__(self, sender, root_switch, root_costs: int):
        self.sender = sender
        self.root_switch = root_switch
        self.root_costs = root_costs
