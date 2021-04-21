import psycopg2
import pyupbit
import os
import time
from time import sleep
import logging.handlers
import logging

log_handlers = [logging.handlers.RotatingFileHandler(filename='/home/coinbot/log.txt', maxBytes=1024*1024*10), logging.StreamHandler()]
logging.basicConfig(level = logging.INFO, format = '%(asctime)s [%(levelname)s] : %(message)s', handlers = log_handlers)
logger = logging.getLogger('auto_trade_logger')

upbit = pyupbit.Upbit(os.environ['accesskey'], os.environ['secretkey'])
max_buy_limit = 20000
max_sell_limit_rate = 1.05
max_auto_trade_sceond = 60*60*6
loop_auto_trade_second = 0
wait_second = 10

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

def get_element_include(source_list, match_attribute, find_value):
    return_value=0
    for source in source_list:
        if source[match_attribute] == find_value:
            return_value = return_value + 1
    return return_value

def get_element_value(source_list, match_attribute, find_value, return_attribute):
    return_value = ''
    for source in source_list:
        if source[match_attribute] == find_value:
            return_value = source[return_attribute]
            break
    return return_value

auto_trade_list_query = f"""
select code_key, count(*) cnt from code_group where group_name ='auto_order' group by code_key having count(*) > 1
"""
def delete_auto_trade_market(code_key):
    delete_auto_trade_list_query = f"""
    delete from code_group where group_name ='auto_order' and code_key ='{code_key}'
    """
    logger.info(delete_auto_trade_list_query)
    cur.execute(delete_auto_trade_list_query)
    conn.commit()

def insert_trade_transaction_log(transaction_type, market_code, order_result):
    insert_trade_transaction_log_query = f"""
    insert into trade_transaction_log ('{transaction_type}', '{market_code}', '{order_result}')
    """
    logger.info(insert_trade_transaction_log_query)
    cur.execute(insert_trade_transaction_log_query)
    conn.commit()

while True:
    try:
        #자동 매매 대상 목록 조회
        cur.execute(auto_trade_list_query)
        logger.info(auto_trade_list_query)
        auto_trade_list = cur.fetchall()
        logger.info(auto_trade_list)
        #미체결 목록 조회 후 반복 매수/매도
        for auto_trade in auto_trade_list:
            non_trade_list = upbit.get_order(auto_trade[0])
            wait_buy_trade = get_element_include(non_trade_list, 'side', 'ask') #매수 미체결 개수
            wait_sell_trade = get_element_include(non_trade_list, 'side', 'bid') #매도 미체결 개수
            current_unit_price = pyupbit.get_current_price(auto_trade[0])
            if wait_buy_trade > 0 and wait_sell_trade == 0: #미체결 매도가 없고 매수가 있다면 바로 매도
                sell_unit_price = get_tick_size(pyupbit.get_current_price(auto_trade[0]), max_sell_limit_rate)
                sell_order_result = upbit.sell_limit_order(auto_trade[0], sell_unit_price, auto_trade['volume'])
                insert_trade_transaction_log('sell', auto_trade[0], sell_order_result)
            elif wait_buy_trade == 0 and wait_sell_trade == 0: #미체결 매수/매도가 없다면 최대 정해진 금액 이하로 매수
                buy_order_result = upbit.buy_limit_order(auto_trade[0], current_unit_price, round(max_buy_limit / current_unit_price,6))
                insert_trade_transaction_log('buy', auto_trade[0], buy_order_result)
            elif wait_buy_trade == 0 and wait_sell_trade > 0: #미체결 매수가 없고 매도만 있다면 정해진 시간이 지난 후 자동매매 대상에서 삭제 미체결 주문도 취소
                loop_auto_trade_second = loop_auto_trade_second + wait_second
                if loop_auto_trade_second >= max_auto_trade_sceond:
                    cancel_uuid = get_element_value(non_trade_list, 'side', 'bid', 'uuid')
                    cancel_order_result = upbit.cancel_order(cancel_uuid)
                    insert_trade_transaction_log('cancel', auto_trade[0], cancel_order_result)
                    delete_auto_trade_market(auto_trade[0])
                    loop_auto_trade_second = 0
        logger.debug('waiting seconds : ' + wait_second)
        sleep(wait_second)
    except Exception as ex:
        logger.error(str(ex))

cur.close()
conn.close()
"""
#ret = upbit.buy_limit_order("KRW-XRP", 50, 100)
#print(ret)
#ret = upbit.sell_limit_order("KRW-XRP", 100000, 1)
#print(ret)
#ret = upbit.sell_limit_order("KRW-XRP", 1000, 20)
print(upbit.get_balance(ticker='KRW-XRP'))
#print(pyupbit.get_orderbook(tickers="KRW-BTC"))
ret=upbit.get_order("KRW-XRP")
print(ret)
#print(upbit.cancel_order(ret[0]['uuid']))
print(pyupbit.get_current_price("KRW-XRP"))

CREATE TABLE public.trade_transaction_log (
	transaction_type varchar(30) NULL,
	market_coin varchar(30) NULL,
	response_json json NULL,
	create_date timestamp NULL DEFAULT CURRENT_TIMESTAMP
);
"""
