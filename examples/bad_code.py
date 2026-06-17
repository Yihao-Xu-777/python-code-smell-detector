def process_student_data(name, age, score, grade, major, year, email):
    total = 0

    for i in range(10):
        if score > 50:
            if grade == "A":
                if major == "Software Engineering":
                    if year > 1:
                        total = score * 3.14

    try:
        result = total / age
    except Exception:
        result = 0

    return result