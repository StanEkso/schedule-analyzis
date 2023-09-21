from shared.types.lesson import Lesson
from .split import split_into_weeks

from shared.services.matcher import is_matching

def has_conflicts(lessons: list[Lesson]) -> bool:
  first_week, second_week, both_weeks = split_into_weeks(lessons)

  if is_matching(lessons):
    return False

  if len(both_weeks) != 0 and (len(first_week) != 0 or len(second_week) != 0):
    return True

  return has_conflict_inner(first_week) or has_conflict_inner(second_week) or has_conflict_inner(both_weeks)

def has_conflict_inner(lessons: list[Lesson]) -> bool:
  for i in range(len(lessons)):
    for j in range(len(lessons)):
      if i == j:
        continue
      if has_conflict_inner_tuple(lessons[i], lessons[j]):
        return True
  return False

def has_conflict_inner_tuple(l1: Lesson, l2: Lesson) -> bool:
  if l1['course'] != l2['course']:
    return True
  
  if l1['group'] != l2['group']:
    return True
  
  if l1['meta'] != l2['meta']:
    return True
  
  return False
