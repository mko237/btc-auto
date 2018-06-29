# This is the main file to be executed

from asset import Asset
from data_manager import DataManager
from account import Account
from strategy import Strategy

#init vars
datam = DataManager(period=1) # update speriod = 1m ?

all_accnts = [] #put accounts here
all_assets = [] #put assests here



def main():
    while True:
        datam.update_all(accnts=all_accnts,assets=all_assets)

if __name__ == '__main__':
    main()
