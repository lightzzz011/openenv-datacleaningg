class DataCleaningEnv:
    def __init__(self):
        self.data = None

    def reset(self):
        self.data = {
            "age": [25, -5, None, 200],
            "salary": [50000, None, -1000, 70000]
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
            valid_ages = [x for x in self.data["age"] if x is not None and 0 <= x <= 120]

            if valid_ages:
                median = sorted(valid_ages)[len(valid_ages)//2]
            else:
                median = 25

            self.data["age"] = [
                median if (x is None or x < 0 or x > 120) else x
                for x in self.data["age"]
            ]

            reward = 0

        elif action == "fix_salary":
            valid_salaries = [x for x in self.data["salary"] if x is not None and x >= 0]

            if valid_salaries:
                mean = sum(valid_salaries) / len(valid_salaries)
            else:
                mean = 50000

            self.data["salary"] = [
                int(mean) if (x is None or x < 0) else x
                for x in self.data["salary"]
            ]

            reward = 0

        elif action == "validate":
            reward = 0.2 if self.calculate_quality() > 0.9 else -0.2

        else:
            reward = -0.2

        new_quality = self.calculate_quality()
        reward += (new_quality - old_quality)

        if action in ["fix_age", "fix_salary"] and new_quality == old_quality:
            reward -= 0.1

        done = new_quality > 0.95

        return self.data, reward, done, info