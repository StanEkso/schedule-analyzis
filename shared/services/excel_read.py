import json
import pandas as pd
from ..types.lesson import Lesson

def read_from_excel(path = "input/1.xlsx"):
  df = pd.read_excel(path, header=None)
  df = df.drop([0, 1, 2, len(df) - 1])

  times = to_times(df)
  lessons = to_lessons(df)

  with open("lesson.json", "w+", encoding="utf8") as file:
    json.dump(lessons, file, indent=4, ensure_ascii=False)

  with open("times.json", "w+", encoding="utf8") as file:
    json.dump(times, file, indent=4, ensure_ascii=False)

  return df


def to_times(df: pd.DataFrame) -> list[str]:
  times: list[str] = []
  for i in range(2, len(df)):
    times.append(f"{df.iloc[i, 0]} {df.iloc[i, 1]}".lower())

  return times

def to_time(df: pd.DataFrame, index) -> tuple:
  return df.loc[index, 0], df.loc[index, 1]

def to_lessons(df: pd.DataFrame, course: int = 1) -> list[Lesson]:
  lessons: list[Lesson] = []
  messages: list[str] = []
  for index, row in df.iterrows():
    if index in [df.index[0], df.index[1]]:
      continue
    try:
      weekday, time = to_time(df, index)
      for i in range(len(row)):
        if i in [0, 1]:
          continue
        text = row[i]
        if isinstance(text, float):
          continue
        group = df.iloc[0, i]

        lesson = parse_lesson(text)

        lesson["group"] = map_group(str(group))
        lesson["weekday"] = str(weekday).lower()
        lesson["time"] = time
        lesson["course"] = str(course)

        lessons.append(lesson)
    except Exception as e:
      print(e)
      pass
  return lessons

def parse_lesson(source: str) -> Lesson:
  parts: list[str] = source.split("\n")
  subject = parts[0]
  teacher = parts[1]
  room = parts[2]
  lesson = {
    "subject": subject,
    "teacher":teacher,
    "room": map_room(room),
    "type": map_to_type(subject),
    "meta": extract_meta(source)
  }

  return lesson

def map_to_type(source: str) -> str:
  if "(практ)" in source:
    return "Практика"
  elif "(лаб)" in source:
    return "Практика"
  elif "(лек)" in source:
    return "Лекция"
  
  return ""

def map_room(source: str) -> str:

  res = source.replace("ауд. №", "")

  return remove_until_braces(remove_until_braces2(res))

def remove_until_braces(source: str) -> str:
  index = source.find("(")
  if index != -1:
    return source[:index].strip()
  
  return source.strip()

def remove_until_braces2(source: str) -> str:
  index = source.find("[")
  if index != -1:
    return source[:index].strip()
  
  return source.strip()


def map_group(source: str) -> str:
  if source == "Военный факультет":
    return "vf"

  return source.replace(" группа", "")

def extract_meta(source: str) -> str:
  week_num = ""
  if "нечетн" in source:
    week_num = "1н"
  elif "четн" in source:
    week_num = "2н"

  sub_group = extract_subgroup(source)

  return "-".join(el for el in [week_num, sub_group] if el != "")

def extract_subgroup(source: str) -> str:
  index = source.find("{")
  if index == -1:
    return ""

  return source[index+1:source.find("}")].replace("подгр. ", "")
