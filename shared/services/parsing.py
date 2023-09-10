
import time
import requests

from bs4 import BeautifulSoup
import aiohttp

from ..types.lesson import Lesson

class ParserService:
    async def parse_lessons(self, url: str) -> list:
        course, group = ParserService.extract_course_group(url)

        print(url)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, features="html.parser")

                time = soup.find_all('td', {'class': 'time'})
                remarks = soup.find_all('td', {"class": "remarks"})
                subjectAndTeacher = soup.find_all(
                    'td', {"class": "subject-teachers"})
                lessonType = soup.find_all('td', {'class': 'lecture-practice'})
                room = soup.find_all('td', {'class': 'room'})
                weekday = soup.find_all('td', {'class': 'weekday'})


                result = [self.map_tuple_to_lesson(i, course, group) for i in zip(time, remarks, subjectAndTeacher, lessonType, room, weekday)]
                if len(result) == 0:
                    print(f"Error with loading {course}-{group}")
                    with open(f"pages/{course}-{group}.html", "w+", encoding="utf-8") as file:
                        file.write(text)
                return result
            
    def parse_lessons_sync(self, url: str) -> list[Lesson]:
        """
        Deprecated (Synchronous)
        """

        print(f"Parsing {url}")

        text = requests.get(url).text

        course, group = ParserService.extract_course_group(url)
        soup = BeautifulSoup(text, features="html.parser")

        time_cells = soup.find_all('td', {'class': 'time'})
        remarks = soup.find_all('td', {"class": "remarks"})
        subjectAndTeacher = soup.find_all('td', {"class": "subject-teachers"})
        lessonType = soup.find_all('td', {'class': 'lecture-practice'})
        room = soup.find_all('td', {'class': 'room'})
        weekday = soup.find_all('td', {'class': 'weekday'})
        result = [self.map_tuple_to_lesson(i, course, group) for i in zip(time_cells, remarks, subjectAndTeacher, lessonType, room, weekday)]
        if len(result) == 0:
            print(f"Error with loading {course}-{group}")
            with open(f"pages/{course}-{group}.html", "w+", encoding="utf-8") as file:
                file.write(text)
        return result

    @staticmethod
    def convert_lesson_type(lessonType: str) -> str:
        if lessonType == "л":
            return "Лекция"
        elif lessonType == "п":
            return "Практика"
        else:
            return ""

    @staticmethod
    def tag_to_text(tag) -> str:
        return tag.text.replace("\n", "")

    @staticmethod
    def map_tuple_to_lesson(lessonTuple: tuple, course: str = "", group: str = "") -> Lesson:
        time, remarks, subject_n_teacher, lesson_type, room, weekday = lessonTuple
        for br in subject_n_teacher.find_all("br"):
            br.replace_with(" %s\n" % br.text)

        lesson_extras = subject_n_teacher.text.split("\n")

        time, remarks, subject_n_teacher, lesson_type, room, weekday = [
            ParserService.tag_to_text(item) for item in lessonTuple]

        # Using lower() method for getting day in lower case.
        # Used for getting day from dictionary.
        weekday = weekday.lower()
        lesson: Lesson = {
            "time": time,
            "meta": remarks,
            "subject": subject_n_teacher,
            "type": ParserService.convert_lesson_type(lesson_type),
            "room": room,
            "weekday": weekday,
            "teacher": lesson_extras[1] if len(lesson_extras) > 1 else "",
            "course": course,
            "group": group
        }
        return lesson

    @staticmethod
    def extract_course_group(url: str) -> tuple[str, str]:
        # TODO: Proper handle
        parts = url.split("/")
        course_str = parts[-3]
        group_str = parts[-2]
        return course_str.split("-")[0], group_str.split("-")[0]


parser_service = ParserService()
