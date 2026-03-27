class HardGrader:
    def calculate_quality(self, data):
        total = 0
        issues = 0

        for val in data["age"]:
            total += 1
            if val is None or val < 0 or val > 120:
                issues += 1

        for val in data["salary"]:
            total += 1
            if val is None or val < 0:
                issues += 1

        return 1 - (issues / total)

    def grade(self, result):
        data = result["final_state"]

        quality = self.calculate_quality(data)

        if not result["done"]:
            quality *= 0.8

        return quality