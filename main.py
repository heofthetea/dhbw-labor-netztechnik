import time
from models.bpdu import BPDU
from models.switch import Switch
from config import load_yaml, init_switches


def main():
    switches = init_switches(load_yaml("network.yml"))
    for switch in switches.values():
        switch.start()

    time.sleep(5)  # Let the switches run for a while
    for switch in switches.values():
        switch.stop()
    print("All switches stopped.")


if __name__ == "__main__":

    main()
