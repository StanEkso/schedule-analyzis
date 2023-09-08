
from services.search import search_service
import asyncio
from services.analyze import check_data, collectRooms, collectTimes, create_base_object, fill_data
from services.common import rooms


import pandas as pd

def highlight_conflict(value):
    return ['background-color: red' if "Конфликт" in v else '' for v in value]

async def grab_lessons():
    scheduleObj = await search_service.grab_groups("https://mmf.bsu.by/ru/raspisanie-zanyatij/")
    lessons = await search_service.grab_schedule(scheduleObj)

    object = create_base_object()

    fill_data(lessons, object)
    check_data(object)


    df = pd.DataFrame(object)
    writer = pd.ExcelWriter('file2.xlsx') 

    workbook = writer.book

    wrap_format = workbook.add_format({'text_wrap': True})

    df.style.apply(highlight_conflict, subset=rooms)

    df.style.apply(highlight_conflict, subset=rooms).to_excel(writer, sheet_name='Конфликты', index=False, na_rep='NaN')



    for i in range(50):
        writer.sheets['Конфликты'].set_row(i, 80)


    for column in df:
        column_length = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        if column != "Время\Аудитории":
          writer.sheets['Конфликты'].set_column(col_idx, col_idx, 20, wrap_format)
          continue
        writer.sheets['Конфликты'].set_column(col_idx, col_idx, column_length)

    writer.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(grab_lessons())