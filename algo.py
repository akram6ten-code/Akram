import streamlit as st
import yfinance as yf
import pandas as pd
import time

SYMBOLS = {
    'BTC': 'BTC-USD',
    'ETH': 'ETH-USD', 
    'SOL': 'SOL-USD',
    'XRP': 'XRP-USD',
    'DOGE': 'DOGE-USD',
    'BNB': 'BNB-USD'
}

INTERVAL = '5m'
REFRESH_INTERVAL = 60

def get_data(symbol):
    ticker = yf.Ticker(SYMBOLS[symbol])
    df = ticker.history(period='5d', interval=INTERVAL)
    
    if df.empty or len(df) < 50:
        st.warning(f"{symbol}: Yah data available nahi hai")
        return None
    
    df = df.tail(100)
    return df
    
st.set_page_config(page_title="Whos Next Algo", layout="wide")
st.title("🚀 Whos Next Algo - Price")

placeholder = st.empty()

while True:
    with placeholder.container():
        for symbol in SYMBOLS.keys():
            df = get_data(symbol)
            
            if df is not None and not df.empty:
                last = df.iloc[-1]
                price = float(last['Close'])
                
                signal = "HOLD ⚪"
                
                col1, col2 = st.columns(2)
                col1.metric(f"{symbol}", f"${price:.2f}")
                col2.write(f"Signal: {signal}")
                
    time.sleep(REFRESH_INTERVAL)
