Food And Recipe Recommender System
==================================

A recommender system to recommend foods with the recipe based on the food you have already tried.

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py


--------
## Installation
Clone this repo in your local machine. Create a virtual environment to install the packages like this,

```
> virtualenv venv
```
After it successfully creates virtual environment then activate it.

```
> source venv/bin/activate # for linux

> .\venv\Scripts\actiavet # for windows
```

Now install all the require packages from `requirements.txt` file like this,

```> pip install -r requirements.txt```


## Dataset
This repo already contains the data in `data/raw/data.csv` which you can directly use. Or you can scrape the data directly from the source using the script.The orinal way to generate a dataset is to collect a data from source and store it in the sqlite database & then export the dataset into .csv file.
To scrape the data from source, run this command.
```
> python -m src.data.scrapper
```
To create the dataset as `.csv` file run this command,
```
> python -m src.data.make_dataset
```


## Training Model
To train the model you can start the training by using this command,
```
> python -m src.models.train_model
```
All the in between steps like pre-processing,feature engineering, etc will be performed automatically. All the generated models will be saved in `models` directory.

The recommender model will be created by using the `similarity` matrix method. 


## Visualization
Don't have any visualization right now but you can add your own if you want.


## Logging 
All the operations will be logged in the `debug.log` file which will be generated automatically once you start running the code.
