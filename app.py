import pandas as pd
from dash import Dash, dash_table, html, dcc, Output, Input

# Dashアプリケーションの初期化
app = Dash(__name__)

# CSVファイルの読み込み
df = pd.read_csv("data.csv")


# 時間を数値に変換する関数
def time_to_float(time_str):
    """時間文字列を浮動小数点数に変換します。"""
    hour, minute = map(int, time_str.split(":"))
    return hour + minute / 60


# データフレームに開始時刻と終了時刻の数値列を追加
df["開始_数値"] = df["開始"].apply(time_to_float)
df["終了_数値"] = df["終了"].apply(time_to_float)

# アプリケーションのレイアウト
app.layout = html.Div(
    style={"padding": "1rem 2rem"},
    children=[
        html.H1("オープンセミナー2024@広島"),
        # スライダー
        html.Div(
            [
                html.Label("時間を選択してください:"),
                dcc.Slider(
                    id="time-slider",
                    min=9,
                    max=18,
                    step=0.1,
                    value=9,
                    marks={i: f"{i}:00" for i in range(9, 19)},
                ),
            ],
            style={"width": "80%", "margin": "1rem auto"},
        ),
        # テーブル
        dash_table.DataTable(
            id="schedule-table",
            columns=[
                {"name": col, "id": col}
                for col in df.columns
                if col not in ["開始_数値", "終了_数値"]
            ],
            data=df.to_dict("records"),
            style_cell={"textAlign": "left", "padding": "0.5rem"},
            style_header={
                "backgroundColor": "rgb(230, 230, 230)",
                "fontWeight": "bold",
            },
            # highlight_current_session の Output で設定される
            # style_data_conditional=[
            #     {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
            # ],
        ),
    ]
)


# コールバックの定義
@app.callback(
    Output("schedule-table", "style_data_conditional"), Input("time-slider", "value")
)
def highlight_current_session(selected_time):
    """
    スライダーで選択された時間に基づいて、該当するセッションの行を強調表示します。
    """
    return [
        {
            "if": {
                "filter_query": f"{{開始_数値}} <= {selected_time} && {{終了_数値}} > {selected_time}"
            },
            "backgroundColor": "tomato",
            "color": "white",
        }
    ]


# サーバーの実行
if __name__ == "__main__":
    app.run_server(debug=True)
