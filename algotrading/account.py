import gdax
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



class GdaxAccount(Account):

    def __init__(self,sandbox=True):
        self.last_updated = 'xxx'
        self.sandbox = sandbox
        #gdax sandbox cred
        self.api_key = '515a1f417f15a4ccc3371740c8181b65'
        self.api_secret = 'FZ77gPfzMoff9/tDH6iBpEw6U0CPdJIoqABWji4c5n6g1fdTUFxyfFLyp1+Fep/LFT756M85nhduCbewav4F1A=='
        self.api_pass = '251cs3trop9'

        self._init_client()

    def _init_client(self):
        url = "https://api.gdax.com"
        if self.sandbox:
             url = "https://api-public.sandbox.gdax.com"
        self.client_public = gdax.PublicClient()
        self.client_private = gdax.AuthenticatedClient(
                              self.api_key,self.api_secret,self.api_pass,url)

    def get_price(self,symbol):
        if symbol.upper() == "BTC":
            symbol = "BTC-USD"
        elif symbol.upper() == "ETH":
            symbol = "ETH-USD"
            return 0 # ETH not yet available
        elif symbol.upper() == "LTC":
            symbol = "LTC-USD"
            return 0 # LTC not yet available
        elif symbol.upper() == "USD":
            return 1
        order_book = self.client_private.get_product_order_book(symbol)
        price = float(order_book['asks'][0][0])
        return price


    def get_net_value(self):
        total = 0
        symbols = ["USD","BTC"]
        for symbol in symbols:
            price = self.get_price(symbol)
            balance = self.get_positions(symbol)
            usd_value = price * balance
            total += usd_value
        return total

    def get_balance(self,symbol):
        """return 'available' balance"""
        account_all = self.client_private.get_accounts()
        fn = lambda x:x['currency'].upper() == symbol.upper()
        account = list(filter(fn,account_all))[0]
        available = float(account['available'])
        return available

    def get_positions(self,symbol):
        """return current balance"""
        positions = self.client_private.get_position()
        balance = float(positions['accounts'][symbol]["balance"])
        return balance


    def place_order(self,order_type,price='market',size=0.0,symbol='BTC-USD'):
        """start here"""
        if price == 'market':
            price = self.get_price(symbol)
        if order_type.upper() == 'BUY':
            self.client_private.buy(price=price,
                                size=size,
                                product_id=symbol)


        if order_type.upper() == 'SELL':
            self.client_private.sell(price=price,
                                size=size,
                                product_id=symbol)
