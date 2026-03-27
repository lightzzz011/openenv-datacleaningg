class DataCleaningEnv:
    def __init__(self):
        self.data = None

    def reset(self):
        self.data = {
            "age": [25, -5, None],
            "salary": [50000, None, 70000]
        }
        return self.data

    def calculate_quality(self):
        total = 0
        issues = 0

        for val in self.data["age"]:
            total += 1
            if val is None or val < 0 or val > 120:
                issues += 1

        for val in self.data["salary"]:
            total += 1
            if val is None or val < 0:
                issues += 1

        return 1 - (issues / total)

    def step(self, action):
        if self.data is None:
            self.reset()
        old_quality = self.calculate_quality()
        info = {}

        if action == "detect_issues":
            issues = []

            for i, val in enumerate(self.data["age"]):
                if val is None or val < 0 or val > 120:
                    issues.append(f"age issue at index {i}")

            for i, val in enumerate(self.data["salary"]):
                if val is None or val < 0:
                    issues.append(f"salary issue at index {i}")

            info["issues"] = issues
            reward = 0.1 if issues else -0.1

        elif action == "fix_age":
            self.data["age"] = [25, 25, 25]
            reward = 0

        elif action == "fix_salary":
            self.data["salary"] = [50000, 60000, 70000]
            reward = 0

        elif action == "validate":
            reward = 0.2 if self.calculate_quality() > 0.9 else -0.2

        else:
            reward = -0.2

        new_quality = self.calculate_quality()
        reward += (new_quality - old_quality)

        done = new_quality > 0.95

        return self.data, reward, done, info