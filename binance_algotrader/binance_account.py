import os
from binance.websockets import BinanceSocketManager
import configparser
from binance.client import Client
from datetime import datetime

class Account():

    def __init__(self):
        self.last_updated = 'xxx'



    def get_balance(self):
        pass

    def get_positions(self):
        pass

    def get_net_value(self):
        pass
    def place_order(self,type,size):
        pass



class BinanceAccount(Account):

    def __init__(self,sandbox=True):
        self.last_updated = 'xxx'
        self.sandbox = sandbox
        #gdax sandbox cred
        config = configparser.ConfigParser()
        cur_dir = os.path.dirname(__file__)
        config.read(os.path.join(cur_dir,"config.txt"))
        self.api_key = config.get("binance","key")
        self.api_secret = config.get("binance","secret")
        self.api_pass = ''

        self._init_client()

    def _init_client(self):
        self.client = Client(self.api_key,self.api_secret)
        self.socket_manager = BinanceSocketManager(self.client)
    def get_price(self,symbol):
        if symbol.upper() == "BTC":
            symbol = "BTCUSDT"
        elif symbol.upper() == "ETH":
            symbol = "ETHUSDT"
        order_book = self.client.get_orderbook_ticker(symbol=symbol)
        price = float(order_book['askPrice'])
        return price

    def get_net_value(self,itemized=False):
        """Get value of all owned assets in USD.
        params:
            itemized : bool : if False (default) return total account value in dollars (int)
                              if True, return dictionary of each assets value`{asset:usd}`
        """

        base_asset = "BTCUSDT"
        current_base_price = self.get_price(base_asset)
        # is_held = lambda x: float(x["free"]) + float(x["locked"]) > 0
        # all_assets = self.client.get_account()
        # owned_assets = filter(is_held,all_assets["balances"])
        owned_assets = self.get_balance()
        asset_usd = {}
        for asset,asset_value in owned_assets.items():
            asset_name = asset + base_asset[:3]
            try:
                asset_base_price = self.get_price(asset_name)
                usd_amt = asset_value*asset_base_price*current_base_price
                asset_usd[asset] = usd_amt
            except Exception as e:
                asset_usd[asset] = 0
        if itemized:
            total = asset_usd
        else:
            total = reduce(lambda x,y: y+x,[i for i in asset_usd.values()])
        return total

    def get_balance(self,symbol=None):
        """Get balance of free coins.
        params:
            symbol : str : if None, returns all free coins and their balance in a dictionary.p
                           else returns the balance of inputted coin.
        """
        is_held = lambda x: float(x["free"]) + float(x["locked"]) > 0
        all_assets = self.client.get_account()
        owned_assets = filter(is_held,all_assets["balances"])

        if symbol is not None:
            symbol = symbol.upper()[:3] # only take first three of symbol i.e. ETH isntead of ETHBTC
            fn = lambda x: x["asset"] == symbol
            asset_value = filter(fn,owned_assets)
            asset_value.append(0) # add 0 to list in case symbol not owned
            total = float(asset_value[0])
        else:
            total = {x["asset"]:float(x["free"]) for x in owned_assets}
        return total

    def get_positions(self,symbol):
        """return current positions"""
        pass

    def place_order(self,order_type,quantity,symbol):
        """Places an order.
        params:
            order_type  : str :   if "BUY", Buys quantity amount of symbol.
                                  if "SELL", Sells quantity amount of symbol.
            quantity    : float : how much you want to buy or sell.
            symbol      : str :   ex. ETHBTC
        """
        if order_type.upper() == "BUY":
            order = self.client.order_market_buy(
                                                    symbol=symbol,
                                                    quantity=quantity)
        elif order_type.upper() == "SELL":
            order = self.client.order_market_sell(
                                                    symbol=symbol,
                                                    quantity=quantity)
        else:
            order = "Something is wrong!"

        return order

    def process_message(self,msg):
        os.system('clear')
        print("message type: {}".format(msg['e']))
        print(msg)

    def start_ticker_stream(self,symbol,callback=None):
        if callback is None:
            self.process_message
        self.socket_manager.start_symbol_ticker_socket(symbol,callback)
        self.socket_manager.start()

    def stop_socket_stream(self):
        self.socket_manager.close()

    def start_kline_stream(self,symbol):
        self.socket_manager.start_kline_socket(symbol,self.process_message)
        self.socket_manager.start()
 
    def start_multi_stream(self,streams,callback=None):
        if callback is None:
            self.process_message
        self.socket_manager.start_multiplex_socket(streams,callback)
        self.socket_manager.start()
