from .models import Test


def check_test_results(user, answers: dict, test_id: int) -> dict:
    """
    answers = {
        '1': [5],       # SINGLE/MULTIPLE: список ID ответов
        '2': "Текст..." # TEXT: строковый ответ
    }
    """
    from .models import Question, TextAnswer

    questions = Question.objects.filter(test_id=test_id).prefetch_related('answers')
    total = questions.count()
    correct = 0
    details = {}

    for q in questions:
        user_answer = answers.get(str(q.id))

        if q.type == 'TEXT':
            # Сохраняем текстовый ответ для ручной проверки
            TextAnswer.objects.create(
                question=q,
                user=user,
                answer_text=user_answer or ""
            )
            details[q.id] = {'type': 'text', 'status': 'pending'}
            continue

        # Для вопросов с выбором ответа
        correct_answers = set(q.answers.filter(is_correct=True).values_list('id', flat=True))
        user_answers = set(map(int, user_answer or []))

        is_correct = (
            user_answers == correct_answers
            if q.type == 'MULTIPLE'
            else len(user_answers) == 1 and user_answers.issubset(correct_answers)
        )

        details[q.id] = {
            'type': q.type.lower(),
            'is_correct': is_correct,
            'correct_answers': list(correct_answers)
        }
        correct += int(is_correct)

    score = round(correct / total * 100) if total > 0 else 0
    test_passed = score >= Test.objects.get(id=test_id).pass_score

    return {
        'score': score,
        'passed': test_passed,
        'correct': correct,
        'total': total,
        'details': details
    }