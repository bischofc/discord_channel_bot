import os
import sys
from src.discord_channel_bot import run

if __name__ == '__main__':

    # Get bot login token
    if len(sys.argv) == 2:
        token = sys.argv[1]
    else:
        token = os.getenv("DC_BOT_TOKEN")
    if not token:
        sys.exit("No token found: Please pass as argument or set environment variable DC_BOT_TOKEN")

    run(token)
