#######################################################################################
# Create list of options for import to TOS watchlist, used as selector for tradable 
# options for the provided symbol.
# Write the option symbols in TOS import format.
# After running this code to create the import files, right click a watchlist in TOS
# Import, select the file and import configuration options.
#
# The code uses yahoo finance, pulls the close value from the last trading day 
# for a symbol. Uses the close price as At The Money price and selects Call and Put 
# options from the options chain. The total number of strikes defaults to 11.
# ATM, 4 below and 5 above.
#
# Parameters: 
# symbol, underlying asset. Default is SPY
# date, date of expiration (0DTE) today is the default.
# n_strikes, how many strikes above/below ATM to create, 5 is the default.   
# export_tos_0dte_watchlist(symbol="SPY", n_strikes=5, date="2025-10-06")
#  
# Files are written with a date stamp name.
# options-chains\SPY_PUTS_watchlist_2025-10-06.txt
# options use TOS naming convention: .SPY251006P664
#
# Run from python via powershell:
# & path/python.exe path/import-options-0dte.py
#######################################################################################

# pip install yfinance pandas
import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def export_tos_0dte_watchlist(symbol: str, n_strikes: int = 5, strike_offset: int = None, output_folder: str = "./options-chains", date: str = None):
    """
    Exports 0DTE call and put options around ATM to TOS watchlist text files.

    Parameters:
        symbol (str): Underlying symbol, e.g., "SPY".
        n_strikes (int): Number of strikes above and below ATM to include.
        output_folder (str): Folder to save the watchlist files.
        date (str): Expiration date in "YYYY-MM-DD" format. Defaults to today.
    """
    # 1. Determine date
    if date is None:
        date_str = datetime.today().strftime("%Y-%m-%d")
    else:
        date_str = date

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # 2. Get ticker
    ticker = yf.Ticker(symbol)

    # 3. Validate expiration
    expirations = ticker.options
    if date_str not in expirations:
        raise ValueError(f"No {symbol} options expiring on {date_str}. Available expirations: {expirations}")

    # 4. Get option chain
    options_chain = ticker.option_chain(date_str)
    calls = options_chain.calls
    puts = options_chain.puts

    # 5. Find ATM strike
    underlying_price = ticker.history(period="1d")["Close"].iloc[-1]
    atm_strike = min(calls['strike'], key=lambda x: abs(x - underlying_price))

    if strike_offset is not None:
        atm_strike += strike_offset
    
    # 6. Select n_strikes above and below ATM
    def get_strikes(df, atm, n):
        strikes = sorted(df['strike'].unique())
        idx = min(range(len(strikes)), key=lambda i: abs(strikes[i] - atm))
        low = max(idx - n, 0)
        high = min(idx + n + 1, len(strikes))
        return strikes[low:high]

    selected_strikes = get_strikes(calls, atm_strike, n_strikes)
    calls = calls[calls['strike'].isin(selected_strikes)]
    puts = puts[puts['strike'].isin(selected_strikes)]

    # 7. Format TOS symbol
    def format_tos_symbol(row, cp_flag):
        exp_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%y%m%d")
        strike = int(row['strike']) if row['strike'].is_integer() else row['strike']
        return f".{symbol}{exp_date}{cp_flag}{strike}"

    calls['TOS_symbol'] = calls.apply(lambda r: format_tos_symbol(r, "C"), axis=1)
    puts['TOS_symbol'] = puts.apply(lambda r: format_tos_symbol(r, "P"), axis=1)

    # 8. Export to TOS watchlist files
    calls_file = os.path.join(output_folder, f"{symbol}_CALLS_watchlist_{date_str}.txt")
    puts_file = os.path.join(output_folder, f"{symbol}_PUTS_watchlist_{date_str}.txt")

    calls['TOS_symbol'].to_csv(calls_file, index=False, header=False)
    puts['TOS_symbol'].to_csv(puts_file, index=False, header=False)
    
    print(f"ATM strike set to: {atm_strike}")
    print(f"Exported {len(calls)} calls → {calls_file}")
    print(f"Exported {len(puts)} puts → {puts_file}")


# --- Example usage ---
# Use today's date
# export_tos_0dte_watchlist(symbol="SPY", n_strikes=5)

# Or specify an expiration date
export_tos_0dte_watchlist(symbol="SPY", n_strikes=5, strike_offset=2, date="2025-10-06")
