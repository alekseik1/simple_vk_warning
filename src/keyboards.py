from vkbottle import Keyboard, KeyboardButtonColor, Text
from src.commands import HelpCommand, GetPasswordCommand, AdminOpenLock


KEYBOARD_ENTRYPOINT = Keyboard(inline=False, one_time=True)
KEYBOARD_ENTRYPOINT.add(
    Text(AdminOpenLock.button_name, payload={'cmd': AdminOpenLock.key}), color=KeyboardButtonColor.PRIMARY
)
KEYBOARD_ENTRYPOINT.row()
for command in [GetPasswordCommand, HelpCommand]:
    KEYBOARD_ENTRYPOINT.add(
        Text(command.button_name, payload={'cmd': command.key}),
        color=KeyboardButtonColor.SECONDARY
    )
