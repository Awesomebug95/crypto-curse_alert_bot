import time
import logging
import requests

NOW = int(time.time())
PAST_TIME = NOW - 3600  # Промежуток времени, за который сравниваются курсы.

# ---Список api_id (coingecko) криптовалют
CASE = [
    '1inch', 'cardano', 'my-neighbor-alice', 'automata', 'cosmos',
    'avalanche-2', 'bella-protocol', 'bittorrent-2', 'celer-network',
    'civic', 'dogecoin', 'polkadot', 'elrond-erd-2', 'ellipsis',
    'ethereum-classic', 'fetch-ai', 'force-protocol', 'helium',
    'internet-computer', 'linear', 'chainlink', 'litentry', 'ethereum',
    'livepeer', 'terra-luna', 'terra-luna', 'matic-network',
    'mina-protocol', 'harmony', 'reef-finance', 'rif-token',
    'thorchain', 'ravencoin', 'the-sandbox', 'shiba-inu', 'bitcoin',
    'smooth-love-potion', 'solana', 'elrond-erd-2', 'litentry',
    'alien-worlds', 'tron', 'trust-wallet-token', 'uniswap',
    'vechain', 'waves', 'stellar', 'tezos', 'zcash', 'zenfuse'
]


def main():
    """
    Парсит api по заданным настройкам,
    оповещает о изменениях курса.
    """
    while True:
        case = CASE
        for coin in range(len(case)):
            url = f'https://api.coingecko.com/api/v3/coins/{case[coin]}/mar' \
                  f'ket_chart/range?vs_currency=usd&from={PAST_TIME}&to={NOW}'
            response = requests.get(url).json()
            prices = response.get('prices')
            old_price = prices[0][1]
            new_price = prices[-1][1]
            cost_difference = new_price - old_price
            alert_border = (old_price / 100) * 1  # цифрой после * устанавливается граница изменения курса в %
            if cost_difference > 0 and cost_difference >= alert_border:
                print(f'🟢Цена 🔺{case[coin]} поднялась на: {round(cost_difference, 4)}$ за час 🔺🟢')
            if 0 > cost_difference <= -alert_border:
                print(f'🔴Цена 🔻{case[coin]} упала на: {round(cost_difference, 4)}$ за час 🔻🔴')

            time.sleep(3)  # Задержка в секундах между запросами.
        time.sleep(3449)  # Задержка в запросах между циклами.


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(__file__ + '.log')
        ],
        format='%(asctime)s, %(levelname)s, %(name)s, %(lineno)s, %(message)s,'
    )
    main()
