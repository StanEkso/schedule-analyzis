def create_lection_matcher(object: dict | None = None):
  copy = {}
  if (object):
    copy = object.copy()

  copy['type'] = "Лекция"
  return copy

def create_course_matcher(courses: list[str], object: dict | None = None):
  copy = {}
  if (object):
    copy = object.copy()

  copy['courses'] = courses
  return copy