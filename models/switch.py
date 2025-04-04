class Switch:

    neighbours: list["Switch"] = []

    def __init__(self, mac_address: str, *, priority: int = 32768):
        self.mac_address = Switch.mac_to_int(mac_address)
        self.priority = priority

    @staticmethod
    def mac_to_int(mac_address: str) -> int:
        return int(mac_address.replace(":", ""), 16)
