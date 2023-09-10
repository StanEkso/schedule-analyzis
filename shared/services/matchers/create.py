def create_lecture_matcher(object: dict | None = None):
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

def create_group_matcher(groups: list[str], object: dict | None = None):
  copy = {}
  if (object):
    copy = object.copy()

  copy['groups'] = groups
  return copy

def create_subject_matcher(subjects: list[str], object: dict | None = None):
  copy = {}
  if (object):
    copy = object.copy()

  copy['subjects'] = subjects
  return copy
