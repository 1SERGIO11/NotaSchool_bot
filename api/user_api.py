from model.user_draft import UserDraft
from utils.request_utils import get_request


async def get_user_draft_info(code: str) -> UserDraft | None:
    response = get_request(f"/register/{code}")
    if response.status_code != 200:
        return None

    json = response.json()

    return UserDraft(**json)


async def create_user(user_draft: UserDraft, experience: str):

    pass


async def get_moderators_for_payments() -> list[int]:
    return [646596194]