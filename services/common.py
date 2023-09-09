lesson_times = [
  "понедельник 08:15–09:35",
  "понедельник 09:45–11:05",
  "понедельник 11:15–12:35",
  "понедельник 13:00–14:20",
  "понедельник 14:30–15:50",
  "понедельник 16:00–17:20",
  "понедельник 17:40–19:00",
  "понедельник 19:10–20:30",
  "",
  "вторник 08:15–09:35",
  "вторник 09:45–11:05",
  "вторник 11:15–12:35",
  "вторник 13:00–14:20",
  "вторник 14:30–15:50",
  "вторник 16:00–17:20",
  "вторник 17:40–19:00",
  "вторник 19:10–20:30",
  "",
  "среда 08:15–09:35",
  "среда 09:45–11:05",
  "среда 11:15–12:35",
  "среда 13:00–14:20",
  "среда 14:30–15:50",
  "среда 16:00–17:20",
  "среда 17:40–19:00",
  "среда 19:10–20:30",
  "",
  "четверг 08:15–09:35",
  "четверг 09:45–11:05",
  "четверг 11:15–12:35",
  "четверг 13:00–14:20",
  "четверг 14:30–15:50",
  "четверг 16:00–17:20",
  "четверг 17:40–19:00",
  "четверг 19:10–20:30",
  "",
  "пятница 08:15–09:35",
  "пятница 09:45–11:05",
  "пятница 11:15–12:35",
  "пятница 13:00–14:20",
  "пятница 14:30–15:50",
  "пятница 16:00–17:20",
  "пятница 17:40–19:00",
  "пятница 19:10–20:30",
  "",
  "суббота 08:15–09:35",
  "суббота 09:45–11:05",
  "суббота 11:15–12:35",
  "суббота 13:00–14:20",
  "суббота 14:30–15:50",
  "суббота 16:00–17:20",
  "суббота 17:40–19:00",
  "суббота 19:10–20:30",
]

rooms = [
    "410",
    "403",
    "404",
    "405",
    "407",
    "408",
    "409",
    "402а",
    "417",
    "330",
    "332",
    "334",
    "337",
    "338",
    "339",
    "340",
    "341",
    "342",
    "344",
    "345",
    "346",
    "347",
    "348",
    "349",
    "351",
    "353",
    "355",
    "120",
    "606",
    "609",
    "237",
    "239",
    "230",
    "238",
    "247",
    ""
]

def lesson_to_time(lesson: dict):
  return f"{lesson.get('weekday')} {lesson.get('time')}"

def convert_lesson_to_str(lesson: dict) -> str:
    meta = "-".join(lesson['meta'].split())
    if len(meta) != 0:
       meta = "-" + meta
    return f"{lesson['course']}-{lesson['group']}{meta} {lesson['teacher']} {lesson['subject']} {lesson['type']}"