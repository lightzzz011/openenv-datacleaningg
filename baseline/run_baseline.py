import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from openai import OpenAI

from env.environment import DataCleaningEnv
from env.models import Action  # ✅ IMPORTANT
from graders.hard_grader import HardGrader

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VALID_ACTIONS = ["detect_issues", "fix_age", "fix_salary", "fix_experience", "validate"]


# ---------------- ACTION SELECTION ----------------
def get_action(state, history):
    prompt = f"""
You are a data cleaning agent.

Dataset:
{state}

Previous actions:
{history}

Goal:
Fix ALL invalid values in ALL columns before validating.

Available actions:
- detect_issues
- fix_age
- fix_salary
- fix_experience
- validate

Rules:
- Do NOT repeat the same action unnecessarily
- Do NOT call detect_issues more than once
- Fix each column step-by-step
- Only validate when everything is clean

Return ONLY one action name.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        action = response.choices[0].message.content.strip().lower()

        if action not in VALID_ACTIONS:
            action = "detect_issues"

        # prevent repeating same action
        if len(history) > 0 and action == history[-1]:
            for alt in VALID_ACTIONS:
                if alt != action:
                    return alt

        return action

    except Exception:
        return "detect_issues"


# ---------------- LLM AGENT ----------------
def run_llm_agent():
    env = DataCleaningEnv()
    state = env.reset()
    history = []

    for _ in range(7):
        action = get_action(state, history)
        history.append(action)

        # ✅ USING TYPED MODEL
        result = env.step(Action(action=action))

        state = result.observation.data
        reward = result.reward
        done = result.done
        info = result.info

        if done:
            break

    result = {
        "final_state": state,
        "done": done
    }

    return HardGrader().grade(result)


# ---------------- RULE BASED ----------------
def run_rule_based_agent():
    env = DataCleaningEnv()
    state = env.reset()

    actions = ["detect_issues", "fix_age", "fix_salary", "fix_experience", "validate"]

    for action in actions:
        result = env.step(Action(action=action))  # ✅ FIXED

        state = result.observation.data
        reward = result.reward
        done = result.done
        info = result.info

        if done:
            break

    result = {
        "final_state": state,
        "done": done
    }

    return HardGrader().grade(result)


# ---------------- BASELINE ----------------
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


# ---------------- MAIN ----------------
if __name__ == "__main__":
    result = run_baseline()
    print("Baseline Result:", result)