import psycopg2
import logging
import pyupbit
import os

upbit = pyupbit.Upbit(os.environ['accesskey'], os.environ['secretkey'])
max_buy_limit = 20000
#ret = upbit.buy_limit_order("KRW-XRP", 50, 100)
#print(ret)
#ret = upbit.sell_limit_order("KRW-XRP", 100000, 1)
#print(ret)
#ret = upbit.sell_limit_order("KRW-XRP", 1000, 20)
print(upbit.get_balance(ticker='KRW-XRP'))
"""
#print(pyupbit.get_orderbook(tickers="KRW-BTC"))
ret=upbit.get_order("KRW-XRP")
print(ret)
#print(upbit.cancel_order(ret[0]['uuid']))

print(pyupbit.get_current_price("KRW-XRP"))

conn = psycopg2.connect(host='localhost', dbname='botdb', user='coinbot', password='Mzc!1025', port='5432')
cur = conn.cursor()

def get_tick_size(price, increase):
    if price >= 2000000:
        tick_size = round(price * increase / 1000) * 1000
    elif price >= 1000000:
        tick_size = round(price * increase / 500) * 500
    elif price >= 500000:
        tick_size = round(price * increase / 100) * 100
    elif price >= 100000:
        tick_size = round(price * increase / 50) * 50
    elif price >= 10000:
        tick_size = round(price * increase / 10) * 10
    elif price >= 1000:
        tick_size = round(price * increase / 5) * 5
    elif price >= 100:
        tick_size = round(price * increase / 1) * 1
    elif price >= 10:
        tick_size = round(price * increase / 0.1) * 0.1
    else:
        tick_size = round(price * increase / 0.01) * 0.01
    return tick_size

높은 변동성 추천 2회 이상 리스트: select
    미체결 목록 조회 upbit.get_order("KRW-XRP")
    if len(미체결목록) == 0 and upbit.get_balance(ticket='KRW-XRP') ==0:
        매수 print(round(max_buy_limit/pyupbit.get_current_price("KRW-XRP")))
    elif 미체결목록[0]['side']='ask' and 미체결목록[0]['side']='wait' and len(미체결목록) == 1:
        print('wait')
    else:
        매도 
"""
