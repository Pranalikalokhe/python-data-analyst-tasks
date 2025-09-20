Task 2: Descriptive & Predictive Analysis Dashboard
--------------------------------------------------
Files:
- generate_sales_data.py  -> creates sales_data.csv (synthetic)
- app.py                  -> Dash app (interactive + prediction)

Dependencies:
- pandas, dash, plotly, scikit-learn, joblib

Run:
1) python generate_sales_data.py
2) python app.py
Open: http://127.0.0.1:8050

Explanation:
- app presents 3 interactive visualizations: monthly revenue (line), top products (bar), revenue by region (pie).
- Forecast: trains a RandomForestRegressor on monthly aggregated revenue using lag features. It predicts next 3 months.
- Dropdown filters cross-update all charts (cross-filtering).
