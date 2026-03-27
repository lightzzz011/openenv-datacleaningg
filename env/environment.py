from env.models import Action, Observation, StepResult


class DataCleaningEnv:
    def __init__(self):
        self.data = None
        self.schema = None
        self.detected = False

    def reset(self):
        self.data = {
            "age": [25, -5, None, 200],
            "salary": [50000, None, -1000, 25000],
            "experience": [2, None, 40, 30]
        }

        self.schema = {
            "age": {"type": "int", "min": 0, "max": 120},
            "salary": {"type": "int", "min": 0},
            "experience": {"type": "int", "min": 0, "max": 50}
        }

        self.detected = False
        return self.data

    def calculate_quality(self):
        total = 0
        issues = 0

        # -------- BASIC SCHEMA CHECKS --------
        for col, rules in self.schema.items():
            for val in self.data[col]:
                total += 1

                if val is None:
                    issues += 1
                    continue

                if "min" in rules and val < rules["min"]:
                    issues += 1

                if "max" in rules and val > rules["max"]:
                    issues += 1

        # -------- DEPENDENCY CHECKS --------
        for i in range(len(self.data["age"])):
            age = self.data["age"][i]
            exp = self.data["experience"][i]
            salary = self.data["salary"][i]

            if age is None or exp is None:
                continue

            # experience must be <= working years
            if exp > (age - 18):
                issues += 1

            # salary vs experience logic
            if salary is not None:
                if exp < 2 and salary > 30000:
                    issues += 1
                if exp > 10 and salary < 30000:
                    issues += 1

        return 1 - (issues / total)

    def step(self, action: Action) -> StepResult:
        if self.data is None:
            self.reset()

        action = action.action
        old_quality = self.calculate_quality()
        info = {}

        # ---------------- DETECT ----------------
        if action == "detect_issues":
            if self.detected:
                reward = -0.2
                info["issues"] = []
            else:
                issues = []

                # schema issues
                for col, rules in self.schema.items():
                    for i, val in enumerate(self.data[col]):
                        if val is None:
                            issues.append(f"{col} missing at index {i}")
                        elif "min" in rules and val < rules["min"]:
                            issues.append(f"{col} below range at index {i}")
                        elif "max" in rules and val > rules["max"]:
                            issues.append(f"{col} above range at index {i}")

                # dependency issues
                for i in range(len(self.data["age"])):
                    age = self.data["age"][i]
                    exp = self.data["experience"][i]
                    salary = self.data["salary"][i]

                    if age is not None and exp is not None:
                        if exp > (age - 18):
                            issues.append(f"experience invalid wrt age at index {i}")

                    if exp is not None and salary is not None:
                        if exp < 2 and salary > 30000:
                            issues.append(f"salary too high for low experience at index {i}")
                        if exp > 10 and salary < 30000:
                            issues.append(f"salary too low for high experience at index {i}")

                info["issues"] = issues
                reward = 0.1 if issues else -0.1
                self.detected = True

        # ---------------- FIX AGE ----------------
        elif action == "fix_age":
            valid = [x for x in self.data["age"] if x is not None and 0 <= x <= 120]
            median = sorted(valid)[len(valid)//2] if valid else 25

            self.data["age"] = [
                median if (x is None or x < 0 or x > 120) else x
                for x in self.data["age"]
            ]
            reward = 0

        # ---------------- FIX SALARY ----------------
        elif action == "fix_salary":
            valid = [x for x in self.data["salary"] if x is not None and x >= 0]
            mean = sum(valid) / len(valid) if valid else 50000

            self.data["salary"] = [
                int(mean) if (x is None or x < 0) else x
                for x in self.data["salary"]
            ]
            reward = 0

        # ---------------- FIX EXPERIENCE ----------------
        elif action == "fix_experience":
            new_exp = []
            for i, x in enumerate(self.data["experience"]):
                age = self.data["age"][i]

                if x is None or x < 0:
                    val = 5
                else:
                    val = x

                # clamp based on age dependency
                if age is not None:
                    val = min(val, age - 18)

                new_exp.append(int(val))

            self.data["experience"] = new_exp
            reward = 0

        # ---------------- VALIDATE ----------------
        elif action == "validate":
            reward = 0.2 if self.calculate_quality() > 0.9 else -0.2

        else:
            reward = -0.2

        # -------- REWARD UPDATE --------
        new_quality = self.calculate_quality()
        reward += (new_quality - old_quality)

        if action in ["fix_age", "fix_salary", "fix_experience"] and new_quality == old_quality:
            reward -= 0.1

        reward -= 0.01

        done = new_quality > 0.95

        return StepResult(
            observation=Observation(data=self.data),
            reward=reward,
            done=done,
            info=info
        )