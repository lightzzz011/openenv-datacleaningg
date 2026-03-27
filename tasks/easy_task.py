from env.environment import DataCleaningEnv

class EasyTask:
    def __init__(self):
        self.env = DataCleaningEnv()

    def run(self):
        state = self.env.reset()

        state, reward, done, info = self.env.step("detect_issues")

        return info