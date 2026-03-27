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

        # Check age
        for val in self.data["age"]:
            total += 1
            if val is None or val < 0 or val > 120:
                issues += 1

        # Check salary
        for val in self.data["salary"]:
            total += 1
            if val is None or val < 0:
                issues += 1

        quality = 1 - (issues / total)
        return quality

    def step(self, action):
        old_quality = self.calculate_quality()

        # Apply action
        if action == "fix_age":
            self.data["age"] = [25, 25, 25]

        elif action == "fix_salary":
            self.data["salary"] = [50000, 60000, 70000]

        new_quality = self.calculate_quality()

        reward = new_quality - old_quality
        done = False

        return self.data, reward, done, {}