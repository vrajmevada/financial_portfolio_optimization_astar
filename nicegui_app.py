from nicegui import ui
import requests
import numpy as np
import pandas as pd

API_URL = "http://127.0.0.1:8000/api/optimize/"

# ======================
# TITLE
# ======================
ui.label("AI Portfolio Optimization Dashboard (A* Search)") \
    .classes("text-h5 font-mono")

ui.separator()

# ======================
# INPUTS
# ======================
with ui.row():
    tickers_input = ui.input(
        label="Tickers (comma separated)",
        value="AAPL,MSFT,GOOGL,AMZN"
    ).props("dense")

    risk_slider = ui.slider(
        min=0.0,
        max=1.0,
        step=0.05,
        value=0.3
    ).props("label-always")

ui.separator()

# ======================
# OUTPUT SECTIONS
# ======================
summary_box = ui.column()
metrics_box = ui.column()

# ======================
# PNL COMPARISON CHART
# ======================
ui.label("Cumulative PnL Comparison")
pnl_chart = ui.echart({
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["Optimized", "Equal Weight"]},
    "xAxis": {"type": "category", "data": []},
    "yAxis": {"type": "value"},
    "series": [
        {"name": "Optimized", "type": "line", "data": []},
        {"name": "Equal Weight", "type": "line", "data": []},
    ],
})

# ======================
# CORRELATION HEATMAP
# ======================
ui.label("Correlation Heatmap")
corr_chart = ui.echart({
    "tooltip": {"position": "top"},
    "xAxis": {"type": "category", "data": []},
    "yAxis": {"type": "category", "data": []},
    "visualMap": {
        "min": -1,
        "max": 1,
        "calculable": True,
        "orient": "horizontal",
        "left": "center"
    },
    "series": [{
        "type": "heatmap",
        "data": [],
        "label": {"show": True}
    }]
})


def run_analysis():
    summary_box.clear()
    metrics_box.clear()

    tickers = [t.strip() for t in tickers_input.value.split(",")]
    risk_aversion = risk_slider.value

    response = requests.post(
        API_URL,
        json={
            "tickers": tickers,
            "risk_aversion": risk_aversion
        }
    )

    if response.status_code != 200:
        ui.notify("Backend error", type="negative")
        return

    data = response.json()

    # ======================
    # PARSE SERIES ONCE
    # ======================
    pnl_opt = np.array(data["pnl_series"])
    pnl_base = np.array(data["baseline_pnl_series"])

    # ======================
    # SUMMARY
    # ======================
    with summary_box:
        ui.label("Optimized Portfolio Allocation").classes("text-h6")
        for k, v in data["weights"].items():
            ui.label(f"{k}: {v:.2%}")

    # ======================
    # METRICS TABLE
    # ======================
    metrics_df = pd.DataFrame({
        "Metric": ["Sharpe Ratio", "Final PnL"],
        "Optimized": [
            data["sharpe"],
            pnl_opt[-1]
        ],
        "Equal Weight": [
            data["baseline_sharpe"],
            pnl_base[-1]
        ]
    })

    with metrics_box:
        ui.label("Performance Metrics").classes("text-h6")
        ui.table(
            columns=[
                {"name": "Metric", "label": "Metric", "field": "Metric"},
                {"name": "Optimized", "label": "Optimized", "field": "Optimized"},
                {"name": "Equal Weight", "label": "Equal Weight", "field": "Equal Weight"},
            ],
            rows=metrics_df.to_dict("records")
        ).props("dense flat")

    # ======================
    # UPDATE PNL CHART
    # ======================
    x = list(range(len(pnl_opt)))

    pnl_chart.options["xAxis"]["data"] = x
    pnl_chart.options["series"][0]["data"] = pnl_opt.tolist()
    pnl_chart.options["series"][1]["data"] = pnl_base.tolist()
    pnl_chart.update()

    # ======================
    # UPDATE CORRELATION HEATMAP
    # ======================
    corr = np.array(data["correlation"])
    heatmap_data = []

    for i in range(len(tickers)):
        for j in range(len(tickers)):
            heatmap_data.append([i, j, float(corr[i, j])])

    corr_chart.options["xAxis"]["data"] = tickers
    corr_chart.options["yAxis"]["data"] = tickers
    corr_chart.options["series"][0]["data"] = heatmap_data
    corr_chart.update()


ui.button("Run Optimization", on_click=run_analysis).classes("q-mt-md")

ui.run()
