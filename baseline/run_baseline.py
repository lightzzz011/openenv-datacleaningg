import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from openai import OpenAI

from env.environment import DataCleaningEnv
from graders.hard_grader import HardGrader

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VALID_ACTIONS = ["detect_issues", "fix_age", "fix_salary", "validate"]


def get_action(state):
    prompt = f"""
You are a data cleaning agent.

Dataset:
{state}

Choose the BEST next action from:
detect_issues, fix_age, fix_salary, validate

Return ONLY the action name.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0  
        )

        action = response.choices[0].message.content.strip().lower()

        if action not in VALID_ACTIONS:
            return "detect_issues"

        return action

    except Exception:
        return "detect_issues"

def run_llm_agent():
    env = DataCleaningEnv()
    state = env.reset()

    for _ in range(5):
        action = get_action(state)
        state, reward, done, info = env.step(action)

        if done:
            break

    result = {
        "final_state": state,
        "done": done
    }

    return HardGrader().grade(result)

def run_rule_based_agent():
    env = DataCleaningEnv()
    state = env.reset()

    actions = ["detect_issues", "fix_age", "fix_salary", "validate"]

    for action in actions:
        state, reward, done, info = env.step(action)

        if done:
            break

    result = {
        "final_state": state,
        "done": done
    }

    return HardGrader().grade(result)


def run_baseline():
    try:
        return {
            "easy": run_rule_based_agent(),
            "medium": run_rule_based_agent(),
            "hard": run_llm_agent()
        }
    except Exception:
        return {
            "easy": run_rule_based_agent(),
            "medium": run_rule_based_agent(),
            "hard": run_rule_based_agent()
        }

if __name__ == "__main__":
    result = run_baseline()
    print("Baseline Result:", result)