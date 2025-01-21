from model.payment_props import PaymentProps
from model.payment import Payment


async def payment_props() -> PaymentProps | None:
    return PaymentProps(
        phone="+79123456789",
        receiver="Акст А.",
        bank="Tinkoff"
    )


async def payment_start(user_id: int, course_id: int) -> Payment:
    return Payment(
        id="1234-5678-1234",
        user=646596194,
        courses_id=[1],
        amount=1499,
        payment_message="tg:Tb123Sfg3451",
        status="WAITING_PAYMENT"
    )


async def payment_process(id: str) -> Payment | None:
    return Payment(
        id="1234-5678-1234",
        user=646596194,
        courses_id=[1],
        amount=1499,
        payment_message="tg:Tb123Sfg3451",
        status="WAITING_CONFIRMATION"
    )


async def confirm_payment(id: str) -> Payment | None:
    return Payment(
        id=id,
        user=646596194,
        courses_id=[1],
        amount=1499,
        payment_message="tg:Tb123Sfg3451",
        status="CONFIRMED"
    )


async def denied_payment(id: str) -> Payment | None:
    return Payment(
        id=id,
        user=646596194,
        courses_id=[1],
        amount=1499,
        payment_message="tg:Tb123Sfg3451",
        status="DENIED"
    )