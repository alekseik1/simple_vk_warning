class CommandBase:
    key: str
    raw_message_name: str
    button_name: str
    description: str


class HelpCommand(CommandBase):
    key = 'help'
    raw_message_name = 'помощь'
    button_name = 'Помощь'
    description = 'Напечатать список всех команд'


class GetPasswordCommand(CommandBase):
    key = 'get_password'
    raw_message_name = 'пароль'
    button_name = 'Мой пароль'
    description = 'Получить логин и пароль для экстренной авторизации'


available_commands = [HelpCommand, GetPasswordCommand]
