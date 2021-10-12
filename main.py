from utils.keep_alive import keep_alive
from utils.bot import Bot
import os


bot = Bot()
TOKEN = os.environ.get("TOKEN")

def main():
    keep_alive()
    bot.run(TOKEN)

if __name__=="__main__":
    main()