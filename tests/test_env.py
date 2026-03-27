import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from env.environment import DataCleaningEnv

env = DataCleaningEnv()

state = env.reset()
print("Initial State:", state)

print("Initial Quality:", env.calculate_quality())

state, reward, done, _ = env.step("fix_age")

print("After Step:", state)
print("New Quality:", env.calculate_quality())
print("Reward:", reward)