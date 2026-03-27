from env.environment import DataCleaningEnv

class MediumTask:
    def __init__(self):
        self.env = DataCleaningEnv()

    def run(self):
        self.env.reset()

        self.env.step("detect_issues")
        self.env.step("fix_age")
        self.env.step("fix_salary")

        return self.env.data