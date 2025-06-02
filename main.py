from config import load_yaml, init_switches
from models.switch import Switch


def main():
    switches = init_switches(load_yaml("network.yml"))
    for switch in switches.values():
        switch.start()

    for switch in switches.values():
        switch.thread.join()  # Wait for all threads to finish
    print("All switches have finished.")
    output(switches.values())


def output(switches: list[Switch]):
    """
    Print a representation of the spanning tree.
    """
    print("\n\nSpanning Tree:")
    for switch in switches:
        print(f"{switch.given_id}:")
        if switch.root_switch == switch:
            print(f"  root: {switch.given_id}")
            continue
        print(
            f"  root: {switch.root_switch.given_id} via {switch.root_port.given_id} (total cost: {switch.root_costs})"
        )


if __name__ == "__main__":
    main()
