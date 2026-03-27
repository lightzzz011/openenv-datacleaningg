class EasyGrader:
    def grade(self, detected_issues):
        total_expected = 3  # we know dataset issues are 3 dudeee haha remember this : (

        correct = len(detected_issues)

        score = correct / total_expected
        return min(score, 1.0)