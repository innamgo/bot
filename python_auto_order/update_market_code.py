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
host_address = 'ec2-52-78-17-156.ap-northeast-2.compute.amazonaws.com'
conn = psycopg2.connect(host=host_address, dbname='botdb', user='coinbot', password='Mzc!1025', port='5432')
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
