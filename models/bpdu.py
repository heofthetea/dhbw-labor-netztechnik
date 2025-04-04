from models.switch import Switch


class Bpdu:
    def __init__(self, switch: Switch, root_switch: Switch, root_path_cost: int):
        self.switch = switch
        self.root_switch = root_switch
        self.root_path_cost = root_path_cost
