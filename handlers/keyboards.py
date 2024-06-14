from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder
from database.request import * 
from aiogram.filters.callback_data import CallbackData

from aiogram_widgets.pagination import KeyboardPaginator



kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Departments')],
    [KeyboardButton(text='Rabы')]],
    resize_keyboard=True,input_field_placeholder='Выберите действие',
    one_time_keyboard=True)

async def departments_kb():
    departments = await get_departments()
    kb = InlineKeyboardBuilder()
    for depp in departments:
        kb.add(InlineKeyboardButton(text = depp.name,
            callback_data=f'department_{depp.id}'))
    return kb.adjust(2).as_markup()

async def workers_kb():
    workers= await get_worker()
    kb = InlineKeyboardBuilder()
    for worker in workers:
        kb.add(InlineKeyboardButton(text = f'{worker.first_name} {worker.last_name}',
            callback_data=f'rab_{worker.id}'))
    return kb.adjust(2).as_markup()

async def rab_kb(department_id):
    rab = await get_rabs(department_id)
    kb = InlineKeyboardBuilder()
    for rabs in rab:
        kb.add(InlineKeyboardButton(text = f'{rabs.first_name} {rabs.last_name}',
            callback_data=f'rab_{rabs.id}'))
        
    kb.add(InlineKeyboardButton(text='◀️',
            callback_data='back_1'))
    return kb.adjust(2).as_markup()



# create delete inline button
async def delete_rab_kb(rab_id):
    delete = await delete_rab(rab_id)
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Back',
            callback_data='back_2'))
    kb.add(InlineKeyboardButton(text='Delete',
            callback_data=f'delete_{rab_id}'))
    return kb.adjust(2).as_markup()

# create create inline button

async def create_rab_kb(department_id):
    
    return kb.adjust(2).as_markup()



# class Pagination(CallbackData, prefix="pagination"):
#     page: int
#     action: str
    
#     def paginator(page: int = 0):
#         pg_builder = InlineKeyboardBuilder()
#         pg_builder.row(InlineKeyboardButton(text='◀️',
#         callback_data=Pagination(page=page, action='prev').pack()),
#                        InlineKeyboardButton(text='▶️',
#         callback_data=Pagination(page=page, action='next').pack()),
#         width=2)
    
#         return pg_builder.as_markup()


# # def create_paginator():
# #     buttons = [
# #         InlineKeyboardButton(text=f"Button {i}", callback_data=f"button_{i}")
# #         for i in range(1, 1001)
# #     ]
# #     additional_buttons = [
# #         [
# #             InlineKeyboardButton(text="Go back 🔙", callback_data="go_back"),
#         ]
#     ]

#     paginator = KeyboardPaginator(
#         data=buttons,
#         additional_buttons=additional_buttons,    
#         per_page=20, 
#         per_row=2
#     )

#     return paginator

# ['faf','afa','afa','afadfa']
# ['faf']['afa']
# ['afa']['afadfa']




