from typing import Dict

class Weights:
    def __init__(self, weights: Dict[str, float]):
        self.weights = weights

    def get_weights(self) -> Dict[str, float]:
        return self.weights

    def __str__(self) -> str:
        weights_str = ""
        for symbol, weight in self.weights.items():
            weights_str += f"{symbol}: {weight}\n"
        return weights_str

    @staticmethod
    def validate_weights(weights: Dict[str, float]) -> bool:
        weight_total = 0
        for weight in weights.values():
            weight_total += weight
        
        if weight_total != 1:
            return False
        return True
    
    