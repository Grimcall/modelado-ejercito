from typing import Optional, Type
from .utils import UnitTransformation, UnitTransformationError

class Unit:
    BASE_STRENGTH_SCORE: int
    TRAINING_BONUS: int
    TRAINING_GOLD_COST: int
    TRANSFORMS_INTO: Optional[UnitTransformation] = None

    def __init__(self, age:int = 0, strength_score:int = 0) -> None:
        self.age = age
        self.strength_score = self.BASE_STRENGTH_SCORE if strength_score == 0 else strength_score
        
    def get_age(self) -> int:
        return self.age

    def train(self, times_trained:int = 1) -> None:
        self.strength_score += self.TRAINING_BONUS * times_trained

    def transform(self) -> "Unit":
        if not self.TRANSFORMS_INTO:
            raise UnitTransformationError("This unit has no available transformations.")
        
        target_class: Type[Unit] = self.TRANSFORMS_INTO.target_unit
        
        # when changing classes, we preserve current unit STR while adding the diff between base STR of target and source.
        # classes only ever upgrade their STR stat, so no need to handle negative STR scenario.
        self.strength_score += (target_class.BASE_STRENGTH_SCORE - self.BASE_STRENGTH_SCORE)
        
        # mutate class directly to avoid reinstancing instead of deleting + creating a new one.
        object.__setattr__(self, '__class__', target_class)
        
        return self
    
class Knight(Unit):
    BASE_STRENGTH_SCORE = 20
    TRAINING_BONUS = 10
    TRAINING_GOLD_COST = 30

class Bowman(Unit): 
    BASE_STRENGTH_SCORE = 10
    TRAINING_BONUS = 5
    TRAINING_GOLD_COST = 20
    TRANSFORMS_INTO = UnitTransformation(
        target_unit = Knight,
        gold_cost=50
    )

class Pikeman(Unit):
    BASE_STRENGTH_SCORE = 5
    TRAINING_BONUS = 3
    TRAINING_GOLD_COST = 10
    TRANSFORMS_INTO = UnitTransformation(
        target_unit = Bowman,
        gold_cost = 30
    )