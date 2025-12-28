# Router and filters for handling incoming messages
from aiogram import Router, F

# Message object from Telegram
from aiogram.types import Message

# FSM components for managing multi-step user interactions
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# Used to send files from memory (bytes) to Telegram
from aiogram.types import BufferedInputFile

# Service for getting latest news (without search)
from services.search import get_latest_news

# Service functions for working with schedules
from services.schedule import (
    get_categories,
    get_groups,
    get_schedule_path,
)

# Reply keyboards used in the bot interface
from bot.keyboards import (
    main_menu_keyboard,
    categories_keyboard,
    groups_keyboard,
)

# Logging
import logging

logger = logging.getLogger(__name__)

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
    logger.info(f"User {message.from_user.id} started bot")
    await message.answer(
        "⛄ Привет! Я помощник института Цифры КемГУ.",
        reply_markup=main_menu_keyboard()
    )


# Handler for the /help command
@router.message(F.text == "/help")
async def help_handler(message: Message):
    logger.info(f"User {message.from_user.id} requested help")
    await message.answer(
        """
        ⛄ Давай посмотрим, что я умею:\n
        1. Новости - Посмотрим актуальные события Института\n
        2. Расписание - Быстро найдём твоё расписание\n
        3. /help - Руководство по использованию бота (ты тут)\n
        4. /start - Начать общение сначала
        """,
        reply_markup=main_menu_keyboard()
    )


# Handler for the "Новости" button
@router.message(F.text == "📺 Новости")
async def news_handler(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} requested latest news")
    # Clear any previous FSM state
    await state.clear()

    news = await get_latest_news(limit=5)

    if not news:
        await message.answer("🦌 Новости не найдены")
        logger.exception(
            f"News not found. News: {news}"
        )
        return

    response = "⛄ Последние новости:\n"
    for item in news:
        response += item

    await message.answer(response)


# Entry point for schedule selection
@router.message(F.text == "📄 Расписание")
async def schedule_start(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} started schedule flow")
    # Reset any previous state
    await state.clear()
    
    # Get available schedule categories
    categories = get_categories()

    # Switch FSM to category selection state
    await state.set_state(ScheduleStates.choosing_category)
    
    # Ask user to choose a schedule category
    await message.answer(
        "⛄ Выберите категорию расписания:",
        reply_markup=categories_keyboard(categories)
    )


# Handler for category selection
@router.message(ScheduleStates.choosing_category)
async def category_chosen(message: Message, state: FSMContext):
    category = message.text
    logger.info(f"User {message.from_user.id} chose category: {category}")
    
    # Get list of groups for the selected category
    groups = get_groups(category)

    # Validate category
    if not groups:
        await message.answer("🦌 Некорректная категория")
        logger.exception(
            f"Wrong category. Category: {category} . Groups: {groups}"
        )
        return

    # Save selected category to FSM context
    await state.update_data(category=category)
    
    # Switch FSM to group selection state
    await state.set_state(ScheduleStates.choosing_group)

    # Ask user to choose a group
    await message.answer(
        f"⛄\nКатегория: {category}\nВыберите группу:",
        reply_markup=groups_keyboard(groups)
    )


# Back button
@router.message(ScheduleStates.choosing_group, F.text == "⬅ Назад")
async def back_to_categories(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} returned to categories")
    
    categories = get_categories()

    await state.set_state(ScheduleStates.choosing_category)

    await message.answer(
        "⛄ Выберите категорию расписания:",
        reply_markup=categories_keyboard(categories)
    )


# Handler for group selection
@router.message(ScheduleStates.choosing_group)
async def group_chosen(message: Message, state: FSMContext):
    
    # to avoid processing this as a group
    if message.text == "⬅ Назад":
        return
    
    group = message.text
    data = await state.get_data()
    category = data.get("category")

    pdf_path = get_schedule_path(category, group)

    logger.info(f"User {message.from_user.id} chose group: {group} ({category})")

    if not pdf_path:
        await message.answer("🦌 Файл расписания не найден")
        logger.exception(
            f"The schedule file was not found. Category: {category} . Group: {group}"
        )
        return

    try:
        pdf_file = BufferedInputFile(
            file=pdf_path.read_bytes(),
            filename=pdf_path.name
        )

        await message.answer_document(
            document=pdf_file,
            caption=f"Расписание\n{category}\n{group}"
        )

    except Exception as e:
        await message.answer("🦌 Не удалось отправить файл расписания")
        logger.exception(
            f"Failed to send schedule PDF. Category: {category} . Group: {group} . Exception type: {e}"
        )

    await state.clear()
    await message.answer(
        "⛄ Выберите следующий раздел:",
        reply_markup=main_menu_keyboard()
    )


# Default handler for any other text
@router.message(F.text)
async def unknown_text_handler(message: Message):
    await message.answer(
        "⛄ Пожалуйста, выберите действие в меню",
        reply_markup=main_menu_keyboard()
    )