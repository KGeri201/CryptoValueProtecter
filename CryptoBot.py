import yaml
from binance.client import Client

def main(config = None):
    #client = Client(config["api_key_test"], config["api_secret_test"], testnet=True)
    client = Client(config["api_key"], config["api_secret"])
    all_coins = client.get_all_tickers()
    for item in all_coins:
        print(item["symbol"]+": "+str(float(item["price"])))
    print(all_coins)
    #client.get_historical_klines("BTCBUSD", "1m",start,end)

if __name__ == "__main__":
    try:
        main(yaml.load(open(r'config.yaml'), Loader=yaml.FullLoader))
    except:
        pass
