import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
from pages.utils.model_train import get_data, get_rolling_mean,get_differencing_order,scaling, evaluate_model, fit_model, get_forecast, scaling, inverse_scaling, stationary_check
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast

##setting page config
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="page_with_curl",
    layout="wide",
)

st.title("Stock Prediction")

col1,col2,col3=st.columns(3)


# This block is the main part of the Streamlit app's column
with col1:
    ticker = st.text_input('Stock Ticker', 'TSLA')

st.subheader('Predicting Next 30 days Close Price for: '+ticker)

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)
differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)
rmse = evaluate_model(scaled_data, differencing_order)

st.write('**Model RMSE Score:**',rmse)

#forecast = get_forecast(scaled_data, differencing_order)
# --- FIX: Pass the historical data to the function ---
forecast = get_forecast(scaled_data, differencing_order, rolling_price)

forecast['Close'] = inverse_scaling(scaler, forecast['Close'])
st.write('#### Forecast Data (Next 30 days)')
fig_tail = plotly_table(forecast.sort_index(ascending = True).round(3))
fig_tail.update_layout(height = 220)
st.plotly_chart(fig_tail, use_container_width=True)

# This block continues from the code above
forecast = pd.concat([rolling_price, forecast])

#st.plotly_chart(Moving_average_forecast(forecast.iloc[150:]), use_container_width=True)
st.plotly_chart(Moving_average_forecast(forecast), use_container_width=True)

