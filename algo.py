import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Whos Next Algo", layout="centered")

# CSS se font size bada kar diya
st.markdown("""
<style>
   .big-font {
        font-size: 32px!important;
        font-weight: bold;
    }
   .signal-font {
        font-size: 24px!important;
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

def get_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=2"
    data = requests.get(url).json()
    prices = [x[1] for x in data['prices']]
    df = pd.DataFrame(prices, columns=['close'])
    return df

for symbol, coin_id in coins.items():
    df = get_data(coin_id)
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
    
    # Yahan font bada kar diya
    st.markdown(f'<p class="big-font">{symbol}</p>', unsafe_allow_html=True)
    st.write(f"**${price:,.2f}**")
    st.write(f"EMA21: ${ema:,.2f}")
    st.write(f"RSI: {rsi:.1f}")
    st.markdown(f'<p class="signal-font">Signal: {signal}</p>', unsafe_allow_html=True)
    st.divider()
