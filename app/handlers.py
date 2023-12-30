import logging
import os
from dotenv import load_dotenv
import sys
from os import getenv
from aiohttp import web

from aiogram import Bot, Dispatcher, Router, types, F, html
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.fsm.context import FSMContext

# All handlers should be attached to the Router (or Dispatcher)
router = Router()

class Gym(StatesGroup):
    weight = State()
    height = State()




@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Gym.weight)
    await message.answer(
        "Привет! Напиши свой вес",
        reply_markup=ReplyKeyboardRemove(),
    )



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



@router.message(Gym.weight)
async def process_weight(message: Message, state: FSMContext) -> None:
    data = await state.update_data(weight=message.text)
    await state.set_state(Gym.height)
    await message.answer(
        f"Понял. Теперь напиши свой рост"
    )



@router.message(Gym.height)
async def process_height(message: Message, state: FSMContext) -> None:
    data = await state.update_data(height=message.text)
    await state.clear()
    await message.answer(
        f"Понял. Твои габариты: {data['weight']} и {data['height']}"
    )
