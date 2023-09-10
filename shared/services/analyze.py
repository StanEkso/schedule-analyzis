from .common import lesson_times, rooms, lesson_to_time, convert_lesson_to_str, lesson_separator
from .matcher import is_matching
from ..types.lesson import Lesson

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

def create_base_object():
  base: dict = {
      'Время\Аудитории': lesson_times
  }
  for room in rooms:
    base[room] = [[] for _ in lesson_times]
  
  return base

def fill_data(lessons: list[Lesson], object):
  for lesson in lessons:
    try:
      room = lesson.get("room")
      time_index = lesson_times.index(lesson_to_time(lesson))
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


def to_item_string(lessons: list[Lesson]):
  mStr = lesson_separator.join([convert_lesson_to_str(v) for v in lessons])
  if (has_conflict(lessons)):
    return "Конфликт: " + mStr
  return mStr


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

def extract_meta(lesson: str):
  try:
    index = lesson.index("н")
    return lesson[index-1:index]
  except:
    return 'every'