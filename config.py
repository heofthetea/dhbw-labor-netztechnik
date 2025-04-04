import yaml

from models.switch import Switch


def load_yaml(file_path):
    """
    Load the configuration file and return the configuration dictionary.
    """
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def init_switches(config: dict) -> dict[str, Switch]:
    """
    Initialize switches based on the configuration.
    """
    switches = {
        k: Switch(
            given_id=k,
            mac_address=v["mac"],
            priority=v.get("priority", 32768),
        )
        for k, v in config["switches"].items()
    }

    switches = __init_neighbours(switches, config)
    return switches


def __init_neighbours(switches: dict[str, Switch], config: dict):
    """
    Initialize neighbours for each switch based on the configuration.
    """

    for switch, edges in config["edges"].items():
        for neighbour, cost in edges.items():
            switches[switch].neighbours[switches[neighbour]] = cost
            switches[neighbour].neighbours[switches[switch]] = cost
    return switches


if __name__ == "__main__":
    config = load_yaml("network.yml")

    switches = init_switches(config)
    print(len(switches))
