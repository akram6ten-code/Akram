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

coins = {
    'BTC': 'bitcoin', 
    'ETH': 'ethereum', 
    'SOL': 'solana', 
    'XRP': 'ripple', 
    'DOGE': 'dogecoin', 
    'BNB': 'binancecoin'
}

@st.cache_data(ttl=60) # 60 sec tak data cache karega, rate limit se bachega
def get_data(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=2"
        r = requests.get(url, timeout=10)
        data = r.json()
        prices = [x[1] for x in data['prices']]
        df = pd.DataFrame(prices, columns=['close'])
        return df
    except:
        return None

for symbol, coin_id in coins.items():
    df = get_data(coin_id)
    
    if df is None or df.empty:
        st.markdown(f'<p class="big-font">{symbol}</p>', unsafe_allow_html=True)
        st.error("Data load nahi hua. 1 min baad refresh karo.")
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
    
    time.sleep(0.3) # API ko thoda time de

st.caption("Auto-refresh: 1 minute | Data: CoinGecko")
