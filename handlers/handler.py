from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import CommandStart, BaseFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboard.kb import (amdin_main, promocode_kb, to_main, 
                         promocode_title_add, promocode_title_del)
from requests_server.http_requests import (set_promocode, delete_promocode, 
                                           get_user_buy_promocode, get_all_promocode)
from config import ADMINS
from openpyxl import Workbook
from io import BytesIO
import logging

router = Router()

class AddPromoState(StatesGroup):
    promocode = State()
    
class DelPromoState(StatesGroup):
    promocode = State()    

class AdminFilter(BaseFilter):
    async def __call__(self, message: Message):
        tg_id = str(message.from_user.id)
        try:
            if tg_id in ADMINS["admins"]:
                logging.info(f"Пользователь {tg_id} является админом.")
                return tg_id
            else:
                logging.info(f"Пользователь {tg_id} не является администратором")
        except Exception as e:
            logging.error(f"Ошибка при проверке админа для tg_id {tg_id}: {e}")
            return False

@router.message(AdminFilter(), CommandStart())
@router.callback_query(AdminFilter(), F.data.startswith('to_main'))
async def cmd_start_admin(message: Message | CallbackQuery):
    message_admin = 'Добро пожаловать в админ панель!'
    message_cancels = 'Вы вернулись на главную панель!'
    
    if isinstance(message, Message):
        await message.answer(message_admin, reply_markup=amdin_main())
    elif isinstance(message, CallbackQuery):
        await message.message.edit_text(message_cancels, reply_markup=amdin_main())   
    
@router.callback_query(AdminFilter(), F.data.startswith('add_promo'))
async def add_promocode_admin(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Выберите категорию товара для добавления промокодов', reply_markup=promocode_title_add())
    
@router.callback_query(AdminFilter(), F.data.startswith('tariff_add:'))
async def add_promocode_one(callback: CallbackQuery, state: FSMContext):
    title = callback.data.split(':')[1]
    await state.update_data(title=title)
    await callback.answer()
    await callback.message.answer(f'Введите все промокоды для {title}, разделяя их переносом строки.')
    await state.set_state(AddPromoState.promocode)

@router.message(AdminFilter(), AddPromoState.promocode)
async def add_promocode_completed(message: Message, state: FSMContext):
    await state.update_data(promocode=message.text)
    get_data = await state.get_data()
    promo_codes = get_data.get('promocode').splitlines()  
    
    title = get_data.get('title')
    for promo in promo_codes:
        await set_promocode(promocode=promo, title=title)
    await message.answer(f'Промокоды для товара {title} успешно добавлены.', reply_markup=await to_main())
    await state.clear()
    
@router.callback_query(AdminFilter(), F.data.startswith('all_promo'))
async def get_promocode_all(callback: CallbackQuery):
    all_user_by_promo = await get_user_buy_promocode()
    all_promo = await get_all_promocode()

    workbook_user = Workbook()
    sheet_user = workbook_user.active
    sheet_user.title = "Купленные товары и промокоды"
    sheet_user.append(["ID пользователя", "Купленный товар", "Выданный промокод", "Cумма товара"])
    
    for user in all_user_by_promo:
        user_id = user['tg_id']  
        product_title = user['card_title']  
        promocode = user['promocode']
        price = user['price']  
        sheet_user.append([user_id, product_title, promocode, price])

    workbook_promo = Workbook()
    sheet_promo = workbook_promo.active
    sheet_promo.title = "Оставшиеся промокоды"
    sheet_promo.append(["Промокод", "Товар"])

    for promocode in all_promo:
        promo = promocode['promocode']
        title = promocode['title']
        sheet_promo.append([promo, title])

    byte_io_user = BytesIO()
    workbook_user.save(byte_io_user)
    byte_io_user.seek(0)

    byte_io_promo = BytesIO()
    workbook_promo.save(byte_io_promo)
    byte_io_promo.seek(0)

    document_by_user = BufferedInputFile(byte_io_user.read(), filename="user_by_promocode_all.xlsx")
    document_by_promo = BufferedInputFile(byte_io_promo.read(), filename="promocode_all.xlsx")
    
    await callback.answer()  
    
    await callback.message.answer_document(
        document=document_by_user,
        caption="Вот файл с купленными товарами и промокодами."
    )
    
    await callback.message.answer_document(
        document=document_by_promo,
        caption="А вот файл с оставшимися промокодами.",
    )


    
@router.callback_query(AdminFilter(), F.data.startswith('del_promo'))
async def del_promocode_kb(callback: CallbackQuery, state: FSMContext):
    """Выбор категории товара для удаления промокодов."""
    await callback.answer()
    await callback.message.answer('Выберите категорию товара для удаления промокодов', reply_markup=promocode_title_del())

@router.callback_query(AdminFilter(), F.data.startswith('tariff_del:'))
async def del_promo_completed(callback: CallbackQuery, state: FSMContext):
    title = callback.data.split(':')[1]
    promocode_keyboard = await promocode_kb(title)
    
    if promocode_keyboard:
        await callback.message.answer(f'Выберите промокод для удаления из категории {title}:', reply_markup=promocode_keyboard)
    else:
        await callback.message.answer(f'В данной категории товаров нет промокодов.')
    await state.clear()

@router.callback_query(AdminFilter(), F.data.startswith('del_'))
async def delete_selected_promocode(callback: CallbackQuery, state: FSMContext):
    promo_code = callback.data.split('_')[1]
    delete_promocoded = await delete_promocode(promocode=promo_code)
    deleted_promocode = delete_promocoded['deleted']
    await callback.message.answer(f'Промокод {deleted_promocode} успешно удален.', reply_markup=await to_main())
    await state.clear()
    
@router.message(CommandStart())
async def cmd_start_user(message: Message):
    await message.answer('Здарова, это бот для отправки сообщение в канал, тебе тут не место!')    
