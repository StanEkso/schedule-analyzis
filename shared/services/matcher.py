from ..types.lesson import Lesson

matchers = [
  {
    "courses": ['1'],
    "groups": ['2', '6', '9'],
    "type": "Лекция"
  },
  {
    "courses": ['2'],
    "groups": ['2', '6', '9'],
    "type": "Лекция"
  },
  {
    "courses": ['3', '4'],
    "groups": ['2', '10', '9'],
    "type": "Лекция"
  },
  {
    "type": "Лекция",
    "subjects": ["социология", "экономика", "бжч"],
  },
  {
    "courses": ["1", "2"],
    "groups": ["4", "5"],
  },
  {
    "subjects": ["Английский язык"],
    "courses": ['1', '2'],
    "groups": ['1', '3'],
  },
    {
    "subjects": ["Английский язык"],
    "courses": ['1', '2'],
    "groups": ['2', '6'],
  },
  {
    "subjects": ["Численные методы"],
    "courses": ['4', '3'],
    "groups": ['2', '3', "9", "10"],
  },
    {
    "subjects": ["Английский язык"],
    "courses": ['1', '2'],
    "groups": ['7', '8'],
    },
    {
    "type": "Лекция",
    "courses": ['1', '2', '3', '4'],
    "groups": ['7', '8'],
  },
  {
    "subjects": ["Язык С#"],
    "groups": ["1", "6"],
  },
  {
    "subjects": ["Физическая культура"],
    "courses": ["1", "2", "3"]
  },
  {
    "courses": ["1"],
    "groups": ["1", "2", "6", "9"],
    "subjects": ["Методы программирования", "Технологии программирования"]
  }
]

def is_matching(lessons: list[Lesson]):
  for lesson in lessons:
    if not is_matches(lesson):
      return False
    
  return True

def is_matching_course(matcher: dict, lesson: Lesson):
  courses = matcher.get("courses")
  if bool(courses):
    return lesson.get("course") in courses
  
  return True

def is_matching_group(matcher: dict, lesson: Lesson):
  groups = matcher.get("groups")
  if bool(groups):
    return lesson.get("group") in groups
  
  return True

def is_matching_type(matcher: dict, lesson: Lesson):
  if bool(matcher.get("type")):
    return lesson["type"] == matcher["type"]
  return True

def is_matching_subject(matcher: dict, lesson: Lesson):
  subjects: list[str] = matcher.get("subjects")
  if not bool(subjects):
    return True
  
  for subject in subjects:
    if subject.lower() in lesson["subject"].lower():
      return True
    
  return False

def is_matches(lesson: Lesson):
  for matcher in matchers:
    if not is_matching_course(matcher, lesson):
      continue

    if not is_matching_group(matcher, lesson):
      continue

    if not is_matching_type(matcher, lesson):
      continue
    
    if not is_matching_subject(matcher, lesson):
      continue

    return True
  
  return False