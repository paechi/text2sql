import clickhouse_connect
from dotenv import load_dotenv
import os

load_dotenv()


username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
host = os.environ.get("HOST")
port = os.environ.get("PORT")
dbname = os.environ.get("DBNAME")

client = clickhouse_connect.get_client(host=host, port=int(port), username=username, password=password, database=dbname)
client.command("CREATE DATABASE IF NOT EXISTS marketing_data")
client.command('''
CREATE TABLE IF NOT EXISTS marketing_data.analytics (
    date Date,
    platform String,
    customer_id Int32,
    clicks Int32,
    visits Int32,
    cpc Float32
    ) ENGINE = MergeTree()
ORDER BY (date, customer_id)
''')

client.command('''
INSERT INTO marketing_data.analytics (date, platform, customer_id, clicks, visits, cpc)
VALUES
    ('2022-01-01', 'Google', 1, 10, 100, 0.5),
    ('2022-01-02', 'Bing', 2, 15, 150, 0.7),
    ('2022-01-01', 'Facebook', 3, 5, 50, 0.3),
    ('2022-01-10', 'Google', 4, 12, 120, 0.6),
    ('2022-01-15', 'Bing', 5, 8, 80, 0.4),
    ('2022-01-23', 'LinkedIn', 6, 6, 60, 0.2),
''')