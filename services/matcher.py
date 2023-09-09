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
    "courses": ['3'],
    "groups": ['2', '10', '9'],
    "type": "Лекция"
  },
  {
    "courses": ['4'],
    "groups": ['2', '10', '9'],
    "type": "Лекция"
  },
  {
    "type": "Лекция",
    "subjects": ["социология", "экономика", "бжч"],
  }
]

def is_matching(lessons: list[dict]):
  for lesson in lessons:
    if not is_matches(lesson):
      return False
  return True

def is_matches(lesson: dict):
  for matcher in matchers:
    if bool(matcher.get("courses")) and not lesson["course"] in matcher["courses"]:
      continue
    if bool(matcher.get("groups")) and not lesson["group"] in matcher["groups"]:
      continue
    if bool(matcher.get("type")) and not lesson["type"] == matcher["type"]:
      continue
    if bool(matcher.get("subjects")):
      print("has subjects")
      res = False
      for subject in matcher.get("subjects"):
        if subject.lower() in lesson["subject"].lower():
          res = True
          break

      
      if not res:
        continue

    return True
  return False