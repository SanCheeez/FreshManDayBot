from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
import logging
TOKEN = "6628777326:AAER9OJhVbyviUdyhQMlW3e-4Mqj6vEEfSw"
HINTS = {'пассатижи': '1.mp4',
         'бочка': '2.2.mp4',
         'балалайка': '4.mp4',
         'шаттл': '5.mp4',
         'паж': '6.mp4',
         'воспоминание': '7.mp4',
         'пирс': '8.mp4',
         'владивосток': '9.mp4',
         'экзамен': '9.mp4',
         'двфу': '9.mp4',
         'сырник': '10.mp4',
         'кукурузник': '11.mp4',
         'улитка': '12.mp4',
         'проводник': '13.mp4',
         'гладиолус': '14_1.mp4',
         'близко': '15.mp4',
         'ИМКТ': 'secret.mp4'}
TEAMS = {}


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def check_id(id: int):
    return True if id in TEAMS.values() else False


def help(update: Update, context):
    update.message.reply_text(
        '''
/help  -- Показывает все команды для бота.
/map -- Показывает карту.
/hint <код> -- Ввод кода для подсказки.
        '''
    )


def create_team(update: Update, context):
    if not check_id(update.effective_chat.id):
        team = update.message.text.replace("/create_team", "").strip()
        if not team:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Введите название команды")
            return
        if team not in TEAMS.keys():
            TEAMS[team] = update.effective_chat.id
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Ваша команда создана")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Команда с таким названием уже создана")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Вы уже создали команду")


def get_all_teams(update: Update, context):
    if not check_id(update.effective_chat.id):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Вы ещё не создали команду")
        return
    teams = ""
    for team, id in TEAMS.items():
        teams += team + " -- " + str(id) + "\n"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Список команд:\n {teams}")


def map(update: Update, context):
    # if not check_id(update.effective_chat.id):
    #     context.bot.send_message(chat_id=update.effective_chat.id,
    #                              text="Вы ещё не создали команду")
    #     return
    map_path = "map.jpg"
    update.message.reply_photo(open(map_path, "rb"), caption="Карта местности")


def hint(update: Update, context):
    # if not check_id(update.effective_chat.id):
    #     context.bot.send_message(chat_id=update.effective_chat.id,
    #                              text="Вы ещё не создали команду")
    #     return
    secret_code = update.message.text.replace("/hint", "").strip().lower()
    response = HINTS.get(secret_code)
    if response:
        update.message.reply_video(
            open(response, "rb"), caption="Держи подсказку")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Код неверный")


def start(update: Update, context: CallbackContext):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    update.message.reply_text(
        '''
Приветствую, я буду вашим помощником в этом путешествии. Я помогу вашей команде добраться до цели, но вам нужно ввести нужный набор команд.

/help  -- Показывает все команды для бота.
/map -- Показывает карту.
/hint <код> -- Ввод кода для подсказки.
        '''
    )


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    # dispatcher.add_handler(CommandHandler('create_team', create_team))
    # dispatcher.add_handler(CommandHandler('get_all_teams', get_all_teams))
    dispatcher.add_handler(CommandHandler('map', map))
    dispatcher.add_handler(CommandHandler('hint', hint))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
