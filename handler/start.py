from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api.user_api import get_user_draft_info, create_user
from handler.introduction import onboarding_message

router = Router()

experience = {
    "Новичок, сбацаю кузнечика": "NEWBIE",
    "Уверенно держу баррэ": "HAS_EXPERIENCE",
    "Не знаю 🤷": "NONE",
}

class StartStates(StatesGroup):
    registering = State()
    entering_unique_code = State()
    choosing_experience = State()

async def start_register(message: Message, state: FSMContext):
    data = message.text.split()
    if len(data) == 1:
        await unregistered_message(message, state)
        return
    payload = data[-1]
    await welcome_message(message, payload, state)

async def unregistered_message(message: Message, state: FSMContext):
    text = "К сожалению, ты ещё не зарегистрирован 😕" + "\n" \
        "Зарегистрируйся на сайте и возвращайся с кодом :)"
    keyboard = InlineKeyboardBuilder() \
                .row(InlineKeyboardButton(text="Наш сайт", url="https://www.youtube.com/watch?v=NDT6k7_y3AY")) \
                .row(InlineKeyboardButton(text="Зарегистрировался 😎", callback_data=f"registered"))
    await state.set_state(StartStates.registering)
    await message.answer(text=text, reply_markup=keyboard.as_markup())


@router.callback_query(StateFilter(StartStates.registering))
async def request_entering_code(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(text="Отлично, теперь вводи код, который ты получил на сайте")
    await state.set_state(StartStates.entering_unique_code)


@router.message(StateFilter(StartStates.entering_unique_code))
async def entering_unique_code(message: Message, state: FSMContext):
    code = message.text
    user = await get_user_draft_info(code)
    if user is None:
        keyboard = InlineKeyboardBuilder() \
            .row(InlineKeyboardButton(text="Наш сайт", url="https://www.youtube.com/watch?v=NDT6k7_y3AY"))
        await message.answer("К сожалению, этот код неверный.\nПроверь правильно ли ты его написал, либо зарегистрируйся заново и вводи его снова", reply_markup=keyboard.as_markup())
        return
    await state.update_data(user=user)
    await message.answer(text="Отлично, код принят! Двигаемся дальше.")
    await select_experience_message(message, state)



async def welcome_message(message: Message, code: str, state: FSMContext):
    user = await get_user_draft_info(code)
    if user is None:
        await entering_unique_code(message, state)
        return
    text = f"Привет, {user.name}!" + "\n" \
        "Осталось совсем чуть-чуть, нам нужно всего-лишь уточнить пару моментов 🙂"
    await message.answer(text=text)
    await state.update_data(user=user)
    await select_experience_message(message,state)

async def select_experience_message(message: Message, state: FSMContext):
    text = "Для более точного формирования курсов, мы хотим знать твой опыт в игре на гитаре)" +"\n" \
        "Выбери свой опыт, согласно описанию на кнопках"
    keyboard = InlineKeyboardBuilder()
    for key, value in experience.items():
        keyboard.row(InlineKeyboardButton(text=key, callback_data=value))
    await message.answer(text=text, reply_markup=keyboard.as_markup())
    await state.set_state(StartStates.choosing_experience)


@router.callback_query(StateFilter(StartStates.choosing_experience))
async def choose_experience_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(choose_experience=callback_query.data)
    data = await state.get_data()
    await create_user(user_draft=data['user'], experience=data['choose_experience'])
    await callback_query.message.delete()
    await callback_query.message.answer(text="Поздравляем! Теперь ты наконец можешь смотреть наши курсы!")
    await state.clear()
    await state.set_data({})
    await onboarding_message(message=callback_query.message, state=state, experience=data['choose_experience'])

