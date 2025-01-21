from model.lesson import Lesson

async def get_intro_lesson(experience: str) -> Lesson | None:
    if experience == "HAS_EXPERIENCE":
        return None
    return Lesson(
        title="Урок №1. Кузнечик",
        description="lorem ipsum dolor sit",
        link="https://www.youtube.com/watch?v=7KDFF3gouOs&pp=ygUi0LrRg9C30L3QtdGH0LjQuiDQvdCwINCz0LjRgtCw0YDQtQ%3D%3D"
    )