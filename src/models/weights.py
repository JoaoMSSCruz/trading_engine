import math
from typing import Dict

class Weights:
    def __init__(self, weights: Dict[str, float]):
        self.validate_weights(weights=weights)

        self.weights = weights

    def get_weights(self) -> Dict[str, float]:
        return self.weights

    def __str__(self) -> str:
        weights_str = ""
        for symbol, weight in self.weights.items():
            weights_str += f"{symbol}: {weight}\n"
        return weights_str

    @staticmethod
    def validate_weights(weights: Dict[str, float]) -> None:
        weight_total = 0
        for weight in weights.values():
            weight_total += weight
        
        if not (0 <= weight_total <= 1):
            raise ValueError("Invalid weights: Sum of weights must be between 0 and 1.")
    
    