import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Whos Next Algo", layout="centered")

st.markdown("""
<style>
 .big-font {
        font-size: 32px!important;
        font-weight: bold;
        margin-bottom: -10px;
    }
 .signal-font {
        font-size: 24px!important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Whos Next Algo - BUY/SELL Signals")

# Binance wale symbols use karenge
coins = {
    'BTC': 'BTCUSDT', 
    'ETH': 'ETHUSDT', 
    'SOL': 'SOLUSDT', 
    'XRP': 'XRPUSDT', 
    'DOGE': 'DOGEUSDT', 
    'BNB': 'BNBUSDT'
}

@st.cache_data(ttl=30) # 30 sec cache. Binance fast hai
def get_data(symbol):
    try:
        # Binance Klines API - 1000 candle free
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100"
        r = requests.get(url, timeout=10)
        data = r.json()
        close_prices = [float(x[4]) for x in data] # 4th index = close price
        df = pd.DataFrame(close_prices, columns=['close'])
        return df
    except:
        return None

for symbol, binance_symbol in coins.items():
    df = get_data(binance_symbol)
    
    if df is None or df.empty:
        st.markdown(f'<p class="big-font">{symbol}</p>', unsafe_allow_html=True)
        st.error("Data load nahi hua. Refresh karo.")
        st.divider()
        continue
        
    df['EMA21'] = df['close'].ewm(span=21).mean()
    
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    price = df['close'].iloc[-1]
    ema = df['EMA21'].iloc[-1]
    rsi = df['RSI'].iloc[-1]
    
    if price > ema and 30 < rsi < 70:
        signal = "BUY 🟢"
    elif price < ema and rsi > 70:
        signal = "SELL 🔴"
    else:
        signal = "HOLD ⚪"
    
    st.markdown(f'<p class="big-font">{symbol}</p>', unsafe_allow_html=True)
    st.write(f"**${price:,.2f}**")
    st.write(f"EMA21: ${ema:,.2f}")
    st.write(f"RSI: {rsi:.1f}")
    st.markdown(f'<p class="signal-font">Signal: {signal}</p>', unsafe_allow_html=True)
    st.divider()

st.caption("Data: Binance API | No limits | Auto-cache: 30 sec")
