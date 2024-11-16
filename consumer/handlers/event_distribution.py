from consumer.handlers.create_recipe import create_recipe
from consumer.handlers.find_receipt import find_receipt
from consumer.handlers.get_info_ab_receipt import on_message
from consumer.handlers.get_receipts import get_receipts
from consumer.handlers.like_dislike import like_dislike
from consumer.handlers.login import login


async def handle_event_distribution(body):
    match body['action']:
        case 'login':
            await login(body)
        case 'create_recipe':
            await create_recipe(body)
        case 'find':
            await find_receipt(body)
        case 'get_receipts':
            await get_receipts(body)
        case 'like' | 'dislike':
            await like_dislike(body)
        case 'info_receipts':
            await on_message(body)
