import time
import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, executor

import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

CHAT_ID = config.CHAT_ID
ADMIN = config.ADMIN

# ---SETTINGS---

CHANGE_RATE = 5  # difference of the exchange rate as a percentage
DELAY_REQUESTS = 3  # delay between requests in a cycle
DELAY_CYCLES = 3449  # delay between cycles
COMPARISON_TIME_DIFF = 3600  # delay between course checks

# ---List api_id (coingecko) cryptocurrency

CASE = [
    '1inch', 'cardano', 'my-neighbor-alice', 'automata', 'cosmos',
    'avalanche-2', 'bella-protocol', 'bittorrent-2', 'celer-network',
    'civic', 'dogecoin', 'polkadot', 'elrond-erd-2', 'ellipsis',
    'ethereum-classic', 'fetch-ai', 'force-protocol', 'helium',
    'internet-computer', 'linear', 'chainlink', 'ethereum',
    'livepeer', 'terra-luna', 'terra-luna', 'matic-network',
    'mina-protocol', 'harmony', 'reef-finance', 'rif-token',
    'thorchain', 'ravencoin', 'the-sandbox', 'shiba-inu', 'bitcoin',
    'smooth-love-potion', 'solana', 'elrond-erd-2', 'litentry',
    'alien-worlds', 'tron', 'trust-wallet-token', 'uniswap',
    'vechain', 'waves', 'stellar', 'tezos', 'zcash', 'zenfuse'
]


async def main():
    """
    Parses the api according to the specified settings,
    notifies of course changes by a message in a telegram.
    """
    message = f'Bot run with change rate {CHANGE_RATE}%' \
              f' and time step {COMPARISON_TIME_DIFF}.'
    await bot.send_message(chat_id=CHAT_ID, text=message)
    while True:
        now = int(time.time())
        past_time = now - COMPARISON_TIME_DIFF
        case = CASE
        for coin in range(len(case)):

            url = f'https://api.coingecko.com/api/v3/coins/{case[coin]}/market_chart/range?vs_currency=usd&from={past_time}&to={now}'
            response = requests.get(url).json()
            prices = response.get('prices')
            old_price = prices[0][1]
            new_price = prices[-1][1]
            cost_difference = new_price - old_price
            alert_border = (old_price / 100) * CHANGE_RATE
            if cost_difference > 0 and cost_difference >= alert_border:
                text = f'🚀Цена 🔺{case[coin]} поднялась на: {round(cost_difference, 4)}$ за час 🔺🚀'
                await bot.send_message(chat_id=CHAT_ID, text=text)
            # down_cost_difference = new_price - old_price
            if 0 > cost_difference <= -alert_border:
                text = f'Цена 🔻{case[coin]} упала на: {round(cost_difference, 4)}$ за час 🔻'
                await bot.send_message(chat_id=CHAT_ID, text=text)
            time.sleep(DELAY_REQUESTS)  # Delay in seconds between requests.
        time.sleep(DELAY_CYCLES)  # Delay in requests between cycles.


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(__file__ + '.log')
        ],
        format='%(asctime)s, %(levelname)s, %(name)s, %(lineno)s, %(message)s,'
    )
    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(main())
    main_loop.run_forever()
    executor.start_polling(dp, skip_updates=True)

