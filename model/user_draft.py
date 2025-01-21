import dataclasses

@dataclasses.dataclass
class UserDraft:
    name: str
    email: str
    phone: str
    registrationCode: str
