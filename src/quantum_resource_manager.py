class QuantumResourceManager:
    def __init__(self):
        self.resources = {}  # Resource management
        self.sensors = {}  # Sensor management
        self.models = {}  # Quantum AI models

    # --------------------
    # Resource Management
    # --------------------
    def allocate_resource(self, task_id, qubits_required):
        """Allocate quantum resources for a specific task."""
        self.resources[task_id] = qubits_required
        return f"Allocated {qubits_required} qubits for task {task_id}"

    def release_resource(self, task_id):
        """Release allocated resources for a specific task."""
        if task_id in self.resources:
            del self.resources[task_id]
            return f"Released resource for task {task_id}"
        raise ValueError("Task not found.")

    # --------------------
    # Sensor Management
    # --------------------
    def register_sensor(self, sensor_id, data_type):
        """Register a new quantum sensor for data collection."""
        self.sensors[sensor_id] = data_type
        return f"Sensor {sensor_id} registered for {data_type} data."

    def collect_data(self, sensor_id):
        """Collect data from a registered quantum sensor."""
        if sensor_id not in self.sensors:
            raise ValueError("Sensor not found.")
        return f"Data collected from sensor {sensor_id} ({self.sensors[sensor_id]})"

    # --------------------
    # Quantum AI Management
    # --------------------
    def train_model(self, model_id, data):
        """Train a quantum AI model using the provided data."""
        self.models[model_id] = "trained"
        return f"Model {model_id} trained with quantum acceleration."

    def infer(self, model_id, input_data):
        """Perform inference using a trained quantum AI model."""
        if model_id not in self.models:
            raise ValueError("Model not found.")
        return f"Quantum inference result for {input_data}"


# -------------------------
# Usage Example
# -------------------------
if __name__ == "__main__":
    qrm = QuantumResourceManager()
    print(qrm.allocate_resource("task001", 5))
    print(qrm.release_resource("task001"))
    print(qrm.register_sensor("sensor001", "temperature"))
    print(qrm.collect_data("sensor001"))
    print(qrm.train_model("model001", "training_data"))
    print(qrm.infer("model001", "input_data"))
