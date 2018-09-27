from  binance_account_btest import BinanceAccount,Client
from scratch import HistoryClient
from time import sleep
import pickle

with open('data_test.pkl','rb') as f:
    TEST_MARKET_DATA=pickle.load(f) #HistoryClient().get_data(interval_mins=5,total_days=1)
print(len(TEST_MARKET_DATA))


def setup_acc():
    b_acc = BinanceAccount(get_data=False)
    b_acc.client.market.set_data(TEST_MARKET_DATA)
    return b_acc

def setup_client():
    cl = Client('key','secret',get_data=False)
    cl.market.set_data(TEST_MARKET_DATA)
    return cl

def test_get_orderbook_ticker():
    c = setup_client()
    out = c.get_orderbook_ticker('btc')
    assert "askPrice" in out
    assert isinstance(out["askPrice"],float)

def test_order_market_buy():
    c = setup_client()
    prev_balance = c.account["balances"][1]["free"]
    c.order_market_buy('btc',.01)
    curr_balance = c.account["balances"][1]["free"]
    assert curr_balance > prev_balance

def test_order_market_sell():
    c = setup_client()
    c.order_market_buy('btc',.01)
    prev_balance = c.account["balances"][1]["free"]
    c.order_market_sell("btc",.01)
    curr_balance = c.account["balances"][1]["free"]
    assert curr_balance < prev_balance

def test_get_price():
    b_acc = setup_acc()
    price = b_acc.get_price('BTC')
    assert isinstance(price,float)

def test_get_net_value():
    b_acc = setup_acc()
    b_acc.client._init_account(1000)
    value = b_acc.get_net_value()
    assert int(value) == 1000

def test_get_balance():
    b_acc = setup_acc()
    b_acc.client._init_account(1000)
    value = b_acc.get_balance(symbol='BTC')
    assert value == 0

def test_place_order():
    b_acc = setup_acc()
    b_acc.client._init_account(1000)
    b_acc.place_order("buy",.01,'btc')
    assert b_acc.get_balance("btc") == .01

def test_place_order_1():
    b_acc = setup_acc()
    b_acc.client._init_account(1000)
    b_acc.place_order("buy",.01,'btc')
    b_acc.place_order("sell",.01,'btc')
    assert b_acc.get_balance("btc") == 0
