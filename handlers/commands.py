from aiogram import Router,F
from aiogram.filters import Command,CommandStart
from aiogram.types import Message,CallbackQuery,FSInputFile
import handlers.keyboards as KB

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







