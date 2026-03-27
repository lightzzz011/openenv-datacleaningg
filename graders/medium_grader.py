class MediumGrader:
    def grade(self, data):
        correct = 0
        total = 2
        if all(0 <= x <= 120 for x in data["age"]):
            correct += 1
        if all(x is not None and x >= 0 for x in data["salary"]):
            correct += 1

        return correct / total