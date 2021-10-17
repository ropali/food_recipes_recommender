
from pathlib import Path
import pandas as pd
from ..utils.logger import Logger
import re
import numpy as np


class FeatureBuilder:
    data_file = Path('data/processed/data.csv')

    required_features = ['recipe','title', 'summary','ingredients']
    
    def __init__(self,df: pd.DataFrame):
        self.logger = Logger(__name__, __name__ == '__main__')

        self.df = df


    def build(self):
        """Build features for recommender system"""

        self.logger.info(f"Starting feature building...")

        """
            Convert all the features into list & join them to form
            a new feature called 'tags' which will be used
            to caclulate the similarity for recommender system.
        """

        new_df = self.df.copy()[self.required_features]

        
        new_df['recipe'] = new_df.recipe.str.split(' ')
        new_df['title'] = new_df.title.str.split(' ')
        new_df['summary'] = new_df.summary.str.split(' ')
        new_df['ingredients'] = new_df.ingredients.str.split(' ')
        

        self.df['tags'] = new_df.recipe + new_df.title + new_df.summary + new_df.ingredients
       
        
        self.logger.info(f"Finished feature building...")

        return self.df

    


if __name__ == '__main__':
    data_file = Path('data/processed/data.csv')

    if not data_file.exists():
        raise FileNotFoundError(f"Could not find {data_file}.")

    df = pd.read_csv(str(data_file))
        
    FeatureBuilder(df).build()
