import yaml


class BackendSelector:
    """
    BackendSelector dynamically selects the PQC and quantum backends
    based on a configuration file.
    """

    def __init__(self, config_file="config.yaml"):
        try:
            with open(config_file, "r") as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file '{config_file}' not found.")

    def get_pqc_backend(self) -> str:
        """
        Retrieve the PQC backend from the configuration file.
        Defaults to 'quantcrypt'.
        """
        return self.config.get("pqc_backend", "quantcrypt")

    def get_quantum_backend(self) -> str:
        """
        Retrieve the quantum backend from the configuration file.
        Defaults to 'quantum_lib'.
        """
        return self.config.get("quantum_backend", "quantum_lib")
