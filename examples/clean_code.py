PASSING_SCORE = 50


def calculate_average(total_score, student_count):
    if student_count == 0:
        return 0

    return total_score / student_count


def is_passing(score):
    return score >= PASSING_SCORE