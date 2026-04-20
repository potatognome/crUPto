
import os
import pandas as pd
from tUilKit import get_logger
from crUPto.proc.data import read_historical_data, get_historical_price

# Use tUilKit logger for all logging
logger = get_logger()

def calculate_units(df):
    """Add the 'Units' column to the DataFrame."""
    # df['Units'] = df.apply(lambda row: row['Units_Received'] if row['Action'] in ['Buy', 'Reward', 'Receive', 'Other'] else -row['Units_Sent'], axis=1)
    df['Units'] = df.apply(lambda row: -row['Units_Sent'] if row['Action'] in ['Send', 'Sell', 'Withdrawal'] else row['Units_Received'], axis=1)

def calculate_acb_and_gains(df):
    """Calculate Adjusted Cost Basis (ACB) and Realized Gains/Losses."""
    # Initialize variables for ACB and transactions
    acb, total_units, total_realized_gains, total_distributions, total_cashback = {}, {}, {}, {}, {}
    acb_list, total_qty_list, acb_per_unit_list, gain_loss_list = [], [], [], []
    sell_transactions, distribution_transactions, cashback_transactions = [], [], []
    gain_loss_value = 0
    for index, row in df.iterrows():
        currency = row['Currency_Sent'] if row['Units'] < 0 else row['Currency_Received']
        gain_loss_value = None
        # Default values for skipped/invalid rows
        acb_val = None
        total_qty_val = None
        acb_per_unit_val = None
        gain_loss_val = None

        if pd.isna(currency) or currency == "":
            # Append None for all columns if currency is invalid
            acb_list.append(acb_val)
            total_qty_list.append(total_qty_val)
            acb_per_unit_list.append(acb_per_unit_val)
            gain_loss_list.append(gain_loss_val)
            continue

        if currency not in acb:
            acb[currency] = 0
            total_units[currency] = 0
            total_realized_gains[currency] = 0
            total_distributions[currency] = 0
            total_cashback[currency] = 0

        # Handle sell/send transactions
        if row['Units'] < 0:
            lot_size = -row['Units']
            acb_per_unit = acb[currency] / total_units[currency] if total_units[currency] != 0 else 0
            gain_loss_value = row['Book_Cost'] - lot_size * acb_per_unit

            acb[currency] -= lot_size * acb_per_unit
            acb[currency] = max(acb[currency], 0)  # Ensure ACB doesn't go negative
            total_units[currency] -= lot_size
            total_realized_gains[currency] += gain_loss_value

            sell_transactions.append({
                'Date': row['Date'],
                'Currency': currency,
                'ACB/Unit': acb_per_unit,
                'Qty Sold': lot_size,
                'Realized Profit/Loss': gain_loss_value,
                'Description': row['Description']  # Include the description
            })
            acb_val = acb[currency]
            total_qty_val = total_units[currency]
            acb_per_unit_val = acb[currency] / total_units[currency] if total_units[currency] > 0 else 0
            gain_loss_val = gain_loss_value

        # Handle buy/receive/reward/other transactions
        elif row['Units'] > 0:
            lot_size = row['Units']
            acb[currency] += row['Book_Cost']
            total_units[currency] += lot_size

            # Check for 'Reward' and 'Other' transactions
            if row['Action'] in ['Reward', 'Other']:
                if row['Description'] in ['Bitcoin cashback', 'ShakeSquad']:
                    # Add to the 'Cashback' category
                    if 'total_cashback' not in locals():
                        total_cashback = {}  # Initialize the variable if it doesn't exist
                    if currency not in total_cashback:
                        total_cashback[currency] = 0  # Initialize for the currency
                    total_cashback[currency] += row['Book_Cost']
                    cashback_transactions.append({
                        'Date': row['Date'],
                        'Currency': currency,
                        'Action': row['Action'],
                        'Units Received': row['Units_Received'],
                        'Book Cost': row['Book_Cost'],
                        'Description': row['Description']  # Include the description
                    })
                else:
                    # Add to Distributions category
                    total_distributions[currency] += row['Book_Cost']
                    distribution_transactions.append({
                        'Date': row['Date'],
                        'Currency': currency,
                        'Action': row['Action'],
                        'Units Received': row['Units_Received'],
                        'Book Cost': row['Book_Cost'],
                        'Description': row['Description']  # Include the description
                    })
            acb_val = acb[currency]
            total_qty_val = total_units[currency]
            acb_per_unit_val = acb[currency] / total_units[currency] if total_units[currency] > 0 else 0
            gain_loss_val = None

        acb_list.append(acb_val)
        total_qty_list.append(total_qty_val)
        acb_per_unit_list.append(acb_per_unit_val)
        gain_loss_list.append(gain_loss_val)
    df['ACB'] = acb_list
    df['Total Units'] = total_qty_list
    df['Gain/Loss'] = gain_loss_list
    df['ACB/Unit'] = acb_per_unit_list

    return df, sell_transactions, distribution_transactions, cashback_transactions, total_realized_gains, total_distributions, total_cashback

def newton_logic(df, historical_dir):
    """Convert Newton transaction history to the required format. Uses config-driven historical_dir."""
    # Rename columns to match the expected headers
    df.rename(columns={
        'Type': 'Action',
        'Received Quantity': 'Units_Received',
        'Received Currency': 'Currency_Received',
        'Sent Quantity': 'Units_Sent',
        'Sent Currency': 'Currency_Sent',
        'Tag': 'Description'
    }, inplace=True)

    # Convert 'Date' column to datetime, coercing errors
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])  # Drop rows where 'Date' couldn't be parsed
    df = df.sort_values(by='Date')

    # Keep float dtype so subsequent price assignments do not upcast from int.
    df['Book_Cost'] = 0.0

    # Convert TRADE type actions into BUY or SELL transactions
    df['Action'] = df.apply(lambda row: 'Buy' if row['Action'] == 'TRADE' and row['Currency_Received'] != 'CAD' else ('Sell' if row['Action'] == 'TRADE' and row['Currency_Received'] == 'CAD' else row['Action']), axis=1)
    df['Units'] = df.apply(lambda row: row['Units_Received'] if row['Action'] in ['Buy','Deposit','DEPOSIT'] else (-row['Units_Sent'] if row['Action'] == 'Sell' else row['Units_Received']), axis=1)
    
    # Live staking summary is rendered once in main.py; avoid noisy redraws here.

    def _as_float(value):
        numeric = pd.to_numeric(value, errors='coerce')
        return float(numeric) if pd.notna(numeric) else None

    for index, row in df.iterrows():
        currency = row['Currency_Received']
        transaction_date = row['Date']
        action = str(row.get('Action', '')).strip().upper()
        units_received = _as_float(row.get('Units_Received')) or 0.0
        units_sent = _as_float(row.get('Units_Sent')) or 0.0
        spot_rate = _as_float(row.get('Spot Rate'))

        if row['Description'] == "Referral Program":     
            # This is actually a Reward Transaction
            df.loc[index, 'Action'] = 'Reward'
            df.loc[index, 'Book_Cost'] = units_received
        elif action == 'BUY':
            # Cost basis for buys comes from the CAD leg or, if needed, spot price.
            if str(row.get('Currency_Sent', '')).upper() == 'CAD' and units_sent > 0:
                df.loc[index, 'Book_Cost'] = units_sent
            elif spot_rate is not None and units_received > 0:
                df.loc[index, 'Book_Cost'] = units_received * spot_rate
            elif pd.isna(row.get('Book_Cost')):
                df.loc[index, 'Book_Cost'] = 0.0
        elif action == 'SELL':
            # Proceeds for sells come from CAD received or spot price of units sold.
            if str(row.get('Currency_Received', '')).upper() == 'CAD' and units_received > 0:
                df.loc[index, 'Book_Cost'] = units_received
            elif spot_rate is not None and units_sent > 0:
                df.loc[index, 'Book_Cost'] = units_sent * spot_rate
            elif pd.isna(row.get('Book_Cost')):
                df.loc[index, 'Book_Cost'] = 0.0
        elif action == 'REWARD' and row['Currency_Received'] != 'CAD':
            # These Staking Reward transactions are in a different currency
            if spot_rate is not None and units_received > 0:
                historical_price = spot_rate
            else:
                historical_folder = os.path.join(historical_dir, f"{currency}_CAD")
                historical_price = get_historical_price(currency, transaction_date, historical_folder)
            df.loc[index, 'Action'] = 'Reward'
            df.loc[index, 'Book_Cost'] = units_received * historical_price
        elif action == 'DEPOSIT' and row['Currency_Received'] != 'CAD':
            # This is actually a Receive Transaction
            if spot_rate is not None and units_received > 0:
                historical_price = spot_rate
            else:
                historical_folder = os.path.join(historical_dir, f"{currency}_CAD")
                historical_price = get_historical_price(currency, transaction_date, historical_folder)
            df.loc[index, 'Book_Cost'] = units_received * historical_price
            df.loc[index, 'Action'] = 'Receive'
            logger.colour_log("!info", "Receive Transaction on:", "!date", transaction_date, "!output", f"${df.loc[index, 'Book_Cost']:.2f}")
        elif action == 'DEPOSIT' and row['Currency_Received'] == 'CAD':
            # Deposit Transaction in CAD cash
            df.loc[index, 'Action'] = 'Deposit'
            df.loc[index, 'Book_Cost'] = units_received
            logger.colour_log("!info", "CAD Deposit Transaction on:", "!date", transaction_date, "!output", f"${df.loc[index, 'Book_Cost']:.2f}")
        elif action == 'WITHDRAWN' and row['Currency_Sent'] == 'CAD':
            # Withdrawal Transaciton in CAD cash
            df.loc[index, 'Action'] = 'Withdrawal'
            df.loc[index, 'Book_Cost'] = units_sent
            currency = row['Currency_Sent']
            logger.colour_log("!info", "CAD Withdrawal Transaction on:", "!date", transaction_date, "!output", f"${df.loc[index, 'Book_Cost']:.2f}")
        elif pd.isna(row.get('Book_Cost')):
            df.loc[index, 'Book_Cost'] = 0.0
    return df

def generate_summary(df, total_realized_gains, total_distributions, total_cashback):
    """Generate the summary DataFrame."""
    all_currencies = pd.concat([df['Currency_Received'], df['Currency_Sent']]).dropna().unique()
    summary_data = {'Currency': [], 'ACB': [], 'Realized Gain/Loss': [], 'Distributions': [], 'Cashback': []}

    for currency in all_currencies:
        currency_df = df[(df['Currency_Received'] == currency) | (df['Currency_Sent'] == currency)]
        acb_final = currency_df['ACB'].dropna().iloc[-1] if not currency_df['ACB'].dropna().empty else 0
        gain_loss_total = total_realized_gains.get(currency, 0)
        distribution = total_distributions.get(currency, 0)
        cashback = total_cashback.get(currency, 0)
        if currency.strip() != "":  # Exclude blank currencies
            summary_data['Currency'].append(currency)
            summary_data['ACB'].append(acb_final)
            summary_data['Realized Gain/Loss'].append(gain_loss_total)
            summary_data['Distributions'].append(distribution)
            summary_data['Cashback'].append(cashback)

    return pd.DataFrame(summary_data)

def match_and_adjust_acb_combined(df, tolerance=0.0001, date_tolerance=1):
    """
    Match send and receive transactions and adjust ACB on the receive side.
    Args:
        df (pd.DataFrame): Combined wallet DataFrame.
        tolerance (float): Tolerance for amount matching.
        date_tolerance (int): Tolerance for date matching (in days).
    Returns:
        pd.DataFrame: Updated combined DataFrame with adjusted ACB.
        pd.DataFrame: Unmatched transactions.
        pd.DataFrame: Matched transactions.
    """
    from crUPto.utils.path_utils import resolve_path
    matches = []
    unmatched_df = df.copy()

    # These should be passed in, but for now, try to get from global config if available
    import builtins
    global_config = getattr(builtins, 'crUPto_global_config', None)
    ROOT_MODES = getattr(builtins, 'crUPto_ROOT_MODES', None)

    for index_send, row_send in df[df['Action'] == 'Send'].iterrows():
        for index_receive, row_receive in df[df['Action'] == 'Receive'].iterrows():
            if (
                row_send['Currency_Sent'] == row_receive['Currency_Received'] and
                abs(row_send['Units_Sent'] - row_receive['Units_Received']) <= tolerance and
                row_receive['Date'] > row_send['Date'] and  # Ensure receive happens after send
                abs((row_send['Date'] - row_receive['Date']).days) <= date_tolerance
            ):
                transaction_date = row_receive['Date']
                currency = row_receive['Currency_Received']
                if global_config is not None and ROOT_MODES is not None:
                    historical_dir = resolve_path("INPUT_HISTORICAL", global_config, ROOT_MODES)
                else:
                    # fallback: use current directory
                    historical_dir = os.path.join(os.getcwd(), "historical")
                historical_folder = os.path.join(historical_dir, f"{currency}_CAD")
                historical_price = get_historical_price(currency, transaction_date, historical_folder)
                acb_adjustment = row_send['Gain/Loss']
                logger.colour_log("Send/Receive Match Produced At: ","DATE",transaction_date, " Spot Rate: $", "OUTPUT", f"{historical_price:.2f} ", "DATA", "ACB Adjustment: ", "OUTPUT", f"{acb_adjustment:6.2f} ")                

                adjusted_acb = row_send['Book_Cost'] - acb_adjustment

                df.at[index_send, 'Book_Cost'] = adjusted_acb
                df.at[index_send, 'Gain/Loss'] = None
                df.at[index_receive, 'Book_Cost'] = adjusted_acb
                df.at[index_receive, 'ACB'] = adjusted_acb
                df.at[index_receive, 'Spot Rate'] = historical_price

                matches.append({
                    'Send Index': index_send,
                    'Receive Index': index_receive,
                    'Date Send': row_send['Date'],
                    'Date Receive': row_receive['Date'],
                    'Currency': row_send['Currency_Sent'],
                    'Amount Sent': row_send['Units_Sent'],
                    'Amount Received': row_receive['Units_Received'],
                    'Adjusted ACB': adjusted_acb
                })

                unmatched_df = unmatched_df.drop(index=[index_send, index_receive], errors='ignore')
                break

    matches_df = pd.DataFrame(matches)
    return df, unmatched_df, matches_df
