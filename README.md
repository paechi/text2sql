# text2sql

This repository implements text2sql task using Langchain and Clickhouse. In particular, I use llm to generate SQL queries given a particular prompt. The results shows that 6/7 test questions are syntactically correct, but note that they may be logically correct.

## Install the dependencies

- Create a new virtual/conda environment (I use Python 3.9.6)
```
python3 -m venv venv
source venv/bin/activate 
```
- Install necessary libraries using pip.
```
pip3 install -r requirements.txt
```

## Prepare database

- I used clickhouse_connect to create the database on python, but use can do it on the clikchouse website.

```
python3 database.py
```
- You can run `text2sql.py` to check how langchain's SQLDatabaseChain works with test questions given a prompt. 
```
python3 text2sql.py
```
- You can also run `app.py` and give your own question. The input should be a dict, which specifies the SQL dialect, table names and the question itself. For example: {"dialect":"sqlite", "table_info": "analytics", "input":"How many active agency customers did we have on January 1st, 2022?"}
```
python3 app.py
```
![app_output](result/app_output.png)

- You might need to provide you own openai key in .env file. I am planning to try other prompts and llms for this task. For now, the results are encouraging.