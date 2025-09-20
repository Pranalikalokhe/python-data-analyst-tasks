"""
app.py
Dash app: interactive visualizations + a simple predictive model (monthly revenue forecast)

Run:
python task2_dashboard/app.py
Then open: http://127.0.0.1:8050
"""

import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from joblib import dump
import dash
from dash import html, dcc, Output, Input
import plotly.express as px

# Load data
DATA_PATH = os.path.join(os.path.dirname(__file__), "sales_data.csv")
df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()

# Aggregate helper
def aggregate(filtered_df):
    monthly = filtered_df.groupby("Month", as_index=False).agg({"Revenue": "sum"})
    monthly = monthly.sort_values("Month").reset_index(drop=True)
    return monthly

# Dash app
app = dash.Dash(__name__, title="Sales Dashboard (Descriptive + Predictive)")

app.layout = html.Div([
    html.H2("📊 Sales Dashboard — Descriptive & Predictive"),
    html.Div([
        html.Label("Region"),
        dcc.Dropdown(
            options=[{"label": "All", "value": "All"}] +
                    [{"label": r, "value": r} for r in sorted(df["Region"].unique())],
            value="All", id="region-filter"
        ),
        html.Label("Product (multi)"),
        dcc.Dropdown(
            options=[{"label": p, "value": p} for p in sorted(df["Product"].unique())],
            value=[], multi=True, id="product-filter"
        ),
        html.Button("Refresh / Re-run prediction", id="refresh-btn"),
    ], style={"width": "25%", "display": "inline-block", "verticalAlign": "top", "padding": "10px"}),

    html.Div([
        dcc.Graph(id="monthly-line"),
        dcc.Graph(id="top-products-bar"),
        dcc.Graph(id="region-pie")
    ], style={"width": "70%", "display": "inline-block", "padding": "10px"}),

    html.Div(id="prediction-output", style={"padding": "20px"})
])

# Feature preparation for prediction
def prepare_features(monthly_df, n_lags=3):
    monthly_df = monthly_df.copy().sort_values("Month").reset_index(drop=True)
    for lag in range(1, n_lags + 1):
        monthly_df[f"lag_{lag}"] = monthly_df["Revenue"].shift(lag)
    monthly_df["month_num"] = monthly_df["Month"].dt.month
    monthly_df["year"] = monthly_df["Month"].dt.year
    monthly_df = monthly_df.dropna().reset_index(drop=True)

    X = monthly_df[[f"lag_{i}" for i in range(1, n_lags + 1)] + ["month_num", "year"]]
    y = monthly_df["Revenue"]
    return monthly_df, X, y

# Training + forecasting
def train_and_forecast(monthly_df, n_lags=3, predict_steps=3):
    if monthly_df.empty or len(monthly_df) < (n_lags + 1):
        return None, "Not enough data to train predictive model."

    monthly, X, y = prepare_features(monthly_df, n_lags=n_lags)
    if len(X) < 2:
        return None, "Not enough data for training."

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    last_row = monthly_df.sort_values("Month").iloc[-n_lags:]["Revenue"].tolist()
    preds = []
    for step in range(predict_steps):
        features = last_row[-n_lags:]
        month_num = (monthly_df["Month"].max() + pd.DateOffset(months=step + 1)).month
        year = (monthly_df["Month"].max() + pd.DateOffset(months=step + 1)).year

        # Use DataFrame to avoid sklearn warning
        X_pred = pd.DataFrame(
            [features + [month_num, year]],
            columns=[f"lag_{i}" for i in range(1, n_lags + 1)] + ["month_num", "year"]
        )
        next_pred = float(model.predict(X_pred)[0])
        preds.append({
                "Month": (monthly_df["Month"].max() + pd.DateOffset(months=step + 1)),
                "PredictedRevenue": round(next_pred, 2)
            })
        last_row.append(next_pred)
    return preds, None

# Callback
@app.callback(
    [Output("monthly-line", "figure"),
     Output("top-products-bar", "figure"),
     Output("region-pie", "figure"),
     Output("prediction-output", "children")],
    [Input("region-filter", "value"),
     Input("product-filter", "value"),
     Input("refresh-btn", "n_clicks")]
)
def update_dashboard(region_value, product_values, _):
    try:
        d = df.copy()
        if region_value and region_value != "All":
            d = d[d["Region"] == region_value]
        if product_values:
            d = d[d["Product"].isin(product_values)]

        if d.empty:
            empty_fig = px.scatter(title="⚠️ No data available")
            return empty_fig, empty_fig, empty_fig, html.Div("⚠️ No data for selected filters")

        # Monthly revenue
        monthly = aggregate(d)
        fig_line = px.line(monthly, x="Month", y="Revenue", title="Monthly Revenue")

        # Top products
        top_products = d.groupby("Product", as_index=False).agg({"Revenue": "sum"}) \
                        .sort_values("Revenue", ascending=False).head(10)
        fig_bar = px.bar(top_products, x="Product", y="Revenue", title="Top Products by Revenue")

        # Region share
        region_share = d.groupby("Region", as_index=False).agg({"Revenue": "sum"})
        fig_pie = px.pie(region_share, names="Region", values="Revenue", title="Revenue Share by Region")

        # Forecast
        preds, err = train_and_forecast(monthly)
        if err:
            pred_text = html.Div([html.H4("Prediction"), html.P(err)])
        else:
            pred_rows = [
                html.Tr([html.Td(p["Month"].strftime("%Y-%m")), html.Td(f"{p['PredictedRevenue']:.2f}")])
                for p in preds
            ]
            pred_table = html.Table([
                html.Thead(html.Tr([html.Th("Month"), html.Th("Predicted Revenue")])),
                html.Tbody(pred_rows)
            ])
            pred_text = html.Div([html.H4("Next 3 months forecast"), pred_table])

        return fig_line, fig_bar, fig_pie, pred_text

    except Exception as e:
        empty_fig = px.scatter(title="⚠️ Error")
        return empty_fig, empty_fig, empty_fig, html.Div(f"⚠️ Error in callback: {str(e)}")

# Run app
if __name__ == "__main__":
    app.run(debug=True)
