import unittest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.army import ChineseArmy, EnglishArmy, ByzantineArmy
from models.civilization import ChineseCivilization, EnglishCivilization, ByzantineCivilization
from models.unit import Pikeman, Bowman, Knight
from models.utils import InsufficientFundsError, UnitTransformationError

class TestArmyCreation(unittest.TestCase):
    
    def test_chinese_army_creation(self):
        chinese_civ = ChineseCivilization(name="China")
        army = chinese_civ.create_army()
        
        self.assertEqual(sum(1 for u in army.units if isinstance(u, Pikeman)), 2)
        self.assertEqual(sum(1 for u in army.units if isinstance(u, Bowman)), 25)
        self.assertEqual(sum(1 for u in army.units if isinstance(u, Knight)), 2)
        self.assertEqual(army.gold, 1000)

    def test_english_army_creation(self):
        english_civ = EnglishCivilization(name="England")
        army = english_civ.create_army()
        
        self.assertEqual(sum(1 for u in army.units if isinstance(u, Pikeman)), 10)
        self.assertEqual(sum(1 for u in army.units if isinstance(u, Bowman)), 10)
        self.assertEqual(sum(1 for u in army.units if isinstance(u, Knight)), 10)
        self.assertEqual(army.gold, 1000)

    def test_byzantine_army_creation(self):
        byzantine_civ = ByzantineCivilization(name="Byzantines")
        army = byzantine_civ.create_army()
        
        self.assertEqual(sum(1 for u in army.units if isinstance(u, Pikeman)), 5)
        self.assertEqual(sum(1 for u in army.units if isinstance(u, Bowman)), 8)
        self.assertEqual(sum(1 for u in army.units if isinstance(u, Knight)), 15)
        self.assertEqual(army.gold, 1000)

    def test_create_two_different_armies_and_battle(self):
        english_civ = EnglishCivilization(name="England")
        chinese_civ = ChineseCivilization(name="China")

        army1 = english_civ.create_army()
        army2 = chinese_civ.create_army()
        
        initial_units_army1 = len(army1.units)
        initial_units_army2 = len(army2.units)

        strongest_units_army2 = sorted(army2.units, key=lambda u: u.strength_score, reverse=True)[:2]

        # train army1 to make it stronger
        army1.train_unit(army1.units[0], times_trained=2)
        new_army1_gold = army1.gold
        army1.attack(army2)
        
        # check logs.
        self.assertIn("Won", army1.battle_log[-1])
        self.assertIn("Lost", army2.battle_log[-1])

        # check that army 1 still has all its units
        self.assertEqual(len(army1.units), initial_units_army1)

        # check that army 1 won gold.
        self.assertEqual(army1.gold, new_army1_gold + 100)
        
        # check that army 2 lost two strongest units
        self.assertEqual(len(army2.units), initial_units_army2 - 2)
        self.assertEqual(strongest_units_army2[0] not in army2.units, True)
        self.assertEqual(strongest_units_army2[1] not in army2.units, True)
    
    def test_battle_tie(self):
        byzantine_civ = ByzantineCivilization(name="Byzantines")

        army1 = byzantine_civ.create_army()
        army2 = byzantine_civ.create_army()

        strongest_unit_army1 = max(army1.units, key=lambda u: u.strength_score).strength_score
        strongest_unit_army2 = max(army2.units, key=lambda u: u.strength_score).strength_score
        
        army1.attack(army2)
        
        self.assertNotIn(strongest_unit_army1, army1.units)
        self.assertNotIn(strongest_unit_army2, army2.units)

    def test_army_with_no_units_attacks(self):
        chinese_civ = ChineseCivilization(name="China")
        english_civ = EnglishCivilization(name="England")

        army1 = chinese_civ.create_army()
        army2 = english_civ.create_army()
        initial_units_army2 = len(army2.units)

        army1.units = []

        army1.attack(army2)

        self.assertIn("Army has no units to attack.", army1.battle_log[-1])
        self.assertEqual(len(army2.units), initial_units_army2) 
    
    def test_army_loses(self):
        chinese_civ = ChineseCivilization(name="China")
        english_civ = EnglishCivilization(name="England")

        army1 = chinese_civ.create_army()
        army2 = english_civ.create_army()
        initial_units_army1 = len(army1.units)

        army1.attack(army2)
        self.assertEqual(len(army1.units), initial_units_army1 - 2)

    def test_army_with_remaining_two_units_becomes_zero(self):
        english_civ = EnglishCivilization(name="England")
        chinese_civ = ChineseCivilization(name="China")

        army1 = english_civ.create_army()
        army2 = chinese_civ.create_army()

        army2.units = army2.units[:2]  # leave only two units

        army1.attack(army2)
        self.assertEqual(len(army2.units), 0)

    def test_train_insufficient_funds(self):
        english_civ = EnglishCivilization(name="England")
        army = english_civ.create_army()

        army.gold = 10  

        with self.assertRaises(InsufficientFundsError):
            army.train_unit(army.units[0], times_trained=3)
    
    def test_transform_insufficient_funds(self):
        chinese_civ = ChineseCivilization(name="China")
        army = chinese_civ.create_army()

        army.gold = 5  

        with self.assertRaises(InsufficientFundsError):
            army.transform_unit(army.units[0])


if __name__ == '__main__':
    unittest.main()