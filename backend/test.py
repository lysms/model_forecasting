import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

def calculate_mape(actual, predicted, epsilon=1e-8):
    """
    Calculate the mean absolute percentage error (MAPE), with a small constant to avoid division by zero.

    Parameters:
    actual (array-like): The actual observed values.
    predicted (array-like): The predicted values.
    epsilon (float): A small value to avoid division by zero errors.

    Returns:
    float: The MAPE value as a percentage.
    """
    actual, predicted = np.array(actual), np.array(predicted)
    return np.mean(np.abs((actual - predicted) / (actual + epsilon))) * 100


def forecast_sales(frequency, categories):
    """
    Forecast sales for selected categories and calculate overall accuracy.

    Parameters:
    frequency (str): The frequency of the data ('hourly', 'daily', 'weekly', 'monthly').
    categories (list): List of categories to forecast.

    Returns:
    float: The overall MAPE value as a percentage.
    """
    file_path = f'sales{frequency}.csv'
    df = pd.read_csv(file_path)
    df['datum'] = pd.to_datetime(df['datum'])
    df.set_index('datum', inplace=True)

    seasonality = {'hourly': 24, 'daily': 7, 'weekly': 52, 'monthly': 12}
    s = seasonality[frequency]

    overall_mape = []

    for category in categories:
        model = SARIMAX(df[category], order=(1, 1, 1), seasonal_order=(1, 1, 1, s))
        model_fit = model.fit(disp=False)

        # Forecast for the entire period
        forecast = model_fit.get_forecast(steps=len(df))
        predicted = forecast.predicted_mean

        # Calculate overall MAPE
        mape = calculate_mape(df[category], predicted)
        overall_mape.append(mape)

    # Calculate the average MAPE across all categories for a single accuracy measure
    average_mape = np.mean(overall_mape)
    return average_mape

# Example usage
frequency = 'monthly'
categories_to_forecast = ['M01AB']
model_accuracy = forecast_sales(frequency, categories_to_forecast)
print(f"Overall Model Accuracy (MAPE): {model_accuracy}%")
