from dotenv import load_dotenv
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
import sqlalchemy as sa
import json
import os

load_dotenv()

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
host = os.environ.get("HOST")
port = os.environ.get("PORT")
dbname = os.environ.get("DBNAME")

url = f'clickhouse+http://{username}:{password}@{host}:{port}/{dbname}?protocol=https'
db = SQLDatabase.from_uri(url)
llm = OpenAI(temperature=0)

PROMPT = """Given an input question, create a syntactically correct {dialect} query to run.
    Use the following format:

    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"
    Answer: "Final answer here"

    Only use the following tables:

    {table_info}

    Question: {input}
    """
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True,return_intermediate_steps=True)

def text2sql():
    print("Type 'exit' to quit")
    # {"dialect":"MySQL", "table_info": "analytics", "input":"How many active agency customers did we have on January 1st, 2022?"}
    while True:
        inp = input("Enter a question: ")
        if inp.lower() == 'exit':
            print('Exiting...')
            break
        else:
            try:
                d = json.loads(inp)
                question = PROMPT.format(dialect=d['dialect'],
                                        table_info=d['table_info'],
                                        input=d['input'])
                print(db_chain.run(question))
            except Exception as e:
                print(e)

text2sql()