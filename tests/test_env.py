import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from env.environment import DataCleaningEnv

env = DataCleaningEnv()

state = env.reset()
print("Initial State:", state)

print("\n--- Detecting Issues ---")
state, reward, done, info = env.step("detect_issues")
print("Issues:", info.get("issues"))
print("Reward:", reward)

print("\n--- Fix Age ---")
state, reward, done, _ = env.step("fix_age")
print("Reward:", reward)

print("\n--- Fix Salary ---")
state, reward, done, _ = env.step("fix_salary")
print("Reward:", reward)

print("\n--- Validate ---")
state, reward, done, _ = env.step("validate")
print("Final Reward:", reward)
print("Done:", done)