import binance_account

class DataManager():
    """This class should manage/match all strategies agaisnt all incoming data streams"""
    def __init__(self,period=1):
        self.period = period #used to determine update freq/period


    def update_asset_price(self,asset):
        pass

    def update_account_balance(self,account):
        pass

    def update_account_positions(self,account):
        pass

    def updates_all
