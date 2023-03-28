import yfinance as yf
import pandas as pd
import streamlit as st
from pandas.tseries.offsets import DateOffset


@st.cache_data
def get_data(tickers: list) -> pd.DataFrame:
    """
    Create a DataFrame of the Close values of the tickers.
    We use a st.cache in order to prevent the call from happening multiple times.
    """
    df = yf.download(tickers, start="2020-01-01")
    df = df["Close"]
    return df


def get_returns(df: pd.DataFrame, month_horizon: int) -> tuple:
    previous_prices = (
        df[: df.index[-1] - DateOffset(months=month_horizon)].tail(1).squeeze()
    )
    recent_prices = df.loc[df.index[-1]]
    return_df = recent_prices / previous_prices - 1

    return previous_prices.name, return_df


def create_dashboard(df: pd.DataFrame):
    st.title("Index component performance of the S&P 500")

    # Get the time horizon
    month_horizon = st.number_input(
        "Please provide the number horizon in months: ",
        min_value=1,
        max_value=24,
    )

    date, returns = get_returns(df, month_horizon)

    winners, losers = returns.nlargest(10), returns.nsmallest(10)
    winners.name, losers.name = "Winners", "Losers"

    st.table(winners)
    winner_choice = st.selectbox("Pick a winner to visualise:", winners.index)
    st.line_chart(df[winner_choice][date:])

    st.table(losers)
    loser_choice = st.selectbox("Pick a loser to visualise:", losers.index)
    st.line_chart(df[loser_choice][date:])


def main():
    tickers = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[
        0
    ].Symbol
    tickers = tickers.to_list()

    close_df = get_data(tickers)

    create_dashboard(close_df)


if __name__ == "__main__":
    main()
