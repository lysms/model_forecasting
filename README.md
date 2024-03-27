# model_forecasting

ARIMA (AutoRegressive Integrated Moving Average) and SARIMAX (Seasonal AutoRegressive Integrated Moving Average with eXogenous factors) models are related but not the same. They are both used for time series forecasting but have different capabilities and use cases:

## ARIMA

ARIMA models are used for analyzing and forecasting univariate time series data.
An ARIMA model is characterized by three main parameters: (p, d, q):

- p (AR part): Number of lag observations included in the model.
- d (I part): Degree of differencing required to make the time series stationary.
- q (MA part): Size of the moving average window.
- ARIMA is suitable for time series without seasonal components or with them removed.

## SARIMAX

SARIMAX extends ARIMA by adding support for seasonality and exogenous variables.
SARIMAX parameters include (p, d, q) for the non-seasonal part, and (P, D, Q, s) for the seasonal part:

- P (seasonal AR part): Seasonal autoregressive order.
- D (seasonal I part): Seasonal differencing order.
- Q (seasonal MA part): Seasonal moving average order.
- s: Number of periods in each season (e.g., 12 for monthly data with yearly seasonality).
- Exogenous factors (X): External variables that might influence the time series but are not part of the series itself.
- SARIMAX is useful when the time series data have a seasonal pattern or when you want to consider the impact of external variables on the forecast.

### when to use

- Use ARIMA when you have a non-seasonal time series or after removing the seasonality from the data.
- Use SARIMAX when dealing with seasonal data or when you want to include the effect of external variables on the forecasts.
