from vkbottle import Keyboard, KeyboardButtonColor, Text
from src.commands import HelpCommand, GetPasswordCommand


KEYBOARD_ENTRYPOINT = Keyboard(inline=False, one_time=True)
for command in [GetPasswordCommand, HelpCommand]:
    KEYBOARD_ENTRYPOINT.add(
        Text(command.button_name, payload={'cmd': command.key}),
        color=KeyboardButtonColor.SECONDARY
    )
