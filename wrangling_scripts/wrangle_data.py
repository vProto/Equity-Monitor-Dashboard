import pandas as pd
import plotly.graph_objs as go
import yfinance as yf
from datetime import date,timedelta


def calculate_mv_avg(df,name):
    """
    Calculates moving averages of stock data
    Args:
        df: dataframe with prices

    Returns: dataframe with moving averages

    """
    # Disable chaining assignment warning (as it is false positive)
    pd.options.mode.chained_assignment = None

    df['3M-MV'] = df[name].rolling(window=63).mean()
    df['1Y-MV'] = df[name].rolling(window=252).mean()
    return df

def return_figures(type):
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # Create start date and end date
    today = date.today() # today
    start =today - timedelta(days=6*365) # 6 years of data
    end = today.strftime("%Y-%m-%d")

    # List of tickers

    tickers = ["SPY", "QQQ", "IWM", "ACWI"] if type=='index' else ["MTUM","SPHB",'VLUE',"SIZE","QUAL","IUSG"]
    # Download data using yfinance
    data = yf.download(tickers, start=start, end=today)
    data = data['Close']

    # Create empty list that we store the figures
    figures = []

    # Loop for each ticker
    for name in tickers:
        # get the data for each ticker
        temp = data[[name]]

        # Calculate moving avarage for each ticker
        mv = calculate_mv_avg(temp,name)

        # Plot
        # Create a figure
        fig = go.Figure()

        # Add trace, x axis, y axis, mode = lines
        fig.add_trace(go.Scatter(x=mv.index, y=mv[name], mode='lines', line=dict(color='#292b2c', width=2),
                                 name=f'{name}  Price'))
        fig.add_trace(go.Scatter(x=mv.index, y=mv['3M-MV'], mode='lines', line=dict(color='#f0ad4e', width=2),
                                 name=f'{name} 3M Moving Average'))
        fig.add_trace(go.Scatter(x=mv.index, y=mv['1Y-MV'], mode='lines', line=dict(color='#d9534f', width=2),
                                 name=f'{name} 1Y Moving Average'))



        # Update layout
        fig.update_layout(
            title={'text': f'{name} ETF'},
            xaxis=dict(
                title=''), yaxis=dict(
                title='',
                ticksuffix=""),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="h")
        )



        # Add to the figures list
        figures.append(dict(data=fig))


    return figures