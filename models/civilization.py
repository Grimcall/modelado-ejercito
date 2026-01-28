from typing import Optional, Type, TYPE_CHECKING

from .utils import InvalidArmyError

if TYPE_CHECKING:
    from .army import Army

class Civilization: 
    RELATED_ARMY_CIVILIZATION: Optional[Type["Army"]] = None 

    def __init__(self, name: str) -> None:
        self.name = name
        self.armies: list["Army"] = []

    def create_army(self) -> "Army":
        if not self.RELATED_ARMY_CIVILIZATION:
            raise InvalidArmyError("Civilization must have an RELATED_ARMY_CIVILIZATION defined to create an army.")
        
        army = self.RELATED_ARMY_CIVILIZATION(civilization=self)
        self.armies.append(army)
        return army

class ChineseCivilization(Civilization):
    pass

class EnglishCivilization(Civilization):
    pass

class ByzantineCivilization(Civilization):
    pass

