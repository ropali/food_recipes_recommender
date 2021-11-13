import pandas as pd
import numpy as np
from ..data.preprocessing import Preprocessor
from ..features.build_features import FeatureBuilder
from ..utils.logger import Logger
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle



def main():
    logger = Logger(__name__, __name__ == '__main__')

    df = pd.read_csv('data/raw/data.csv')

    preprocessor = Preprocessor(df)

    cleaned_df = preprocessor.start()

    feat_builder = FeatureBuilder(cleaned_df)

    processed_df = feat_builder.build()

    logger.info(f'Training Data Points {processed_df.shape}')

    
    cv = CountVectorizer(max_features=5000,stop_words='english')

    vector = cv.fit_transform(processed_df['tags']).toarray()

    similarity = cosine_similarity(vector)
    
    model_path = 'models/similarity.pkl'
    
    pickle.dump(similarity,open(model_path,'wb'))
    
    logger.info(f'Similarity Model Saved at {model_path}')


if __name__ == '__main__':
    main()
