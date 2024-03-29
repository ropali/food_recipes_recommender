# -*- coding: utf-8 -*-
from pathlib import Path
from ..database.models import RecipeModel
import pandas as pd
from ..utils.logger import Logger
import sys
from .scrapper import start_scrapper

logger = Logger(__name__, std_out=True)


def table_to_csv(query, db_con, save_path):
    df = pd.read_sql_query(query, db_con)
    logger.info(f'Saving raw data into {save_path}')
    df.to_csv(save_path,index=False)


def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """

    save_path = 'data/raw/data.csv'

    model = RecipeModel()
    
    if model.all():
        table_to_csv(f'select * from {model.TABLE_NAME}', model.con,save_path)
        return
     
    user_input = input('Local database is empty. Would you like to start scrapping the data from source?(Y/N) : ')

    if not user_input:
        print('Invalid input! Exiting script...')
        sys.exit()

    if user_input.lower() == 'y':
        start_scrapper()
        
        table_to_csv(f'select * from {model.TABLE_NAME}', model.con,save_path)

    sys.exit()


       


if __name__ == '__main__':

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    main()
