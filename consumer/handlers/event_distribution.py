from consumer.handlers.login import login


async def handle_event_distribution(body):
    match body['action']:
        case 'login':
            await login(body)