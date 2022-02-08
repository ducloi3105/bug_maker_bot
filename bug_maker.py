import logging
from random import randrange
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import TELEGRAM_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class BugMakerBot(object):
    foods = []

    def start(self, update, context):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def help(self, update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text(
            '1. /start\n'
            '2. /help\n'
            '3. /show_foods\n'
            '4. /add_food <food name>\n'
            '5. /reset_food\n'
            '6. /pick_food'
        )

    def echo(self, update, context):
        """Echo the user message."""
        update.message.reply_text('Command not found')

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update {} caused error {}'.format(update, context.error))

    def show_foods(self, update, content):
        message = self.create_menu()
        return update.message.reply_text(message)

    def create_menu(self, ):
        if not self.foods:
            message = 'Menu empty, call /add_food <food>'
        else:
            message = ''
            for index, item in enumerate(self.foods):
                index += 1
                message += f'{index}. {item}.\n'
        return message

    def add_food(self, update, content):
        print(update, content)
        food = update.message.text or ''
        if not food:
            return update.message.reply_text('Please input the food: /add_food <food_name>')

        food = food[10:]
        self.foods.append(food)

    def remove_food(self, update, content):
        food = update.message.text or ''
        try:
            number = int(food[12:])
            self.foods.pop(number - 1)
        except:
            return update.message.reply_text('Cannot remove food, index must number or not out of range')

        message = self.create_menu()
        return update.message.reply_text(message)

    def reset_food(self, update, content):
        self.foods = []
        update.message.reply_text('Menu empty now!')

    def pick_food(self, update, content):
        if not self.foods:
            return update.message.reply_text('Menu empty!')

        range_foods = randrange(len(self.foods))
        food = self.foods[range_foods]
        update.message.reply_text(food)


def main():
    '''Start the bot.'''
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    bug_maker_bot = BugMakerBot()
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('start', bug_maker_bot.start))
    dp.add_handler(CommandHandler('help', bug_maker_bot.help))
    dp.add_handler(CommandHandler('show_foods', bug_maker_bot.show_foods))
    dp.add_handler(CommandHandler('add_food', bug_maker_bot.add_food))
    dp.add_handler(CommandHandler('pick_food', bug_maker_bot.pick_food))
    dp.add_handler(CommandHandler('remove_food', bug_maker_bot.remove_food))
    dp.add_handler(CommandHandler('reset_food', bug_maker_bot.reset_food))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, bug_maker_bot.echo))

    # log all errors
    dp.add_error_handler(bug_maker_bot.error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
