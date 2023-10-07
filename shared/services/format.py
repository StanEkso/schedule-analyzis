from ..types.lesson import Lesson
import regex as re

def to_separate_course(lessons: list[Lesson], course: int) -> list[Lesson]:
  return [lesson for lesson in lessons if lesson["course"] == str(course)]

def collect_distinct_for_meta(lessons: list[Lesson]) -> list[str]:
  distinct = set()

  for lesson in lessons:
    distinct.add(to_lesson_time_with_meta(lesson))

  return sort_times(list(distinct))

def to_lesson_time_with_meta(lesson: Lesson) -> str:
  sub_groups = ['б', 'в', 'г']

  time = f"{lesson['weekday']}-{lesson['time']}"
  meta = lesson['meta']
  for sub_group in sub_groups:
    if sub_group in meta:
      time = f"{time}-{sub_group}"
  return time

def sort_times(times: list[str]):
  weekdays = {
        'понедельник': 1,
        'вторник': 2,
        'среда': 3,
        'четверг': 4,
        'пятница': 5,
        'суббота': 6
    }
  times.sort(key=lambda v: (weekdays[v.split('-')[0]], v.split('-')[1],  v.split('-')[2] if len(v.split('-')) > 2 else ''))

  return times

def collect_groups(lessons: list[Lesson]) -> list[str]:
  groups = set()

  for lesson in lessons:
    groups.add(lesson['group'])

  group_order = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'vf': 11
  }

  return sorted(list(groups), key=lambda v: group_order[v])

def create_base_schedule(times, groups):
  base: dict = {
      'День недели': [""] + times,
      'Время': [""] + times
  }
  for group in groups:
    base[group] = [""] + ["" for _ in times]
  
  return base

def fix_names(schedule):
  for i, el in enumerate(schedule['День недели']):
    if len(el.split('-')) <= 1:
      continue
    schedule['День недели'][i] = el.split('-')[0].capitalize()

  for i, el in enumerate(schedule['Время']):
    if len(el.split('-')) <= 1:
      continue
    schedule['Время'][i] = el.split('-')[1]

def fill_schedule(schedule, lessons, times):
  for lesson in lessons:
    group, position = get_lesson_position(lesson, times)
    schedule[group][position] = lesson_formatter(lesson)

def get_lesson_position(lesson: Lesson, times: list[str]):
  return lesson['group'], 1 + times.index(to_lesson_time_with_meta(lesson))

def lesson_formatter(lesson: Lesson) -> str:
  return "\n".join(el for el in [
      f"{lesson['subject']} {format_lesson_type(lesson)}",
      lesson['teacher'],
      format_room(lesson['room']),
      to_subgroup(lesson),
      to_weeknum(lesson['meta']),
      to_date_period(lesson)
    ]
    if el != '')

def format_lesson_type(lesson: Lesson) -> str:
  type = lesson['type']
  if type == 'Лекция':
    return '(лек)'
  
  if type == 'Практика':
    return '(практ)'
  
  return '(практ)'

def format_room(room: str) -> str:
  if room == '':
    return ''
  return f"ауд. №{room}"

def to_weeknum(meta: str) -> str:
  if '1н' in meta:
     return '(нечетн.)'
   
  if '2н' in meta:
      return '(четн.)'
   
  return ''

def to_subgroup(lesson: Lesson) -> str:
  is_full_group_subgroup = lesson['subject'].lower() not in ['английский язык', 'физическая культура', 'немецкий язык']

  sub_groups = ['а', 'б', 'в', 'г']

  if is_full_group_subgroup:
    for sub_group in sub_groups:
      if sub_group in lesson['meta']:
        return "{" + f"подгр. {lesson['course']}.{lesson['group']}{sub_group}" + "}"
      
  for sub_group in sub_groups:
      if sub_group in lesson['meta']:
        return "{" + f"подгр. {sub_group}" + "}"
      
  return ''
      
def to_date_period(lesson: Lesson) -> str:
  # 	Экономика (с 14.10 до 23.12) -> [14.10-23.12]
  #   Экономика (с 06.09) -> [06.09-]
  #   Экономика (до 13.12) -> [-13.12]

  # Take content between ()

  if '(' not in lesson['rawSubject'] or ')' not in lesson['rawSubject']:
    return ''
  
  index = lesson['rawSubject'].index('(')

  if index == -1:
    return ''
  
  extras = lesson['rawSubject'][index + 1:lesson['rawSubject'].index(')')]
  
  print(lesson, extras)

  if re.match(r'^(\d{2}\.\d{2})(, (\d{2}\.\d{2}))*$', extras):
    return f"[{extras}]"
  
  if re.match(r'^с (\d{2}\.\d{2}) до (\d{2}\.\d{2})$', extras):
    return f"[{extras.split(' до ')[0]}-{extras.split(' до ')[1]}]".replace('с ', '')
  
  if re.match(r'^с (\d{2}\.\d{2})$', extras):
    return f"[{extras.split('с ')[1]}-]"
  
  if re.match(r'^до (\d{2}\.\d{2})$', extras):
    return f"[-{extras.split('до ')[1]}]"

  return ''
  