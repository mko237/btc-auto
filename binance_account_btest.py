import os
from binance.websockets import BinanceSocketManager
import configparser
#from binance.client import Client
from datetime import datetime
from market import Market

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

class Client():
    def __init__(self,key,secret,usd_balance=1000,get_data=False):
        self.account = {}
        self.market = Market(get_data=get_data)
        self._init_account(usd_balance)
        self.pos_direction = 0

    def _init_account(self,usd_balance):
        self.account = {"balances":[{"asset":"USD","free":usd_balance,"locked":0}
                                    ,{"asset":"BTC","free":0,"locked":0}
                                    ,{"asset":"ETH","free":0,"locked":0}
                                    ]
                       }

    def get_orderbook_ticker(self,symbol):
        out = {}
        out['askPrice'] = self.market.get_price(symbol)
        return out

    def get_account(self):
        return self.account

    def _get_symbol_id(self,symbol):
        if symbol.upper() == 'BTC':
            symbol_id = 1
        elif symbol.upper() == 'ETH':
            symbol_id = 2
        return symbol_id

    def order_market_buy(self,symbol,quantity):
        # contact Market, transfer usd to symbol at current price
        price = self.get_orderbook_ticker(symbol)['askPrice']
        #random spread can be introduced here...
        usd_amt = price * quantity
        symbol_id = self._get_symbol_id(symbol)
        self.account["balances"][symbol_id]["free"] += quantity
        self.account["balances"][0]["free"] -= usd_amt
        self.pos_direction += quantity

    def order_market_sell(self,symbol,quantity):
        # contact Market, transfer symbol to usd at current price
        price = self.get_orderbook_ticker(symbol)['askPrice']
        #random spread can be introduced here...
        usd_amt = price * quantity
        symbol_id = self._get_symbol_id(symbol)
        self.account["balances"][symbol_id]["free"] -= quantity
        self.account["balances"][0]["free"] += usd_amt
        self.pos_direction -= quantity



class BinanceAccount(Account):

    def __init__(self,get_data=True):
        #self.last_updated = 'xxx'
        #self.sandbox = sandbox
        #gdax sandbox cred
        #config = configparser.ConfigParser()
        #cur_dir = os.path.dirname(__file__)
        #config.read(os.path.join(cur_dir,"config.txt"))
        #self.api_key = config.get("binance","key")
        #self.api_secret = config.get("binance","secret")
        #self.api_pass = ''
        self._init_client(get_data)
        self._stop_loss = None
        self._take_profit = None

    def _init_client(self,get_data=True):
        self.client = Client('key','secret',get_data=get_data)
        self.socket_manager = BinanceSocketManager(self.client)

    def get_price(self,symbol):
        if symbol.upper() == "BTC":
            symbol = "BTCUSDT"
        elif symbol.upper() == "ETH":
            symbol = "ETHUSDT"
        elif symbol.upper() == "USD":
             symbol = "USDBTCT"
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
            total = sum([i for i in asset_usd.values()])
        return total

    def get_state(self):
        state = []

        money_available = int(self.get_net_value() > 0)
        state.append(money_available)

        short_pos_open = int(self.client.pos_direction < 0)
        state.append(short_pos_open)

        long_pos_open = int(self.client.pos_direction > 0)
        state.append(long_pos_open)

        return state

    def get_balance(self,symbol=None):
        """Get balance of free coins.
        params:
            symbol : str : if None, returns all free coins and their balance in a dictionary.p
                           else returns the balance of inputted coin.
        """
        is_held = lambda x: float(x["free"]) + float(x["locked"]) > 0
        all_assets = self.client.get_account()
        owned_assets = list(filter(is_held,all_assets["balances"]))

        if symbol is not None:
            symbol = symbol.upper()[:3] # only take first three of symbol i.e. ETH isntead of ETHBTC
            fn = lambda x: x["asset"] == symbol
            asset_value = list(filter(fn,owned_assets))# there could be a bug here? need to set asset_value to owned_assests['free']
            if len(asset_value) > 0:
                asset_value = asset_value[0]["free"]
            else:
                asset_value = 0
            #asset_value.append(0) # add 0 to list in case symbol not owned
            total = float(asset_value)
        else:
            total = {x["asset"]:float(x["free"]) for x in owned_assets}
        return total

    def get_positions(self,symbol):
        """return current positions"""
        pass

    def place_order(self,order_type,quantity,symbol,stop_loss=None,take_profit=None):
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

        self._stop_loss = stop_loss
        self._take_profit = take_profit

        return order

    def _set_stop_loss(self,price,symbol):
        self._stop_loss = price

    def _set_take_profit(self,price,symbol):
        self._take_profit = price

    def execute_stop_loss_or_take_profit(self):
        if self.cur_pos > 0:
            self.place_order("SELL",abs(cur_pos),'btc')
        elif self.cur_pos < 0:
            self.place_order("BUY",abs(cur_pos),'btc')

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
