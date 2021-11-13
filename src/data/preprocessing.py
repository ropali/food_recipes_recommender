from pathlib import Path
import pandas as pd
import numpy as np
from src.utils.logger import Logger
import json
import re


class Preprocessor:
    
    cleaned_file = Path('data/processed/data.csv')

    def __init__(self,df: pd.DataFrame):

        self.df = df

        self.logger = Logger(__name__, __name__ == '__main__')
    


    def start(self, save_file=False):
    
        self.logger.info('Starting cleaning process.')
        self._strip_features()
        self._clean_recipe()
        self._clean_title()
        self._clean_summary()
        self._clean_ingred()
        self._clean_nutritions()
        self._remove_duplicates()

        if save_file:
            self.logger.info(f'Saving cleaned file at {self.cleaned_file}')

            self.df.to_csv(str(self.cleaned_file), index=False)

        return self.df

    def _strip_features(self):
        for col in self.df.select_dtypes(include='object').columns:
            self.df[col] = self.df[col].str.strip()

        self.logger.info('Stripping whitespaces from objects columns.')

    def _clean_recipe(self):
        """recipe feature has json objects as string,Let's join all the steps and make a single string value"""
        
        def _clean(val):
            master_string = ""

            dict_ = json.loads(val)

            for k,v in dict_.items():
                # remove "Step {x}" from string 
                master_string += re.sub(r'((step)|(Step)) \d', ' ', v)
        
            return master_string.strip()

        self.df['recipe'] = self.df.recipe.apply(_clean)
        self.logger.info("Cleaned recipe feature...")

    def _clean_title(self):
        """remove unwanted characters from the value"""
        def _clean(val):
            val_str = re.sub(r'[\\(\\)]|(II)', '', val)
            
            return val_str.strip()


        self.df['title'] = self.df.title.apply(_clean)
        self.logger.info("Cleaned title feature...")

    def _clean_summary(self):
        """remove unwanted characters from the value"""
        def _clean(val): 
            val_str = re.sub(r'[\\(\\)]|(II)', '', val)
            
            return val_str.strip()


        self.df['summary'] = self.df.summary.apply(_clean)
        self.logger.info("Cleaned summary feature...")

    def _clean_ingred(self):
        """remove unwanted characters from the value"""
        def _clean(val):
            sub_str = re.sub(r'[0-9]|(-)|[½¾¼⅓]|(Optional)|[\\(\\)]', '', val)

            return sub_str.strip()

        self.df['ingredients'] = self.df.ingredients.apply(_clean)
        self.logger.info("Cleaned ingredients feature...")

    def _clean_nutritions(self):
        """remove 'Per Serving:' and 'Full Nutrition' strings from it"""
        self.df['nutritions'] = self.df.nutritions.apply(lambda x: x.replace('Per Serving:','').replace('Full Nutrition','').strip())
        self.logger.info("Cleaned nutritions feature...")

    def _drop_cols(self):
        """Drop cols which are not required."""
        cols = ['url', 'image_url']

        self.df.drop(columns=cols,inplace=True)

        self.logger.info(f'Dropping {cols} columns.')

    def _remove_duplicates(self):
        dups_count = self.df.duplicated().sum()
        self.logger.info(f'Found {dups_count} duplicate records.')
        
        self.df = self.df.drop_duplicates('title', keep='last')
        self.logger.info('Removed all the duplicates records.')


if __name__ == '__main__':
    data_file = Path('data/raw/data.csv')

    if not data_file.exists():
        raise FileNotFoundError(f"Could not find {data_file}.")

    df = pd.read_csv(str(data_file))

    Preprocessor(df=df).start(save_file=True)
