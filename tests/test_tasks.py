import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tasks.easy_task import EasyTask
from tasks.medium_task import MediumTask
from tasks.hard_task import HardTask

print("\n--- EASY TASK ---")
easy = EasyTask()
print(easy.run())

print("\n--- MEDIUM TASK ---")
medium = MediumTask()
print(medium.run())

print("\n--- HARD TASK ---")
hard = HardTask()
print(hard.run())   