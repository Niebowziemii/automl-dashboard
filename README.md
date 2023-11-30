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
## Chart Descriptions

### Calendar Heatmap
The *Calendar Heatmap* presents daily sales on a calendar, filtered by product categories (FOODS, HOUSEHOLD, HOBBIES). Users can select a specific category for focused analysis.

### Products Correlation
The *Products Correlation* plot unveils the correlation between a random subset (default: 100) of products. This analysis is instrumental in identifying potential relationships or patterns in sales behavior, offering valuable insights for analytical purposes.

### Sales Distribution
The *Sales Distribution* plot visualizes aggregate sales over time, providing filtering options for product categories, states, and stores. Users can explore trends in sales for random samples, gaining detailed insights into sales dynamics.

### Sales Heatmap
The *Sales Heatmap* dynamically illustrates product sales for a random subset (default: 100) over a specified time span (default: 300 days). This plot offers a comprehensive view of product sales distribution and is customizable for varying subsets.

### Stores Boxplot
The *Stores Boxplot* summarizes aggregate sales for the three categories (FOODS, HOUSEHOLD, HOBBIES) across different stores. This plot provides a comparative view of sales distribution, contributing to an understanding of store-specific sales dynamics.
