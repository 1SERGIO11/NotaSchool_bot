import dataclasses

@dataclasses.dataclass
class PaymentProps:
    receiver: str
    phone: str
    bank: str