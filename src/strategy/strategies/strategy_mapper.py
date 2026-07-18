"""This must be used to dynamically import strategies
Exemple: "MovingAverage": {"strategy_class_name": "MovingAverage", "strategy_module_path": "src.strategy.strategies.moving_average"} 
"""
STRATEGY_MAPPER = {
    "MovingAverage": {"strategy_class_name": "MovingAverage", "strategy_module_path": "src.strategy.strategies.moving_average"}
}