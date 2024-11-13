from consumer.handlers.create_recipe import create_recipe
from consumer.handlers.get_receipts import get_receipts
from consumer.handlers.like_dislike import like_dislike
from consumer.handlers.login import login
from consumer.handlers.all_ids import admin
from consumer.handlers.find_receipt import find_receipt

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
        case 'like':
            await like_dislike(body)
        case 'dislike':
            await like_dislike(body)
        # case 'admin':
        #     await admin(body)
