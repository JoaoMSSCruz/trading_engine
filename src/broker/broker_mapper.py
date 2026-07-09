"""This must be used to dynamically import brokers
Exemple: "Alpaca": {"broker_class_name": "Alpaca", "broker_module_path": "src.broker.alpaca"} 
"""
BROKER_MAPPER = {
    "Alpaca": {"broker_class_name": "Alpaca", "broker_module_path": "src.broker.alpaca"},
}