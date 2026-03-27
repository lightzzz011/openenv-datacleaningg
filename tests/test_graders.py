import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tasks.easy_task import EasyTask
from tasks.medium_task import MediumTask
from tasks.hard_task import HardTask

from graders.easy_grader import EasyGrader
from graders.medium_grader import MediumGrader
from graders.hard_grader import HardGrader

print("\n--- EASY GRADER ---")
easy_task = EasyTask()
easy_result = easy_task.run()
print(EasyGrader().grade(easy_result["issues"]))

print("\n--- MEDIUM GRADER ---")
medium_task = MediumTask()
medium_result = medium_task.run()
print(MediumGrader().grade(medium_result))

print("\n--- HARD GRADER ---")
hard_task = HardTask()
hard_result = hard_task.run()
print(HardGrader().grade(hard_result))