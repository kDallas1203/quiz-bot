import telegram
class UserHasNoQuestion(Exception):
    pass

class TelegramUserHasNoQuestion(telegram.TelegramError):
    pass
