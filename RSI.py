import pybroker
from pybroker import Strategy, StrategyConfig, YFinance, ExecContext
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt

def run_rsi_strategy(
    start_date="2022-01-01",
    end_date="2023-01-01",
    timeframe="1h",
    warmup=14,
    initial_cash=100_000
):
    """
    Runs a simple RSI-based strategy on BTC-USD and ETH-USD:
      - Buy when RSI < 40
      - Sell when RSI > 60

    Saves the resulting portfolio chart to rsi_result.png
    and attempts to display it in a GUI window.
    """

    # Optionally enable caching for faster repeated runs.
    pybroker.enable_data_source_cache("rsi_btc_eth")

    # Create a StrategyConfig (e.g., specify initial cash).
    config = StrategyConfig(initial_cash=initial_cash)

    # Initialize the Strategy with YFinance data.
    strategy = Strategy(
        data_source=YFinance(),
        start_date=start_date,
        end_date=end_date,
        config=config
    )

    def exec_rsi(ctx: ExecContext):
        """Execution function for RSI-based rules: Buy if RSI < 40, Sell if RSI > 60."""
        close_prices = ctx.close
        if close_prices is None or len(close_prices) < 15:
            return

        # Compute RSI(14) using pandas_ta
        rsi_14 = ta.rsi(pd.Series(close_prices), length=14)
        if rsi_14 is None or rsi_14.dropna().empty:
            return

        last_rsi = rsi_14.iloc[-1]

        # BUY if RSI < 40 and no current long position
        if not ctx.long_pos() and last_rsi < 40:
            ctx.buy_shares = 100
        # SELL if RSI > 60 and we have a long position
        elif ctx.long_pos() and last_rsi > 60:
            ctx.sell_all_shares()

    # Apply the RSI rules to both BTC-USD and ETH-USD
    strategy.add_execution(exec_rsi, ["BTC-USD", "ETH-USD"])

    # Run the backtest with the specified timeframe and warmup
    result = strategy.backtest(timeframe=timeframe, warmup=warmup)

    # Print a summary of the results
    print(f"=== RSI Strategy on BTC/ETH ===")
    print(f"Period: {start_date} to {end_date} | Timeframe: {timeframe} | Warmup: {warmup}")
    print(f"Initial Cash: {initial_cash}")
    print("\n>> TestResult <<")
    print(result)

    # Plot the portfolio's market value over time
    plt.figure(figsize=(10, 5))
    plt.plot(result.portfolio.index, result.portfolio["market_value"], label="Market Value")
    plt.title("BTC/ETH Portfolio Market Value (RSI Strategy)")
    plt.xlabel("Date")
    plt.ylabel("Market Value")
    plt.legend()

    # Save to local file in the current directory
    plt.savefig("rsi_result.png")

    # Attempt to display the figure in a window (may cause a warning in headless env)
    plt.show()


# Example usage (run this file directly to execute the strategy):
if __name__ == "__main__":
    run_rsi_strategy(
        start_date="2022-01-01",
        end_date="2023-01-01",
        timeframe="1h",
        warmup=14,
        initial_cash=100_000
    )
