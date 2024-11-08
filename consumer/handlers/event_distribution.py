from consumer.handlers.create_recipe import create_recipe
from consumer.handlers.login import login

async def handle_event_distribution(body):
    match body['action']:
        case 'login':
            await login(body)
        case 'create_recipe':
            await create_recipe(body)