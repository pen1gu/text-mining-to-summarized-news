import pandas as pd
import json
from sqlalchemy import create_engine

with open("db_info.json", "r") as f:
    db_info = json.loads(f.read())

db_id = db_info["id"]
db_psw = db_info["psw"]
db_name = db_info["db_name"]

db_connection_str = f"mysql+pymysql://{db_id}:{db_psw}@127.0.0.1/{db_name}"
db_connection = create_engine(db_connection_str)

pd.DataFrame().to_sql(
    name="test_table", con=db_connection, if_exists="replace", index=False
)

