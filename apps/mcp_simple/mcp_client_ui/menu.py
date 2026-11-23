import json

import questionary

EXIT = object()


async def choose_tool(tools):
    choices = [questionary.Choice(title=tool.name, value=tool) for tool in tools]
    choices.append(questionary.Choice(title='Exit', value=EXIT))
    selected = await questionary.select(
        'Choose a tool (use the arrow keys and Enter):', choices=choices
    ).ask_async()
    return None if selected is EXIT else selected


async def get_arguments(tool):
    if tool.name == 'led_control':
        action = await questionary.select(
            'Choose an LED action:', choices=['on', 'off', 'toggle', 'Back']
        ).ask_async()
        if action is None or action == 'Back':
            return None
        return {'action': action}

    if tool.name == 'delayed_response':
        message = await questionary.text(
            'Message (optional):'
        ).ask_async()
        if message is None:
            return None
        return {'message': message} if message else {}

    # Unknown tools can still be called using the input schema from the server.
    print('Tool input schema:')
    print(json.dumps(tool.input_schema, indent=2))
    while True:
        raw = await questionary.text(
            'Arguments as a JSON object:', default='{}'
        ).ask_async()
        if raw is None:
            return None
        try:
            arguments = json.loads(raw)
        except json.JSONDecodeError:
            print('Please enter valid JSON, for example {"action": "on"}.')
            continue
        if isinstance(arguments, dict):
            return arguments
        print('Arguments must be a JSON object, for example {}.')


def print_result(result):
    print('Response:')
    for item in result.content:
        text = getattr(item, 'text', None)
        print(text if text is not None else item)
