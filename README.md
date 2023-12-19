# automl-dashboard

## The input file structure should be added like here: 
```
automl-dashboard
├── input
│   └── m5-forecasting-accuracy
│       ├── calendar.csv
│       ├── sales_train_evaluation.csv
│       ├── sales_train_validation.csv
│       ├── sample_submission.csv
│       └── sell_prices.csv
...
```
Download input data [here](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data)

## To run the app use the following:

in /automl-dashboard:

```bash

python -m pipenv install
python -m pipenv run streamlit run main.py
```
