# coding=utf-8
import requests
import psycopg2

url = 'https://api.upbit.com/v1/market/all'
queryString = {"isDetails":"false"}
response = requests.request("GET", url, params=queryString)
print(response.text)

insert_market_json_query = f"""
insert into crawling_upbit_fact (sequence_number, response_json) values (1,'{response.text}')
"""
delete_market_json_query = f"""delete from crawling_upbit_fact"""

delete_market_code_query = f"""delete from code_group where group_name = 'market'"""
insert_market_code_query = f"""
insert into code_group(group_name ,code_key ,code_value_char_1)
	select 'market', replace(cast(res->'market' as varchar),'"','') , replace(cast(res->'korean_name' as varchar),'"','')
	from (
	select JSON_ARRAY_ELEMENTS(response_json) res 
	from crawling_upbit_fact
	) aa
"""
host_address = ''
conn = psycopg2.connect(host=host_address, dbname='botdb', user='coinbot', password='', port='5432')
cur = conn.cursor()
print(delete_market_json_query)
cur.execute(delete_market_json_query)
print(insert_market_json_query)
cur.execute(insert_market_json_query)
conn.commit()

print(delete_market_code_query)
cur.execute(delete_market_code_query)
print(insert_market_code_query)
cur.execute(insert_market_code_query)
conn.commit()
cur.close()
conn.close()


"""
min_price	max_price	order_unit
 2,000,000 	 99,999,999,999 	 1,000 
 1,000,000 	 2,000,000 	 500 
 500,000 	 1,000,000 	 100 
 100,000 	 500,000 	 50 
 10,000 	 100,000 	 10 
 1,000 	 10,000 	 5 
 100 	 1,000 	 1 
 10 	 100 	 0.1 
 - 	 10 	 0.01 
"""
"""
def set_auto_order(market_name):
    auto_order_insert = f"""
    insert into code_group (group_name , code_key , code_value_char_1, code_value_int_1)
    values ('auto_order', {market_name}, 'on',1)
    """
    cur.execute(auto_order_insert)
    conn.commit()
"""
