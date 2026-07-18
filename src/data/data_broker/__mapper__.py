"""This must be used to dynamically import brokers
Exemple: "Alpaca": {"data_broker_class_name": "DataAlpaca", "data_broker_module_path": "src.data.data_broker.data_alpaca"} 
"""
BROKER_MAPPER = {
    "Alpaca": {"data_broker_class_name": "DataAlpaca", "data_broker_module_path": "src.data.data_broker.data_alpaca"},
}