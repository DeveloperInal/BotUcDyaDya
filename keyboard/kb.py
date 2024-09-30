from aiogram.utils.keyboard import InlineKeyboardBuilder
from requests_server.http_requests import get_promocodes_by_title

def amdin_main():
    kb_inline = InlineKeyboardBuilder()
    kb_inline.button(text='Добавить промокод', callback_data='add_promo')
    kb_inline.button(text='Все промокоды', callback_data='all_promo')
    kb_inline.button(text='Удалить промокод', callback_data='del_promo')
    return kb_inline.adjust(2).as_markup()

async def to_main():
   kb_inline = InlineKeyboardBuilder()
   kb_inline.button(text=f'Назад', callback_data='to_main')
   return kb_inline.as_markup()

def promocode_title_add():
    kb_inline = InlineKeyboardBuilder()
    kb_inline.button(text='60UC', callback_data='tariff_add:60UC')
    kb_inline.button(text='325UC', callback_data='tariff_add:325UC')
    kb_inline.button(text='660UC', callback_data='tariff_add:660UC')
    kb_inline.button(text='1800UC', callback_data='tariff_add:1800UC')
    kb_inline.button(text='3850UC', callback_data='tariff_add:3850UC')
    kb_inline.button(text='8100UC', callback_data='tariff_add:8100UC')
    return kb_inline.adjust(3).as_markup()

def promocode_title_del():
    kb_inline = InlineKeyboardBuilder()
    kb_inline.button(text='60UC', callback_data='tariff_del:60UC')
    kb_inline.button(text='325UC', callback_data='tariff_del:325UC')
    kb_inline.button(text='660UC', callback_data='tariff_del:660UC')
    kb_inline.button(text='1800UC', callback_data='tariff_del:1800UC')
    kb_inline.button(text='3850UC', callback_data='tariff_del:3850UC')
    kb_inline.button(text='8100UC', callback_data='tariff_del:8100UC')
    return kb_inline.adjust(3).as_markup()

def user_main():
    kb_inline = InlineKeyboardBuilder()
    kb_inline.button(text='Информация', callback_data='info')
    kb_inline.button(text='Помощь', callback_data='help')
    return kb_inline.adjust(2).as_markup()

async def promocode_kb(title: str):
    promocodes = await get_promocodes_by_title(title)
    if not promocodes or isinstance(promocodes, str):
        return None 
    keyboard = InlineKeyboardBuilder()
    if isinstance(promocodes, list):
        for promo in promocodes:
            promo_code = str(promo) 
            keyboard.button(text=f'{promo_code}', callback_data=f'del_{promo_code}')
    return keyboard.adjust(2).as_markup()
