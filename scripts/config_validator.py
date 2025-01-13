import yaml
import sys

REQUIRED_FIELDS = [
    "pqc_backend",
    "quantum_backend",
    "blockchain",
    "smart_contracts",
    "quantum_services",
    "logging",
    "monitoring",
    "api",
    "keys",
    "development"
]

def validate_config(config_path):
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        for field in REQUIRED_FIELDS:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")

        print("Config validation successful.")
        return True
    except Exception as e:
        print(f"Config validation failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python config_validator.py <path_to_config>")
        sys.exit(1)

    config_path = sys.argv[1]
    if not validate_config(config_path):
        sys.exit(1)
