from .common import lesson_times, rooms, lesson_to_time, convert_lesson_to_str, lesson_separator
from .matcher import is_matching, is_required
from ..types.lesson import Lesson
from shared.analyze import has_conflicts
def collectRooms(lessons: list[Lesson]):
  rooms = set()
  for lesson in lessons:
    rooms.add(lesson.get("room"))
  
  return rooms

def collectTimes(lessons: list[Lesson]):
  times = set()
  for lesson in lessons:
    times.add(f"{lesson['course']}-{lesson['group']}")

  return times

def create_base_object(times = lesson_times):
  base: dict = {
      'Время\Аудитории': times
  }
  for room in rooms:
    base[room] = [[] for _ in times]
  
  return base

def fill_data(lessons: list[Lesson], object, times = lesson_times):
  for lesson in lessons:
    try:
      room = lesson.get("room")
      time_index = times.index(lesson_to_time(lesson))
      length = len(object[room][time_index])

      if length == 0:
         object[room][time_index] = [lesson]
      else:
        lessonList: list = object[room][time_index]
        lessonList.append(lesson)
        object[room][time_index] = lessonList
    except Exception as excp:
       print(excp)
       pass
    

def check_data(object: dict):
  for room in rooms:
    object[room] = [to_item_string(v) for v in object[room]]
    continue


DIFFERENT_WEEKS_KEY = "t-dw/"
MATCHING_KEY = "t-mg/"
INFORMATION_HOUR_KEY = "t-ih/"

def to_item_string(lessons: list[Lesson]):
  mStr = lesson_separator.join([convert_lesson_to_str(v) for v in lessons])
  if (has_conflicts(lessons)):
    return "Конфликт: " + mStr
  
  # Some lesson from lessons is information hour
  if any(['Информационный час'.lower() in v['subject'].lower() for v in lessons]):
    return INFORMATION_HOUR_KEY + mStr
  
  # if len(first_week) > 0 and len(second_week) > 0:
  #   return DIFFERENT_WEEKS_KEY + mStr

  return mStr

def split_into_weeks(lessons: list[Lesson]):
  first_week: list[Lesson] = []
  second_week: list[Lesson] = []
  others: list[Lesson] = []

  for lesson in lessons:
    if '1н' in lesson['meta']:
      first_week.append(lesson)
      continue

    if '2н' in lesson['meta']:
      second_week.append(lesson)
      continue

    others.append(lesson)

  return first_week, second_week, others

def conflicting(lessons: list[Lesson]) -> bool:
  first_week, second_week, others = split_into_weeks(lessons)

  if (len(first_week) > 0 or len(second_week) > 0) and len(others) > 0:
    return True
  
  if has_conflict(first_week):
    return True
  
  if has_conflict(second_week):
    return True
  
  if has_conflict(others):
    return True
  
  return False

def has_conflict(lessons: list[Lesson]) -> bool:
  if (len(lessons) <= 1):
     return False
  if is_matching(lessons):
     return False
  current: str = "INITIAL-VALUE"
  for lesson in lessons:
    if current == lesson['meta']:
        return True
    current = lesson['meta']
  return False

def filter_lessons(lessons: list[Lesson]) -> list[Lesson]:
  matching: list[Lesson] = []
  for lesson in lessons:
    if is_required(lesson):
      matching.append(lesson)

  return matching
