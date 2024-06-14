from aiogram import Router,F
from aiogram.filters import Command,CommandStart
from aiogram.types import Message,CallbackQuery,FSInputFile,ReplyKeyboardRemove
import handlers.keyboards as KB
from database.request import *
from database.models import *
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
router = Router()
import logging
from typing import Any, Dict


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


from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class AddRabStates(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    salary = State()
    email = State()
    phone = State()
    address = State()
    department_id = State()



@router.message(Command("add_rab"))
async def cmd_add_rab(message:Message,state: FSMContext):
    await state.set_state(AddRabStates.first_name)
    await message.answer("Enter first name:",
    reply_markup=ReplyKeyboardRemove())
    
@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(AddRabStates.first_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text)
    await state.set_state(AddRabStates.last_name)
    await message.answer("Enter last name:",
    reply_markup=ReplyKeyboardRemove())


@router.message(AddRabStates.last_name)
async def process_last_name(message: Message, state: FSMContext) -> None:
    await state.update_data(last_name=message.text)
    await state.set_state(AddRabStates.age)
    await message.answer("Enter age:")

@router.message(AddRabStates.age)
async def process_age(message: Message, state: FSMContext) -> None:
    await state.update_data(age=int(message.text))
    await state.set_state(AddRabStates.salary)
    await message.answer("Enter salary:")

@router.message(AddRabStates.salary)
async def process_salary(message: Message, state: FSMContext) -> None:
    await state.update_data(salary=float(message.text))
    await state.set_state(AddRabStates.email)
    await message.answer("Enter email:")

@router.message(AddRabStates.email)
async def process_email(message: Message, state: FSMContext) -> None:
    await state.update_data(email=message.text)
    await state.set_state(AddRabStates.phone)
    await message.answer("Enter phone:")

@router.message(AddRabStates.phone)
async def process_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(phone=int(message.text))
    await state.set_state(AddRabStates.address)
    await message.answer("Enter address:")

@router.message(AddRabStates.address)
async def process_address(message: Message, state: FSMContext) -> None:
    await state.update_data(address=message.text)
    await state.set_state(AddRabStates.department_id)
    await message.answer("Enter department id:")

@router.message(AddRabStates.department_id)
async def process_department_id(message: Message, state: FSMContext) -> None:
    await state.update_data(department_id=int(message.text))
    data = await state.get_data()
    await show_summary(message, data)
    await state.clear()

async def show_summary(message: Message, data: Dict[str, Any]):
    rab = Rab(first_name=data["first_name"],
              last_name=data["last_name"],
              age=data["age"],
              salary=data["salary"], 
              email=data["email"], 
              phone=data["phone"], 
              address=data["address"],
              department_id=data["department_id"])
    result = await create_rab(rab)
    await message.answer(text="Успешно добавили рабочего", reply_markup=ReplyKeyboardRemove())
































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


