"""
Created July 21st, 2017
Program: Executes arbitrage trades on Poloniex cryptocurrency market.
@author: Charles Zhang
"""

import requests
import ast
import numpy as np
import time
import pandas as pd
import datetime
now = datetime.datetime.now()

import urllib
import urllib2
import json
import hmac,hashlib

# Sources
inputDirectory = 'Input//'
input_canvas = inputDirectory + 'canvas.csv'
# Transforms csv files to data frames
canvas = pd.read_csv(input_canvas, encoding="ISO-8859-1",low_memory = False)
outputDirectory = 'Output//'
class poloniex:
    def __init__(self):
        self.APIKey = ''
        self.Secret = ''

    def post_process(self, before):
        after = before

        # Add timestamps if there isnt one but is a datetime
        if ('return' in after):
            if (isinstance(after['return'], list)):
                for x in xrange(0, len(after['return'])):
                    if (isinstance(after['return'][x], dict)):
                        if ('datetime' in after['return'][x] and 'timestamp' not in after['return'][x]):
                            after['return'][x]['timestamp'] = float(createTimeStamp(after['return'][x]['datetime']))

        return after

    def api_query(self, command, req={}):
        if (command == "returnTicker" or command == "return24Volume"):
            ret = urllib.urlopen(urllib.Request('https://poloniex.com/public?command=' + command))
            return json.loads(ret.read())
        elif (command == "returnOrderBook"):
            ret = urllib.urlopen(urllib.Request(
                'https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair'])))
            return json.loads(ret.read())
        elif (command == "returnMarketTradeHistory"):
            ret = urllib2.urlopen(urllib2.Request(
                'https://poloniex.com/public?command=' + "returnTradeHistory" + '&currencyPair=' + str(
                    req['currencyPair'])))
            return json.loads(ret.read())
        else:
            req['command'] = command
            req['nonce'] = int(time.time() * 1000)
            post_data = urllib.urlencode(req)

            sign = hmac.new(self.Secret, post_data, hashlib.sha512).hexdigest()
            headers = {
                'Sign': sign,
                'Key': self.APIKey
            }
            ret = requests.post('https://poloniex.com/tradingApi', data=req, headers=headers)

            #ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
            jsonRet = json.loads(ret.text)
            return self.post_process(jsonRet)

    # Returns all of your balances.
    # Outputs:
    # {"BTC":"0.59098578","LTC":"3.31117268", ... }
    def returnBalances(self):
        return self.api_query('returnBalances')
    # Places a buy order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
    # Inputs:
    # currencyPair  The curreny pair
    # rate          price the order is buying at
    # amount        Amount of coins to buy
    # Outputs:
    # orderNumber   The order number
    def buy(self,currencyPair,rate,amount):
        return self.api_query('buy',{"currencyPair":currencyPair,"rate":rate,"amount":amount})

    # Places a sell order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
    # Inputs:
    # currencyPair  The curreny pair
    # rate          price the order is selling at
    # amount        Amount of coins to sell
    # Outputs:
    # orderNumber   The order number
    def sell(self,currencyPair,rate,amount):
        return self.api_query('sell',{"currencyPair":currencyPair,"rate":rate,"amount":amount})

p = poloniex()

def ticker(c1,c2,c3):#c1 and c3 must both be exchanges
    ex11 = ""
    ex12 = ""
    ex21 = ""
    ex22 = ""
    ex31 = ""
    ex32 = ""

    # 1 = buy, 2 = sell
    move1 = 0
    move2 = 0
    move3 = 0
    if ("usdt" in c1 or "usdt" in c2):
        if "usdt" in c1:
            ex11 = c1
            ex12 = c2
        elif "usdt" in c2:
            ex11 = c2
            ex12 = c1
    elif ("btc" in c1 or "btc" in c2):
        if "btc" in c1:
            ex11 = c1
            ex12 = c2
        elif "btc" in c2:
            ex11 = c2
            ex12 = c1
    elif ("eth" in c1 or "eth" in c2):
        if "eth" in c1:
            ex11 = c1
            ex12 = c2
        elif "eth" in c2:
            ex11 = c2
            ex12 = c1
    elif ("xmr" in c1 or "xmr" in c2):
        if "xmr" in c1:
            ex11 = c1
            ex12 = c2
        elif "xmr" in c2:
            ex11 = c2
            ex12 = c1
            
    if ("usdt" in c2 or "usdt" in c3):
        if "usdt" in c2:
            ex21 = c2
            ex22 = c3
        elif "usdt" in c3:
            ex21 = c3
            ex22 = c2
    elif ("btc" == c2 or "btc" == c3):
        if "btc" in c2:
            ex21 = c2
            ex22 = c3
        elif "btc" in c3:
            ex21 = c3
            ex22 = c2
    elif ("eth" in c2 or "eth" in c3):
        if "eth" in c2:
            ex21 = c2
            ex22 = c3
        elif "eth" in c3:
            ex21 = c3
            ex22 = c2
    elif ("xmr" in c2 or "xmr" in c3):
        if "xmr" in c2:
            ex21 = c2
            ex22 = c3
        elif "xmr" in c3:
            ex21 = c3
            ex22 = c2

    if ("usdt" in c3 or "usdt" in c1):
        if "usdt" in c3:
            ex31 = c3
            ex32 = c1
        elif "usdt" in c1:
            ex31 = c1
            ex32 = c3
    elif ("btc" in c3 or "btc" in c1):
        if "btc" in c3:
            ex31 = c3
            ex32 = c1
        elif "btc" in c1:
            ex31 = c1
            ex32 = c3
    elif ("eth" in c3 or "eth" in c1):
        if "eth" in c3:
            ex31 = c3
            ex32 = c1
        elif "eth" in c1:
            ex31 = c1
            ex32 = c3
    elif ("xmr" in c3 or "xmr" in c1):
        if "xmr" in c3:
            ex31 = c3
            ex32 = c1
        elif "xmr" in c1:
            ex31 = c1
            ex32 = c3

    t1 = ex11 + "_" + ex12
    t2 = ex21 + "_" + ex22
    t3 = ex31 + "_" + ex32

    move1 = 1
    if ex12 == ex21:
        move2 = 1 #buy
    else:
        move2 = 2 #sell

    if ex32 == ex11:
        move3 = 1 #buy
    else:
        move3 = 2 #sell

    moves = [move1,move2,move3]
    trades = [t1,t2,t3]
    return {'moves':moves,'trades':trades}

#returns the exchange rate of a currency pair for a buy/sell
def exrate(exchange,currencypair,buy_sell):
    currencypair = currencypair.upper()
    ask_bid = ""
    if (buy_sell == 1):
        ask_bid = "lowestAsk"
    elif (buy_sell == 2):
        ask_bid = "highestBid"
    rate = exchange.get(currencypair).get(ask_bid)
    return rate

etc = np.empty(shape = (7,3))
list= ["btc"] * 15
list2 = ["etc","gno","gnt","lsk","rep","steem","zec","bcn","blk","btcd","dash","ltc","maid","nxt","zec"]
list3 = ["eth","eth","eth","eth","eth","eth","eth","xmr","xmr","xmr","xmr","xmr","xmr","xmr","xmr"]

def sell_amount(currency):
    balances = p.returnBalances()
    amount_currency = balances.get(currency)
    print(amount_currency)

#executes trade based on buy/sell, currency pair, exchange rate, and amount
def executetrade(buy_sell,l_currencyPair,rate,number):
    rate = float(rate)
    number = float(number)
    currencyPair = l_currencyPair.upper()
    amount = 0
    if buy_sell == "1":
        amount = number/rate
        print(currencyPair)
        print(rate)
        print(amount)
        #print(p.buy(currencyPair,rate,amount))
    elif buy_sell == "2":
        sell_currency = currencyPair.split("_",1)[1]
        amount = sell_amount(sell_currency)
        print(currencyPair)
        print(rate)
        print(amount)
        #print(p.sell(currencyPair, rate, amount))
executetrade(2,"BTC_ZEC",)
finalcount = 0
num_trades = 0
start_amount = 0.0002 # IN BTC
while finalcount < 10000:
    response = str(requests.get('https://poloniex.com/public?command=returnTicker').content)
    string_dict = response[:len(response)]
    #print(string_dict)
    exchange = ast.literal_eval(string_dict)

    count = 0
    product = [0] * 15
    master_moves = [None] * 15
    master_trades = [None] * 15
    master_rates = [0] * 15
    master_amount = [None] * 15
    while count <= 14:
        c1 = list[count]
        c2 = list2[count]
        c3 = list3[count]

        control = ticker(c1, c2, c3)
        moves = control.get('moves')
        master_moves[count] = moves
        trades = control.get('trades')
        master_trades[count] = trades

        count2 = 0
        rates = [0, 0, 0]
        values = [0,0,0]
        amount = [start_amount,0,0]
        while count2 <= 2:
            rates[count2] = float(exrate(exchange, trades[count2], moves[count2]))
            if moves[count2] == 2:
                values[count2] = float(exrate(exchange, trades[count2], moves[count2]))
            elif moves[count2] == 1:
                values[count2] = 1 / float(exrate(exchange, trades[count2], moves[count2]))
            if count2 < 2:
                amount[count2+1] = amount[count2] * values[count2]

            count2 += 1
        product[count] = values[0] * values[1] * values[2]
        master_amount[count] = amount
        master_rates[count] = rates
        count += 1

    count3 = 0
    highest = 0
    highest_index = -1
    while count3 <= 14:
        # if product[count3] > 1.01:
        if product[count3] > highest:
            highest = product[count3]
            highest_index = count3
        # print("----")
        # print(master_trades[count3])
        # print(master_moves[count3])
        # print(product[count3])
        # print("----")
        count3 += 1
    time.sleep(1)
    #canvas.loc[finalcount,'return'] = highest

    print("---")
    print(finalcount)
    print(master_moves[highest_index])
    print(master_trades[highest_index])
    print(highest)
    print(finalcount)
    print(highest)
    if (highest > 1):
        print("---")
        executetrade(str(master_moves[highest_index][0]),str(master_trades[highest_index][0]),str(master_rates[highest_index][0]),str(master_amount[highest_index][0]))
        executetrade(str(master_moves[highest_index][1]),str(master_trades[highest_index][1]),str(master_rates[highest_index][1]),str(master_amount[highest_index][1]))
        executetrade(str(master_moves[highest_index][2]),str(master_trades[highest_index][2]),str(master_rates[highest_index][2]),str(master_amount[highest_index][2]))
        print("---")

        print("---")
        print("Trade 1:")
        print("currencyPair: " + str(master_trades[highest_index][0]))
        print("rate: " + str(master_rates[highest_index][0]))
        print("amount: " + str(master_amount[highest_index][0]))
        print("buy_sell: " + str(master_moves[highest_index][0]))
        print("---")
        print("Trade 2:")
        print("currencyPair: " + str(master_trades[highest_index][1]))
        print("rate: " + str(master_rates[highest_index][1]))
        print("amount: " + str(master_amount[highest_index][1]))
        print("buy_sell: " + str(master_moves[highest_index][1]))

        print("---")
        print("Trade 3:")
        print("currencyPair: " + str(master_trades[highest_index][2]))
        print("rate: " + str(master_rates[highest_index][2]))
        print("amount: " + str(master_amount[highest_index][2]))
        print("buy_sell: " + str(master_moves[highest_index][2]))
        print("---")
        print("EXECUTED!!!")
        print(p.returnBalances())
        quit()
    finalcount +=1

#canvas.to_csv(outputDirectory + "results.csv")


