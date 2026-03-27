import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from env.environment import DataCleaningEnv
from env.models import Action

env = DataCleaningEnv()

print("Initial State:", env.reset())

print("\n--- Detecting Issues ---")
result = env.step(Action(action="detect_issues"))
print("Issues:", result.info["issues"])
print("Reward:", result.reward)

print("\n--- Fix Age ---")
result = env.step(Action(action="fix_age"))
print("Reward:", result.reward)

print("\n--- Fix Salary ---")
result = env.step(Action(action="fix_salary"))
print("Reward:", result.reward)

print("\n--- Fix Experience ---")
result = env.step(Action(action="fix_experience"))
print("Reward:", result.reward)

print("\n--- Validate ---")
result = env.step(Action(action="validate"))
print("Final Reward:", result.reward)
print("Done:", result.done)