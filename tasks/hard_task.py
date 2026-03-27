from env.environment import DataCleaningEnv

class HardTask:
    def __init__(self):
        self.env = DataCleaningEnv()

    def run(self):
        self.env.reset()

        self.env.step("detect_issues")
        self.env.step("fix_age")
        self.env.step("fix_salary")
        state, reward, done, _ = self.env.step("validate")

        return {
            "final_state": state,
            "reward": reward,
            "done": done
        }