import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tasks.easy_task import EasyTask
from tasks.medium_task import MediumTask
from tasks.hard_task import HardTask

from graders.easy_grader import EasyGrader
from graders.medium_grader import MediumGrader
from graders.hard_grader import HardGrader


def run_baseline():
    results = {}

    # EASY
    easy_task = EasyTask()
    easy_result = easy_task.run()
    easy_score = EasyGrader().grade(easy_result["issues"])
    results["easy"] = easy_score

    # MEDIUM
    medium_task = MediumTask()
    medium_result = medium_task.run()
    medium_score = MediumGrader().grade(medium_result)
    results["medium"] = medium_score

    # HARD
    hard_task = HardTask()
    hard_result = hard_task.run()
    hard_score = HardGrader().grade(hard_result)
    results["hard"] = hard_score

    return results


if __name__ == "__main__":
    print(run_baseline())