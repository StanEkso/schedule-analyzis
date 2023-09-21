from shared.types.lesson import Lesson

def split_into_weeks(lessons: list[Lesson]) -> tuple[list[Lesson], list[Lesson], list[Lesson]]:
  # '1н' '2н' - и другие
  first_week = []
  second_week = []
  both_weeks = []

  for lesson in lessons:
    meta_lower = lesson['meta'].lower()
    if '1н' in meta_lower:
      first_week.append(lesson)
    elif '2н' in meta_lower:
      second_week.append(lesson)
    else:
      both_weeks.append(lesson)
  return (first_week, second_week, both_weeks)