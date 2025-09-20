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
<img width="720" height="194" alt="image" src="https://github.com/user-attachments/assets/0e948376-29bd-4f7f-adfa-c25abbf14413" />


Explanation:
- app presents 3 interactive visualizations: monthly revenue (line), top products (bar), revenue by region (pie).
- Forecast: trains a RandomForestRegressor on monthly aggregated revenue using lag features. It predicts next 3 months.
- Dropdown filters cross-update all charts (cross-filtering).
<img width="1354" height="524" alt="image" src="https://github.com/user-attachments/assets/ebb4aaf5-27ca-4894-aba4-f8712db8a2db" />

<img width="1069" height="493" alt="image" src="https://github.com/user-attachments/assets/b983466f-bab2-488f-87e9-f5369ac74498" />

<img width="991" height="466" alt="image" src="https://github.com/user-attachments/assets/a632ad8a-6326-4d05-b383-ad653bcb2fab" />


