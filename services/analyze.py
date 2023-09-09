from .common import lesson_times, rooms, lesson_to_time, convert_lesson_to_str
from .matcher import is_matching

def collectRooms(lessons: list[dict]):
  rooms = set()
  for lesson in lessons:
    rooms.add(lesson.get("room"))
  
  return rooms


class Item:
  day: str
  time: str

  def __init__(self, day, time) -> None:
    self.day = day
    self.time = time
    pass

  def __repr__(self) -> str:
    return f"'{self.day} {self.time}'"
  
  def __eq__(self, other):
        if isinstance(other, Item):
            return ((self.day == other.day) and (self.time == other.time))
        else:
            return False
  def __ne__(self, other):
        return (not self.__eq__(other))

  def __hash__(self) -> int:
    return hash(self.__repr__())


def collectTimes(lessons: list[dict]):
  times = set()
  for lesson in lessons:
    times.add(Item(lesson.get("weekday"), lesson.get("time")))

  return times

def create_base_object():
  base: dict = {
      'Время\Аудитории': lesson_times
  }
  for room in rooms:
    base[room] = [[] for _ in lesson_times]
  
  return base

def fill_data(lessons: list[dict], object):
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
       pass
    

def check_data(object):
  for room in rooms:
      object[room] = [to_item_string(v) for v in object[room]]
      continue


def to_item_string(lessons: list[dict]):
  mStr = ":".join([convert_lesson_to_str(v) for v in lessons])
  if (has_conflict(lessons)):
      return "Конфликт: " + mStr
  return mStr
          
               


def has_conflict(lessons: list[dict]) -> bool:
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