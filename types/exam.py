from typing import TypedDict


class Exam(TypedDict):
    """
    The object representing an exam.
    """

    group: str
    subject: str
    teacher: str
    examDate: str
    examTime: str
    examRoom: str
    consultationDate: str
    consultationTime: str
    consultationRoom: str
