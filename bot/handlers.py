# Router and filters for handling incoming messages
from aiogram import Router, F

# Message object from Telegram
from aiogram.types import Message

# FSM components for managing multi-step user interactions
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# Used to send files from memory (bytes) to Telegram
from aiogram.types import BufferedInputFile

# HTTP client for downloading PDF files from external sources
import requests

# Service for searching news on the university website
from services.search import get_news_for_user

# Service functions for working with schedules
from services.schedule import (
    get_categories,
    get_groups,
    get_schedule_url,
)

# Reply keyboards used in the bot interface
from bot.keyboards import (
    main_menu_keyboard,
    categories_keyboard,
    groups_keyboard,
)


# Create a router instance for this module
router = Router()


# FSM states for schedule selection flow
class ScheduleStates(StatesGroup):
    # State where user selects a schedule category (course, exams, etc.)
    choosing_category = State()
    
    # State where user selects a specific group
    choosing_group = State()


# Handler for the /start command
@router.message(F.text == "/start")
async def start_handler(message: Message):
    # Send greeting message and show the main menu
    await message.answer(
        "Привет! Я помощник Института цифры КемГУ.",
        reply_markup=main_menu_keyboard()
    )


# Entry point for schedule selection
@router.message(F.text == "Расписание")
async def schedule_start(message: Message, state: FSMContext):
    # Reset any previous state
    await state.clear()
    
    # Get available schedule categories
    categories = get_categories()

    # Switch FSM to category selection state
    await state.set_state(ScheduleStates.choosing_category)
    
    # Ask user to choose a schedule category
    await message.answer(
        "Выберите категорию расписания:",
        reply_markup=categories_keyboard(categories)
    )


# Handler for category selection
@router.message(ScheduleStates.choosing_category)
async def category_chosen(message: Message, state: FSMContext):
    category = message.text
    
    # Get list of groups for the selected category
    groups = get_groups(category)

    # Validate category
    if not groups:
        await message.answer("Некорректная категория.")
        return

    # Save selected category to FSM context
    await state.update_data(category=category)
    
    # Switch FSM to group selection state
    await state.set_state(ScheduleStates.choosing_group)

    # Ask user to choose a group
    await message.answer(
        f"Категория: {category}\nВыберите группу:",
        reply_markup=groups_keyboard(groups)
    )


# Handler for group selection
@router.message(ScheduleStates.choosing_group)
async def group_chosen(message: Message, state: FSMContext):
    group = message.text
    
    # Retrieve previously saved category from FSM context
    data = await state.get_data()
    category = data.get("category")

    # Get direct URL to the schedule PDF
    url = get_schedule_url(category, group)

    # Validate URL existence
    if not url:
        await message.answer("Расписание для выбранной группы не найдено.")
        return

    try:
        # Download the PDF file from the university website
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        # Wrap file bytes for sending to Telegram
        pdf_file = BufferedInputFile(
            file=response.content,
            filename="schedule.pdf"
        )

        # Send the PDF document to the user
        await message.answer_document(
            document=pdf_file,
            caption=f"Расписание\n{category}\n{group}"
        )

    except Exception:
        # Fallback: send the direct link if file download fails
        await message.answer(
            "Не удалось загрузить файл напрямую.\n"
            f"Вот ссылка на расписание:\n{url}"
        )

    # Clear FSM state after completing the flow
    await state.clear()
    
    # Return user to the main menu
    await message.answer(
        "Выберите следующий раздел:",
        reply_markup=main_menu_keyboard()
    )


# Default text handler for news search
@router.message(F.text)
async def text_handler(message: Message):
    # Clean user input
    query = message.text.strip()

    # Search for news based on user query
    news = get_news_for_user(query)

    # Inform user if no results were found
    if not news:
        await message.answer("По вашему запросу ничего не найдено.")
        return

    # Build response message with found news
    response = "Найденные новости:\n\n"
    for item in news:
        response += f"• {item}\n"

    # Send news list to the user
    await message.answer(response)