import time
from config import load_yaml, init_switches


def main():
    switches = init_switches(load_yaml("network.yml"))
    for switch in switches.values():
        switch.start()

    for switch in switches.values():
        switch.thread.join()  # Wait for all threads to finish
    print("All switches have finished.")


if __name__ == "__main__":
    main()
