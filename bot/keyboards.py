from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Main functions menu
def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Новости")],
            [KeyboardButton(text="Расписание")],
        ],
        resize_keyboard=True
    )

# Back button
def back_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Назад")]],
        resize_keyboard=True
    )

# Select categories to search for schedules
def categories_keyboard(categories: list[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=category)] for category in categories],
        resize_keyboard=True
    )

# Group selection (encapsulated after category selection)
def groups_keyboard(groups: list[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=group)] for group in groups],
        resize_keyboard=True
    )