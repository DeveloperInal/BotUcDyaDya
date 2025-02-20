from httpx import AsyncClient
from aiohttp import ClientSession
from core.settings import settings
import logging

http_client = AsyncClient()
base_url = settings.http_client

async def set_promocode(promocode: str, title: str):
    url = f'{base_url}/set_promocod'
    promocode_data = { "promocode": promocode, "title": title } 
    try:
        async with ClientSession() as client:
            async with client.post(url=url, json=promocode_data) as response:
                if response.status == 200:
                    data = await response.json()
                    logging.info(f"Полученные промокоды: {data}") 
                    return data 
                else:
                    logging.warning(f"Ошибка при добавлении промокода {promocode}: статус {response.status}")
    except Exception as e:
        logging.error(f"Ошибка при добавлении промокода: {e}")
        
async def get_all_promocode():
    url = f'{base_url}/get_promocode'
    headers = {'Content-Type': 'application/json'}
    try:
        async with ClientSession() as client:
            async with client.get(url=url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
            logging.warning('Админ успешно получил все промокоды')
    except Exception as e:
        logging.error(f'Ошибка при получении промокодов: {e}')
        
async def delete_promocode(promocode: str):
    url = f'{base_url}/delete_promocod?promocode={promocode}'                              
    try:
        async with ClientSession() as client:
            async with client.delete(url=url) as responce:
                if responce.status == 200:
                    return await responce.json()
        logging.warning('Промокод успешно добавлен')
    except Exception as e:
        logging.error(f'Ошибка при удалении промокода: {e}')
        
async def get_user_buy_promocode():
    url = f'{base_url}/get_user_by_promocode'
    headers = {'Content-Type': 'application/json'}
    try:
        async with ClientSession() as client:
            async with client.get(url=url, headers=headers) as responce:
                if responce.status == 200:
                    data = await responce.json()
                    return data
            logging.warning('Админ успешно получил промокоды')
    except Exception as e:
        logging.error(f'Ошибка при получении пользователей: {e}')
        
async def get_promocodes_by_title(title: str):
    url = f'{base_url}/get_promocode_by_title?promocode_title={title}'
    headers = {'Content-Type': 'application/json'}
    try:
        async with ClientSession() as client:
            async with client.get(url=url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if isinstance(data, list):
                        promocodes = [promo['promocode'] for promo in data]
                        return promocodes
                    else:
                        return data['promocode'] 
                    
            logging.warning('Админ успешно получил промокоды по данной категории')
    except Exception as e:
        logging.error(f'Ошибка получения промокодов по категории: {e}')        
