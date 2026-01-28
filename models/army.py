from typing import TYPE_CHECKING, Optional
    
if TYPE_CHECKING:
    from .civilization import Civilization

from .unit import Unit, Pikeman, Bowman, Knight
from .utils import InsufficientFundsError, UnitTransformationError

class Army:
    PIKEMEN: int
    BOWMEN: int
    KNIGHTS: int
    BASE_GOLD: int = 1000

    def __init__(self, 
                civilization: "Civilization",
                battle_log: Optional[list[str]] = None
                ) -> None:

        self.civilization = civilization
        self.gold = self.BASE_GOLD
        self.battle_log: list[str] = battle_log if battle_log is not None else []
        self.units: list[Unit] = self._build_army()
    
    def _build_army(self) -> list[Unit]:
        units: list[Unit] = []

        units += [Pikeman() for _ in range(self.PIKEMEN)]
        units += [Bowman() for _ in range(self.BOWMEN)]
        units += [Knight() for _ in range(self.KNIGHTS)]

        return units
    
    def attack(self, defending_army: "Army") -> None:
        if not self.units:
            self.log_battle_result("Army has no units to attack.")
            return
        
        attacking_army_STR = self.get_accumulated_strength()
        defending_army_STR = defending_army.get_accumulated_strength()
        
        # attacker wins.
        if attacking_army_STR > defending_army_STR:
            self.win_battle(defending_army_STR)
            defending_army.lose_battle(attacking_army_STR)
        
        # defender wins
        elif defending_army_STR > attacking_army_STR:
            self.lose_battle(defending_army_STR)
            defending_army.win_battle(attacking_army_STR)

        # tie.
        else:
            self.tie()
            defending_army.tie()

    def win_battle(self, opponent_strength: int) -> None:
        self.gold += 100
        self.log_battle_result(f"Won battle: {self.get_accumulated_strength()}pts vs. Opponent Army ({opponent_strength}pts)")
        
    def lose_battle(self, opponent_strength: int) -> None:
        # edge case for when army has less than 2 units - kill all
        if len(self.units) <= 2:
            self.units = []
            self.log_battle_result(f"Lost battle: 0pts vs. Opponent Army ({opponent_strength}pts)")
            return
        
        # else lose the two strongest units.
        self.units.sort(key=lambda unit: unit.strength_score, reverse=True)
        self.units = self.units[2:]
        self.log_battle_result(f"Lost battle: {self.get_accumulated_strength()}pts vs. Opponent Army ({opponent_strength}pts)")

    # both lose strongest unit.
    def tie(self) -> None:
        # edge case for when army has no units
        if not self.units:
            self.log_battle_result("Tied battle: No units left in army.")
            return
        
        self.units.sort(key=lambda unit: unit.strength_score, reverse=True)
        self.units = self.units[1:]

        self.log_battle_result(f"Tied battle: {self.get_accumulated_strength()}pts in both armies.")

    def log_battle_result(self, result:str) -> None:
        self.battle_log.append(result)

    def train_unit(self, unit: Unit, times_trained: int = 1) -> None:
        total_cost = unit.TRAINING_GOLD_COST * times_trained

        if self.gold < total_cost:
            raise InsufficientFundsError("Not enough gold to train unit.")
        
        unit.train(times_trained)
        self.gold -= total_cost
    
    def transform_unit(self, unit: Unit) -> Unit:
        if not unit.TRANSFORMS_INTO:
            raise UnitTransformationError("This unit cannot be transformed.")
        
        total_cost = unit.TRANSFORMS_INTO.gold_cost

        if self.gold < total_cost:
            raise InsufficientFundsError("Not enough gold to transform unit.")
        
        unit.transform()
        self.gold -= total_cost
        return unit
    
    def get_accumulated_strength(self) -> int:
        return sum(unit.strength_score for unit in self.units)

class ChineseArmy(Army):
    PIKEMEN = 2
    BOWMEN = 25
    KNIGHTS = 2

class EnglishArmy(Army):
    PIKEMEN = 10
    BOWMEN = 10
    KNIGHTS = 10

class ByzantineArmy(Army):
    PIKEMEN = 5
    BOWMEN = 8
    KNIGHTS = 15

from .civilization import ChineseCivilization, EnglishCivilization, ByzantineCivilization
ChineseCivilization.RELATED_ARMY_CIVILIZATION = ChineseArmy
EnglishCivilization.RELATED_ARMY_CIVILIZATION = EnglishArmy
ByzantineCivilization.RELATED_ARMY_CIVILIZATION = ByzantineArmy