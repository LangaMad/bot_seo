from aiogram import Router,F
from aiogram.filters import Command,CommandStart
from aiogram.types import Message,CallbackQuery,FSInputFile
import handlers.keyboards as KB
from database.request import *
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
router = Router()


@router.message(CommandStart())
async def start(message:Message):
    await message.answer("Hello I`m bot ceo helper",reply_markup=KB.kb)

@router.message(Command(commands=['help']))
async def help(message:Message):
    await message.answer("For help call 911")


@router.message(F.text == 'Departments')
async def departments(message:Message):
    await message.answer("Choice department",reply_markup= await KB.departments_kb())

@router.message(F.text == 'Rabы')
async def workers(message:Message):
    await message.answer("Choice Worker",reply_markup= await KB.workers_kb())



@router.callback_query(F.data.startswith('department_'))
async def department(callback:CallbackQuery):
    await callback.message.delete()
    department_id = callback.data.split('_')[1]
    await callback.message.answer(
        "Люди работающие в этом отделе:", 
        reply_markup= await KB.rab_kb(department_id)
        )

@router.callback_query(F.data == 'back_1')
async def back_1(callback:CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Choice department",
        reply_markup= await KB.departments_kb())

@router.callback_query(F.data.startswith('rab_'))
async def rab(callback:CallbackQuery):
    await callback.message.delete()
    rab_id = callback.data.split('_')[1]
    rab = await get_rab(rab_id)
    await callback.message.answer(f"""Информация о работнике:\nИмя Фамилия: {rab.first_name} {rab.last_name} \nВозраст: {rab.age}\nemail: {rab.email} \nЗаработная плата: {rab.salary} \nНомер телефона: {rab.phone} \nАдрес: {rab.address} \n""".strip(),
                    reply_markup=await KB.delete_rab_kb(rab_id))

# from contextlib import suppress
# @router.callback_query(KB.Pagination.filter(F.action.in_(
#     ['next','prev'])))
# async def pagination(callback:CallbackQuery,callback_data:KB.Pagination):
#     page_number = int(callback_data.page)
    
#     result = await rab_data()
#     if callback_data.action == 'next':
#         if page_number < len(result) - 1:
#             page_number += 1
#         else:
#             page = page_number
#             await callback.message.answer(f'Last page')
#     elif callback_data.action == 'prev':
#         if page_number > 0:
#             page_number -= 1
#         else:
#             page = 0
#             await callback.message.answer(f'First page')       
        
#     with suppress(TelegramBadRequest):
#         await callback.message.edit_text(
#             text=f'{result[page_number][1]} {result[page_number][2]}',
#             reply_markup=KB.Pagination.paginator(page_number)
#         )
        
    


# # text = 'department_2'
# # print(text.split('_'))
# # выводит:
# # ['department','2']


