from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api import course_api
from handler import payment
from model.lesson import Lesson

router = Router()

buy_callback = "BUY"
denied_callback = "DENIED"

class IntroductionStates(StatesGroup):
    watching_lesson = State()
    offer = State()
    payment_process = State()

async def onboarding_message(message: Message, state: FSMContext, experience: str):
    first_lesson = await course_api.get_intro_lesson(experience)
    if first_lesson is None:
        text = "К сожалению для твоего уровня пока нет курса, но в скором времени он обязательно появится :)"
        await message.answer(text)
        return
    text = "Начнём наше обучение. Вот тебе первый урок"
    await message.answer(text)
    await send_first_lesson(message, state, first_lesson)


async def send_first_lesson(message: Message, state: FSMContext, lesson: Lesson):
    text = f"<b>{lesson.title}</b>" + "\n\n" + \
            f"{lesson.description}" + "\n" \
            f"Ссылка: {lesson.link}"
    keyboard = InlineKeyboardBuilder() \
        .button(text="Посмотрел", callback_data="watched")
    await message.answer(text=text, reply_markup=keyboard.as_markup(), protect_content=True, parse_mode=ParseMode.HTML)
    await state.set_state(IntroductionStates.watching_lesson)


@router.callback_query(StateFilter(IntroductionStates.watching_lesson))
async def request_entering_code(callback_query: CallbackQuery, state: FSMContext):
    text = "Поздравляем тебя с первым просмотренным уроком!" + "\n" \
        "И предлагаем тебе по этому поводу купить полноценный курс всего за N рублей!"
    keyboard = InlineKeyboardBuilder() \
        .button(text="Хочу срочно купить", callback_data=buy_callback) \
        .button(text="Не интересует", callback_data=denied_callback) \
        .as_markup()
    await callback_query.message.answer(text=text, reply_markup=keyboard)
    await state.set_state(IntroductionStates.offer)


@router.callback_query(StateFilter(IntroductionStates.offer))
async def answer_to_offer(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == buy_callback:
        await state.update_data(course_id=1)
        await payment.payment_process_message(message=callback_query.message, state=state)
    else:
        pass