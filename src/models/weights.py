from typing import Dict

class Weight:
    def __init__(self, weights: Dict[str, float]):
        self.weights = weights

    @staticmethod
    def validate_weights(weights: Dict[str, float]) -> bool:
        weight_total = 0
        for weight in weights.values():
            weight_total += weight
        
        if weight_total != 1:
            return False
        return True