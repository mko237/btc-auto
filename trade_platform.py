class TradePlatform():

    def __init__(self,account,market):
        self.account = account
        self.market = market

    def get_state(self):
        state = []
        state.extend(self.account.get_state())
        state.extend(self.market.get_state())
        return state
    def next_state(self):
        pass

    def open_long_pos(self,symbol,quantity,stop_loss_percent=None,take_profit_percent=None):
        curr_price = self.account.get_price(symbol)
        if stop_loss_percent:
            stop_loss = curr_price - (curr_price * stop_loss_percent)
        else:
            stop_loss = None
        if take_profit_percent:
            take_profit = curr_price + (curr_price * take_profit_percent)
        else:
            take_profit = None
        self.account.place_order('BUY',symbol=symbol,quantity=quantity,stop_loss=stop_loss,take_profit=take_profit)

    def open_short_pos(self,symbol,quantity,stop_loss_percent=None,take_profit_percent=None):
        curr_price = self.account.get_price(symbol)
        if stop_loss_percent:
            stop_loss = curr_price + (curr_price * stop_loss_percent)
        else:
            stop_loss = None
        if take_profit_percent:
            take_profit = curr_price - (curr_price * take_profit_percent)
        else:
            take_profit = None
        self.account.place_order('SELL',symbol=symbol,quantity=quantity,stop_loss=stop_loss,take_profit=take_profit)

    def close_pos(self,symbol):
        cur_pos = self.account.client.pos_direction
        quantity = abs(cur_pos)
        if cur_pos > 0:
            self.account.place_order('SELL',symbol=symbol,quantity=quantity)
        if cur_pos < 0:
            self.account.place_order('BUY',symbol=symbol,quantity=quantity)

    def perform_action(self):
        pass

