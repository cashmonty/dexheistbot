import pandas as pd
import mplfinance as mpf

def calculate_ichimoku(df):
    # Ensure that we are working on a copy of the DataFrame to avoid SettingWithCopyWarning
    df = df.copy()

    # Calculate Ichimoku Cloud components
    high_9 = df['High'].rolling(window=9).max()
    low_9 = df['Low'].rolling(window=9).min()
    df.loc[:, 'Tenkan-sen'] = (high_9 + low_9) / 2

    high_26 = df['High'].rolling(window=26).max()
    low_26 = df['Low'].rolling(window=26).min()
    df.loc[:, 'Kijun-sen'] = (high_26 + low_26) / 2

    df.loc[:, 'Senkou_Span_A'] = (df['Tenkan-sen'] + df['Kijun-sen']) / 2

    high_52 = df['High'].rolling(window=52).max()
    low_52 = df['Low'].rolling(window=52).min()
    df.loc[:, 'Senkou_Span_B'] = (high_52 + low_52) / 2

    df.loc[:, 'Chikou_Span'] = df['Close'].shift(periods=-26)

    return df





num_candles = 100

async def process_ohlc_data_and_generate_chart(ohlc_data):
    df = pd.DataFrame(ohlc_data['data'])
    df['date_open'] = pd.to_datetime(df['date_open'])
    df.set_index('date_open', inplace=True)
    df.rename(columns={
        'price_open': 'Open',
        'price_high': 'High',
        'price_low': 'Low',
        'price_close': 'Close',
        'volume_1h_usd': 'Volume'
    }, inplace=True)

    # Define thresholds for outlier removal
    upper_threshold = df['Close'].mean() + 3 * df['Close'].std()
    lower_threshold = df['Close'].mean() - 3 * df['Close'].std()

    # Filter out outliers based on thresholds
    df_filtered = df[(df['High'] <= upper_threshold) & (df['Low'] >= lower_threshold)]

    # Calculate the Ichimoku Cloud on the filtered data
    df_filtered = calculate_ichimoku(df_filtered)

    # Slice to get the last 'num_candles' candles from the filtered data
    df_last_candles = df_filtered[-num_candles:]

    # Create Ichimoku Cloud lines for plotting
    ic = [
        mpf.make_addplot(df_last_candles['Tenkan-sen'], color='#fcc905'),
        mpf.make_addplot(df_last_candles['Kijun-sen'], color='#F83C78'),
        mpf.make_addplot(df_last_candles['Senkou_Span_A'], color='#006B3D', alpha=0.5),
        mpf.make_addplot(df_last_candles['Senkou_Span_B'], color='#D3212C', alpha=0.5),
        mpf.make_addplot(df_last_candles['Chikou_Span'], color='#8D8D16'),
    ]
    # Prepare the fill_between parameters for where Senkou_Span_A is above Senkou_Span_B
    ichimoku_fill_above = {
        'y1': df_last_candles['Senkou_Span_A'].values,
        'y2': df_last_candles['Senkou_Span_B'].values,
        'where': df_last_candles['Senkou_Span_A'] >= df_last_candles['Senkou_Span_B'],
        'alpha': 0.5,
        'color': '#a6f7a6'
    }
        # Prepare the fill_between parameters for where Senkou_Span_B is above Senkou_Span_A
    ichimoku_fill_below = {
        'y1': df_last_candles['Senkou_Span_A'].values,
        'y2': df_last_candles['Senkou_Span_B'].values,
        'where': df_last_candles['Senkou_Span_A'] < df_last_candles['Senkou_Span_B'],
        'alpha': 0.5,
        'color': '#f4a7b9'
    }
    # Manually set y-axis limits for the last 'num_candles' candles
    price_min = df_last_candles[['Low', 'Tenkan-sen', 'Kijun-sen', 'Senkou_Span_A', 'Senkou_Span_B']].min().min()
    price_max = df_last_candles[['High', 'Tenkan-sen', 'Kijun-sen', 'Senkou_Span_A', 'Senkou_Span_B']].max().max()
    y_limits = (price_min, price_max)

    # Plot the chart with fills
    mpf.plot(
        df_last_candles,
        type='candle',
        style='yahoo',
        addplot=ic,  # Your previously defined Ichimoku Cloud lines
        fill_between=[ichimoku_fill_above, ichimoku_fill_below],  # Specify fills
        figsize=(20, 10),
        ylim=y_limits,
        savefig='chart.png'
    )

    return 'chart.png'