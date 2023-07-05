from dotenv import load_dotenv
import clickhouse_connect
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate
import sqlalchemy as sa
import json
import os
import ast

load_dotenv()

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
DBNAME = os.environ.get("DBNAME")

_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}

Question: {input}"""

def read_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def write_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)


def check_llm_res(filepath):
    data = read_json(filepath)
    command, command_res = data['sql'], data['result']
    client = clickhouse_connect.get_client(host=HOST, port=int(PORT), username=USERNAME, password=PASSWORD, database=DBNAME)
    try:
        query_result = client.query(command)
        res = query_result.result_rows
    except:
        print("There is an error with the LLM generated SQL query")
        res = None
    # llm_res = ast.literal_eval(command_res)
    if res is None or str(res) != command_res:
        return 0
    else:
        return 1


def run_text2sql(questions):
    url = f'clickhouse+http://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?protocol=https'
    db = SQLDatabase.from_uri(url)
    llm = OpenAI(temperature=0)
    PROMPT = PromptTemplate(
        input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
    )
    db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, prompt=PROMPT, verbose=True, return_intermediate_steps=True)

    idx = 0
    count = 0
    for question in questions:
        res = db_chain(question)
        d = {'sql': res['intermediate_steps'][0], 'result': res['intermediate_steps'][1]}
        res_filepath = os.path.join('results', 'question_' + str(idx) + '.json')
        write_json(res_filepath, d)
        res = check_llm_res(res_filepath)
        count += res
        idx += 1

    print(f"Percentage of syntactically accurate queries for questions: {(count/len(questions))} %")


if __name__ == "__main__":
    questions = ['How many active agency customers did we have on January 1st, 2022?',
                 'When did we get the highest number of users per day in Q1 2023?',
                 'When did we get the maximum of daily visits on the website in 2022?',
                 'What was the average CPC in Google Ads in April 2023?',
                 'How many LinkedIn clicks did we have in 2022?',
                 'Which platform had the highest CPC in 2022: Google or Bing?',
                 'Get the best ad name by clicks from Facebook, Google, and LinkedIn for 2022.']

    run_text2sql(questions)