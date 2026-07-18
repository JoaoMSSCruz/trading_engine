"""This must be used to dynamically import brokers
Exemple: "Alpaca": {"execution_broker_class_name": "ExecutionAlpaca", "execution_broker_module_path": "src.execution.execution_broker.execution_alpaca"} 
"""
BROKER_MAPPER = {
    "Alpaca": {"execution_broker_class_name": "ExecutionAlpaca", "execution_broker_module_path": "src.execution.execution_broker.execution_alpaca"},
}