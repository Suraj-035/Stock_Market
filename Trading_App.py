import streamlit as st

st.set_page_config(
    page_title="Trading App",
    page_icon="heavy_dollar_sign",
    layout="wide"
)

st.title("Trading Guide App :bar_chart:") ## this colon here is a emoji sign 
st.header("We provide the Greatest platform for u to collect all information prior to investing in stocks.")

st.image("images.jpeg")

st.markdown("### We provide the following services :")

st.markdown("#### :one: Stock Information")
st.write("Through this page, you can see all the information about stock.")

st.markdown("#### :two: Stock Prediction")
st.write("You can explore predicted closing prices for the next 30 days based on historical stock data and advanced forecasting models. Use this tool to gain valuable insights into market trends and make informed investment decisions.")

st.markdown("#### :three: CAPM Return")
st.write("Through this page, you can see all the information about stock.")

st.markdown("#### :four: CAPM Return")
st.write("Discover how the Capital Asset Pricing Model (CAPM) calculates the expected return of different stocks asset based on its risk and market performance.")

st.markdown("#### :five: CAPM beta")
st.write("Calculates Beta and Expected Return for Individual Stocks.")


