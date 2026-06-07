import streamlit as st
import requests
import pandas as pd

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
    'BTC': 'BTC', 
    'ETH': 'ETH', 
    'SOL': 'SOL', 
    'XRP': 'XRP', 
    'DOGE': 'DOGE', 
    'BNB': 'BNB'
}

@st.cache_data(ttl=120) # 2 min cache. 100k limit hai month ki
def get_data(symbol):
    try:
        # CryptoCompare API - No key needed for basic
        url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={symbol}&tsym=USD&limit=100"
        headers = {'User-Agent': 'Mozilla/5.0'} # Ye important hai
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        prices = [x['close'] for x in data['Data']['Data']]
        df = pd.DataFrame(prices, columns=['close'])
        return df
    except:
        return None

for symbol, cc_symbol in coins.items():
    df = get_data(cc_symbol)
    
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

st.caption("Data: CryptoCompare | 100k calls/month free")
