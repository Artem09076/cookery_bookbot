from consumer.handlers.login import login
from consumer.handlers.all_ids import admin

async def handle_event_distribution(body):
    match body['action']:
        case 'login':
            await login(body)
        # case 'admin':
        #     await admin(body)