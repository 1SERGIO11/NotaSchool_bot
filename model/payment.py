import dataclasses

@dataclasses.dataclass
class Payment:
    id: str
    user: int
    amount: int
    courses_id: list[int]
    payment_message: str
    status: str