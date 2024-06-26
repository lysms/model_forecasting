import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

def forecast_sales(frequency, categories, steps=36):
    """
    Forecast sales for selected categories over a specified number of months.

    Parameters:
    df (dfFrame): The sales df.
    categories (list): List of categories to forecast.
    steps (int): Number of months to forecast.

    Returns:
    Two plots: one for each category's historical and forecasted sales, 
    and one for the total sales.
    """
    plt.figure(figsize=(15, 10))
    file_path = f'sales{frequency}.csv'
    df = pd.read_csv(file_path)
    # Default the forecasting period
    if steps is None:
        if frequency == 'hourly':
            steps = 2 * 7 * 24  # 2 weeks
        elif frequency == 'daily':
            steps = 3 * 30  # 3 months
        elif frequency == 'weekly':
            steps = 52  # 1 year
        elif frequency == 'monthly':
            steps = 3 * 12  # 3 years

    df['datum'] = pd.to_datetime(df['datum'])
    df.set_index('datum', inplace=True)

    
    # Determine the seasonality based on the data frequency
    seasonality = {'hourly': 24, 'daily': 7, 'weekly': 52, 'monthly': 12}
    s = seasonality.get(frequency, 1)

    # Plot for each category
    for category in categories:
        # Initialize a SARIMAX model on the total_sales column of the dataset.
        # The SARIMAX model can account for both seasonal and non-seasonal elements of a time series.
        # order=(1, 1, 1): The non-seasonal order parameters for the model, where:
        #   p=1: The number of lag observations included in the model (AR part).
        #   d=1: The degree of differencing (the number of times the data have had past values subtracted).
        #   q=1: The size of the moving average window (MA part).
        # seasonal_order=(1, 1, 1, 12): The seasonal order parameters, where:
        #   P=1: The number of seasonal autoregressive terms.
        #   D=1: The number of seasonal differences applied to achieve stationarity.
        #   Q=1: The number of seasonal moving average terms.
        #   s=12: The number of periods in each season (12 indicates monthly data with an annual cycle).
        # total_model = SARIMAX(data['total_sales'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))


        # SARIMAX (Seasonal AutoRegressive Integrated Moving Average with eXogenous factors) models
        model = SARIMAX(df[category], order=(1, 1, 1), seasonal_order=(1, 1, 1, s))
        model_fit = model.fit(disp=False)
        forecast = model_fit.get_forecast(steps=steps)
        forecast_mean = forecast.predicted_mean

        # Plotting historical and forecasted sales for each category
        plt.plot(df.index, df[category], label=f'Historical {category}')
        plt.plot(forecast_mean.index, forecast_mean, linestyle='--', label=f'Forecasted {category}')

    plt.title('Historical and Forecasted Sales for Each Category')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.show()

    # Plot for total sales
    plt.figure(figsize=(15, 10))
    df['total_sales'] = df[categories].sum(axis=1)
   

    total_model = SARIMAX(df['total_sales'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    total_model_fit = total_model.fit(disp=False)
    total_forecast = total_model_fit.get_forecast(steps=steps)

    plt.plot(df.index, df['total_sales'], label='Historical Total Sales')
    plt.plot(total_forecast.predicted_mean.index, total_forecast.predicted_mean, linestyle='--', label='Forecasted Total Sales')
    plt.title('Historical and Forecasted Total Sales')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.show()

     # ACF and PACF plots for each category
    for category in categories:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8))
        plot_acf(df[category], ax=ax1, title=f'ACF for {category}')
        plot_pacf(df[category], ax=ax2, title=f'PACF for {category}')
        plt.show()

# Example usage of the function

frequency = 'monthly'
categories_to_forecast = ['M01AB']  # example categories
forecast_sales(frequency, categories_to_forecast, steps=36)