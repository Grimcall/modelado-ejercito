
from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .unit import Unit
    
class UnitTransformation(NamedTuple):
    target_unit: type["Unit"]
    gold_cost: int


# Unit exceptions
class UnitTransformationError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

# Army/civ excepetions
class InvalidArmyError(Exception):
    pass

class InsufficientUnitsError(Exception):
    pass