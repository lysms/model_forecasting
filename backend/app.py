from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

app = Flask(__name__)
CORS(app)  # Handles CORS issues for local development
from flask import Flask, request, jsonify
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

app = Flask(__name__)

@app.route('/forecast', methods=['GET'])
def forecast_sales():
    # Extract categories and frequency from query parameters
    categories = request.args.get('categories', '')
    frequency = request.args.get('frequency', 'monthly')
    categories = categories.split(',') if categories else []

    # Load the appropriate sales data file based on the frequency
    file_path = f'sales{frequency}.csv'
    df = pd.read_csv(file_path)
    df['datum'] = pd.to_datetime(df['datum'])
    df.set_index('datum', inplace=True)

    # Determine the forecasting steps and seasonality based on the frequency
    steps_mapping = {
        'hourly': 2 * 7 * 24,  # 2 weeks
        'daily': 3 * 30,       # 3 months
        'weekly': 52,          # 1 year
        'monthly': 3 * 12      # 3 years
    }
    seasonality = {
        'hourly': 24,
        'daily': 7,
        'weekly': 52,
        'monthly': 12
    }
    steps = steps_mapping.get(frequency, 3 * 12)  # Default to 3 years for monthly
    s = seasonality.get(frequency, 12)  # Default to 12 for monthly

    results = {}
    
    # Forecast for each selected category
    for category in categories:
        if category in df.columns:
            model = SARIMAX(df[category], order=(1, 1, 1), seasonal_order=(1, 1, 1, s))
            model_fit = model.fit(disp=False)
            forecast = model_fit.get_forecast(steps=steps)
            results[category] = {
                'historical': df[category].tolist(),
                'forecast': forecast.predicted_mean.tolist()
            }
    
    # Calculate and add the total sales historical and forecast data if there are categories
    if categories:
        df['total_sales'] = df[categories].sum(axis=1)
        total_model = SARIMAX(df['total_sales'], order=(1, 1, 1), seasonal_order=(1, 1, 1, s))
        total_model_fit = total_model.fit(disp=False)
        total_forecast = total_model_fit.get_forecast(steps=steps)
        results['total_sales'] = {
            'historical': df['total_sales'].tolist(),
            'forecast': total_forecast.predicted_mean.tolist()
        }

    return jsonify(results)

if __name__ == '__main__':
    app.run()
