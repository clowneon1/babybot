from utils import keep_alive, bot
import os

bot = bot.Bot()
TOKEN = os.environ.get("TOKEN")

def main():
    keep_alive.keep_alive()
    bot.run(TOKEN)

if __name__=="__main__":
    main()