from .checkbooknyc import CheckbookNYC
from .utils import psql_insert_copy
import json
import pandas as pd
import datetime
from sqlalchemy import create_engine
from multiprocessing import Pool
from pathlib import Path
import os
from . import BUILD_ENGINE


def check_table_existence(engine, name):
    r = engine.execute(
        """
        select * from information_schema.tables 
        where table_name='%(name)s'
        """
        % {"name": name}
    )
    return bool(r.rowcount)


def get_records(d: str):
    engine = create_engine(BUILD_ENGINE)
    search_criteria = {"issue_date": d}
    c = CheckbookNYC(type_name="Spending", search_criteria=search_criteria)
    a = c()
    results = []
    for i in a:
        results += i['response']['result_records']['spending_transactions']['transaction']

    df = pd.DataFrame(results)
    if df.shape[0] > 0:
        if check_table_existence(engine, 'capital_spending'):
            engine.execute(
                f"DELETE FROM capital_spending WHERE issue_date = '{d}'")
        df.to_sql(
            'capital_spending',
            con=BUILD_ENGINE,
            if_exists="append",
            index=False,
            method=psql_insert_copy,
        )
        # output_file_dir = f'.output/date={d}/output.csv'
        # os.makedirs(Path(output_file_dir).parent, exist_ok=True)
        # df.to_csv(f'.output/date={d}/output.csv')


if __name__ == '__main__':
    start = datetime.datetime.strptime("2009-12-22", "%Y-%m-%d")
    end = datetime.datetime.now()
    dates = [start + datetime.timedelta(days=x)
             for x in range(0, (end-start).days)]
    dates_formated = [d.strftime("%Y-%m-%d") for d in dates]
    with Pool(5) as p:
        p.map(get_records, dates_formated)
