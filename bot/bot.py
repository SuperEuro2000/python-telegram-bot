import random
import nltk
import json
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


with open('BOT_CONFIG.json', 'r') as f:
  BOT_CONFIG = json.load(f)

# with open('/content/BOT_CONFIG.json', 'w') as f:
#   json.dump(BOT_CONFIG, f, ensure_ascii=False, indent=3)



X = []
y = []

for intent in BOT_CONFIG['intents'].keys():
    try:
      if intent != 'other':
        for example in BOT_CONFIG['intents'][intent]['examples']:
            X.append(example)
            y.append(intent)
    except:
      print(BOT_CONFIG['intents'][intent])


len(X), len(y)


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)


vectorizer = CountVectorizer(ngram_range=(2, 4), analyzer='char')
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)
len(vectorizer.get_feature_names())


clf = LogisticRegression().fit(X_train_vectorized, y_train)
# clf = RandomForestClassifier(n_estimators=200).fit(X_train_vectorized, y_train)


clf.score(X_train_vectorized, y_train)
# 0.8422174840085288 LogReg_base


clf.score(X_test_vectorized, y_test)
# 0.2297872340425532 LogReg_base


clf.predict(vectorizer.transform(['откуда ты?']))


def get_intent_by_model(text):
  return clf.predict(vectorizer.transform([text]))[0]



def bot(input_text):
  intent = get_intent_by_model(input_text)
  print(intent)
  return random.choice(BOT_CONFIG['intents'][intent]['responces'])


BOT_CONFIG['intents']['payment']


input_text = ''
while input_text != 'Завершить работу':
  input_text = input()
  print(bot(input_text))




# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(bot(update.message.text))


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1947061307:AAFd7UgS46rKFCqmuS1mXUPn8qug7mMHVIo")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()