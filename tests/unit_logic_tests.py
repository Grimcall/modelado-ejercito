import unittest
import sys, os

# Add parent directory to path to import models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.unit import Pikeman, Bowman, Knight
from models.utils import UnitTransformationError

class TestUnitLogic(unittest.TestCase):
    
    def test_unit_creation(self):
        pikeman = Pikeman(age=27)

        self.assertEqual(pikeman.age, 27)
        self.assertEqual(pikeman.strength_score, Pikeman.BASE_STRENGTH_SCORE)
    
    def test_train(self):
        pikeman = Pikeman(age=27)
        times_trained = 3
        pikeman.train(times_trained)
        self.assertEqual(pikeman.strength_score, Pikeman.BASE_STRENGTH_SCORE + Pikeman.TRAINING_BONUS*times_trained)
    
    def test_full_transformation_chain(self):
        unit = Pikeman(age=27)
        
        unit.transform() 
        self.assertIsInstance(unit, Bowman)
        self.assertEqual(unit.strength_score, Bowman.BASE_STRENGTH_SCORE)
        
        unit.transform() 
        self.assertIsInstance(unit, Knight)
        self.assertEqual(unit.strength_score, Knight.BASE_STRENGTH_SCORE)
    
    def test_knight_cannot_transform(self):
        knight = Knight(age=57)
        
        with self.assertRaises(UnitTransformationError):
            knight.transform()

    def test_strength_carryover(self):
        pikeman = Pikeman(age=27)
        
        times_trained = 2
        pikeman.train(times_trained)
        str_post_training = pikeman.strength_score
        expected_strength = Pikeman.BASE_STRENGTH_SCORE + (times_trained*Pikeman.TRAINING_BONUS)
        self.assertEqual(str_post_training, expected_strength)
        
        pikeman.transform()
        
        expected_bowman_strength = expected_strength + (Bowman.BASE_STRENGTH_SCORE - Pikeman.BASE_STRENGTH_SCORE)
        self.assertEqual(pikeman.strength_score, expected_bowman_strength)
        self.assertIsInstance(pikeman, Bowman)

if __name__ == '__main__':
    unittest.main()