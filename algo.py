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

EMA_LENGTH = 21
RSI_LENGTH = 14
INTERVAL = '5m'
REFRESH_INTERVAL = 60

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_data(symbol):
    ticker = yf.Ticker(SYMBOLS[symbol])
    df = ticker.history(period='5d', interval=INTERVAL)
    
    if df.empty or len(df) < 50:
        st.warning(f"{symbol}: Yah data available nahi hai")
        return None
    
    df['ema'] = df['Close'].ewm(span=EMA_LENGTH, adjust=False).mean()
    df['rsi'] = calculate_rsi(df['Close'], RSI_LENGTH)
    df = df.tail(100)
    return df
    
st.set_page_config(page_title="Whos Next Algo", layout="wide")
st.title("🚀 Whos Next Algo - BUY/SELL Signals")

placeholder = st.empty()

while True:
    with placeholder.container():
        for symbol in SYMBOLS.keys():
            df = get_data(symbol)
            
            if df is not None and not df.empty:
                last = df.iloc[-1]
                price = float(last['Close'])
                ema = float(last['ema'])
                rsi = float(last['rsi'])
                
                signal = "HOLD ⚪"
                if price > ema and rsi < 70 and rsi > 30:
                    signal = "BUY 🟢"
                if price < ema and rsi > 70:
                    signal = "SELL 🔴"
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric(f"{symbol}", f"${price:.2f}")
                col2.metric("EMA21", f"${ema:.2f}")
                col3.metric("RSI", f"{rsi:.1f}")
                col4.write(f"**Signal: {signal}**")
                
    time.sleep(REFRESH_INTERVAL)
