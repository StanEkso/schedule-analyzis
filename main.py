
import json
import openpyxl
from shared.analyze.main import has_conflict_inner_tuple
from shared.services.search import search_service
import asyncio
from shared.services.analyze import DIFFERENT_WEEKS_KEY, INFORMATION_HOUR_KEY, check_data, collectTimes, create_base_object, fill_data, filter_lessons
from shared.services.common import rooms
from shared.services.excel_read import read_from_excel, to_lessons, to_times


from datetime import datetime
import pandas as pd

from shared.types.lesson import Lesson

def highlight_conflicts(value: list[str]):
    return [highlight_cell(v) for v in value]


def highlight_cell(value: str):
    if "Конфликт" in value:
        return 'background-color: yellow'
    if INFORMATION_HOUR_KEY in value.lower():
        return 'background-color: #8b00ff'
    if DIFFERENT_WEEKS_KEY in value:
        return 'background-color: #f7f7f7'

    # if len(value.split(lesson_separator)) >= 2:
    #     return 'background-color: yellow'
    if len(value) != 0:
        return 'background-color: #f7f7f7'
    return ''

async def grab_lessons():
    df = read_from_excel()

    times = to_times(df)
    lessons = to_lessons(df)

    # scheduleObj = await search_service.grab_groups("https://mmf.bsu.by/ru/raspisanie-zanyatij/")

    # lessons = search_service.grab_schedule_sync(scheduleObj)

    lessons = filter_lessons(lessons)

    # with open("file.json", "w+", encoding="utf-8") as file:
    #     json.dump(lessons, file, ensure_ascii=False, indent=4)

    # times = list(collectTimes(lessons))

    # times.sort(key=lambda v: (v[0:1], v[2:3]))

    # print(times)

    object = create_base_object(times)

    fill_data(lessons, object, times)

    check_data(object)


    df = pd.DataFrame(object)

    now = datetime.now()

    formatted_date = now.strftime("%Y-%m-%d-%H-%M-%S")
    file_name = f'results/report-{formatted_date}.xlsx'

    writer = pd.ExcelWriter(file_name) 

    workbook = writer.book

    wrap_format = workbook.add_format({'text_wrap': True, 'bold': True })

    wrap_format.set_text_wrap(True)
    df.style.set_properties({ "text_wrap": True })
    df.style.apply(highlight_conflicts, subset=rooms).to_excel(writer, sheet_name='Конфликты', index=False, na_rep='NaN', freeze_panes=(1, 1))

    for i in range(1, 1000):
        writer.sheets['Конфликты'].set_row(i, 80, wrap_format)


    for column in df:
        column_length = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)

        if column != "Время\Аудитории":
          writer.sheets['Конфликты'].set_column(col_idx, col_idx, 20, wrap_format)
          continue
        writer.sheets['Конфликты'].set_column(col_idx, col_idx, column_length, None)

    writer.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(grab_lessons())