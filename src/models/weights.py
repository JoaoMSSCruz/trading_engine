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
        
        """This check prevents weight sum != 1 and floating point deviations"""
        if not math.isclose(weight_total, 1.0, rel_tol=1e-9): 
            raise ValueError(f"Invalid weights: Sum of weights must be exactly 1.0, got {weight_total}")
    
    