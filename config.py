import yaml


def load_config(file_path):
    """
    Load the configuration file and return the configuration dictionary.
    """
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config


if __name__ == "__main__":
    print(load_config("network.yml"))
