from fastapi import FastAPI
from env.environment import DataCleaningEnv

from tasks.easy_task import EasyTask
from tasks.medium_task import MediumTask
from tasks.hard_task import HardTask
from pydantic import BaseModel
from graders.easy_grader import EasyGrader
from graders.medium_grader import MediumGrader
from graders.hard_grader import HardGrader

app = FastAPI()

env = DataCleaningEnv()
class ActionRequest(BaseModel):
    action: str

@app.get("/reset")
def reset():
    state = env.reset()
    return {"state": state}


@app.post("/step")
def step(request: ActionRequest):
    state, reward, done, info = env.step(request.action)
    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }


@app.get("/state")
def get_state():
    return {"state": env.data}


@app.get("/tasks")
def get_tasks():
    return {
        "tasks": ["easy", "medium", "hard"],
        "actions": ["detect_issues", "fix_age", "fix_salary", "validate"]
    }


@app.get("/grader/{level}")
def grade(level: str):
    if level == "easy":
        result = EasyTask().run()
        score = EasyGrader().grade(result["issues"])

    elif level == "medium":
        result = MediumTask().run()
        score = MediumGrader().grade(result)

    elif level == "hard":
        result = HardTask().run()
        score = HardGrader().grade(result)

    else:
        return {"error": "invalid level"}

    return {"score": score} 