from binance_account_btest import BinanceAccount
from trade_platform import TradePlatform
import pickle

def setup_accnt():
    accnt = BinanceAccount(get_data=False)
    with open('data_test.pkl','rb') as f:
        accnt.client.market.set_data(pickle.load(f))
    return accnt
def setup_tp():
    accnt = setup_accnt()
    mkt = accnt.client.market
    tp = TradePlatform(accnt,mkt)
    return tp

TP = setup_tp()

def test_get_state():
    state = TP.get_state()
    assert len(state) > 0

def test_open_long_pos():
    old_pos = TP.account.client.pos_direction

    TP.open_long_pos('btc',8)

    new_pos = TP.account.client.pos_direction
    assert new_pos > old_pos

def test_open_long_pos_2():

    TP.open_long_pos('btc',8,stop_loss_percent=.5,take_profit_percent=.5)
    price = TP.account.get_price('btc')

    assert TP.account._stop_loss == price*.5
    assert TP.account._take_profit == price*1.5

def test_open_short_pos():
    old_pos = TP.account.client.pos_direction

    TP.open_short_pos('btc',8)

    new_pos = TP.account.client.pos_direction
    assert new_pos < old_pos

def test_open_short_pos_2():

    TP.open_short_pos('btc',8,stop_loss_percent=.5,take_profit_percent=.5)
    price = TP.account.get_price('btc')

    assert TP.account._stop_loss == price*1.5
    assert TP.account._take_profit == price*.5

def test_close_pos():
    TP.open_long_pos('btc',9)
    TP.close_pos('btc')
    new_pos = TP.account.client.pos_direction
    assert new_pos == 0
