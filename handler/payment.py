from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api import payment_api, user_api
from bot import bot

router = Router()

class PaymentStates(StatesGroup):
     payment_process = State()
     denied_payment_reason = State()



async def payment_process_message(message: Message, state: FSMContext):
   await message.delete()
   data = await state.get_data()
   course_id = data['course_id']
   props = await payment_api.payment_props()
   payment = await payment_api.payment_start(user_id=message.from_user.id, course_id=course_id)
   text = "Тебе необходимо перевести деньги по данным реквизитам: " + "\n\n" \
       f"Получатель: {props.receiver}" + "\n" \
       f"Номер телефона: {props.phone}" + "\n" \
       f"Банк: {props.bank}" + "\n" \
       f"Сумма: {payment.amount} рублей" + "\n\n" \
       "Обязательно укажи данный комментарий к платежу:" + "\n" \
       f"<code>{payment.payment_message}</code>"
   keyboard = InlineKeyboardBuilder() \
       .button(text="Оплатил", callback_data="complete_payment") \
       .button(text="Отмена", callback_data="cancel") \
       .as_markup()
   await state.set_state(PaymentStates.payment_process)
   await state.update_data(payment_id=payment.id)
   await message.answer(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


@router.callback_query(StateFilter(PaymentStates.payment_process))
async def answer_to_offer(callback_query: CallbackQuery, state: FSMContext):
     if callback_query.data == "complete_payment":
          await callback_query.message.delete()
          text = "Спасибо за оплату курса! Обработка платежа может занять некоторое время."
          data = await state.get_data()
          await state.clear()
          await callback_query.message.answer(text=text)
          payment = await payment_api.payment_process(data["payment_id"])
          await payment_confirmation_message(payment.id, payment_message=payment.payment_message)
     else:
          text = "Платёж отменен"
          await state.clear()
          await callback_query.message.answer(text=text)


async def payment_confirmation_message(payment_id: str, payment_message: str):
     moderators = await user_api.get_moderators_for_payments()
     keyboard = InlineKeyboardBuilder() \
          .button(text="Оплатил", callback_data=f"confirm_payment_{payment_id}") \
          .button(text="Отказ", callback_data=f"denied_payment_{payment_id}") \
          .adjust(1) \
          .as_markup()
     text = f"Требуется подтверждение оплаты с таким сообщением: \n<code>{payment_message}</code>"
     for moderator in moderators:
          await bot.send_message(chat_id=moderator, reply_markup=keyboard, text=text, parse_mode=ParseMode.HTML)


@router.callback_query(lambda x: x.data.startswith("confirm_payment_"))
async def payment_confirmation(callback_query: CallbackQuery):
     await callback_query.message.delete()
     payment_id = callback_query.data.split("_")[-1]
     payment = await payment_api.confirm_payment(payment_id)
     user = payment.user
     text = f"Ваш платёж успешно подтвержден! Теперь вы можете насладиться курсом!"
     await bot.send_message(chat_id=user, text=text)


@router.callback_query(lambda x: x.data.startswith("denied_payment_"))
async def payment_denied(callback_query: CallbackQuery, state: FSMContext):
     await callback_query.message.delete()
     payment_id = callback_query.data.split("_")[-1]
     await state.update_data(payment_id_denied=payment_id)
     await state.set_state(PaymentStates.denied_payment_reason)
     await callback_query.message.answer(text="Введите причину отклонения платежа:")


@router.message(StateFilter(PaymentStates.denied_payment_reason))
async def denied_payment_reason(message: Message, state: FSMContext):
    data = await state.get_data()
    payment_id = data["payment_id_denied"]
    payment = await payment_api.denied_payment(payment_id)
    await state.clear()
    user = payment.user
    message_text = message.text
    text = f"К сожалению, ваш платёж отклонён. \nПричина: \n{message_text}"
    await bot.send_message(chat_id=user, text=text)