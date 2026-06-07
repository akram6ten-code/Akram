import time
import streamlit as st
import pandas as pd
# import pandas_ta as ta
import yfinance as yf

# ===== CONFIG =====
SYMBOLS = {
    'BTCUSD': 'BTC-USD',
    'ETHUSD': 'ETH-USD',
    'SOLUSD': 'SOL-USD',
    'XRPUSD': 'XRP-USD',
    'DOGEUSD': 'DOGE-USD',
    'BNBUSD': 'BNB-USD'
}
EMA_LENGTH = 21
CANDLE_INTERVAL = '5m'
REFRESH_SEC = 60
# ==================

def get_data(symbol):
    try:
        ticker = yf.Ticker(SYMBOLS[symbol])
        # Ticker.history zyada reliable hai download se
        df = ticker.history(period='5d', interval=CANDLE_INTERVAL)

        if df.empty or len(df) < EMA_LENGTH:
            st.warning(f"{symbol}: Yahoo se data kam mila. {len(df)} candles only.")
            return None

        # df['ema'] = ta.ema(df['Close'], length=EMA_LENGTH)
        df = df.tail(100) # Last 100 candles hi rakho
        return df
    except Exception as e:
        st.error(f"{symbol} Error: {e}")
        return None

st.set_page_config(page_title="Whos Next Algo", layout="wide")
st.title("🚀 Whos Next Algo - Price + EMA Signal")

placeholder = st.empty()

while True:
    with placeholder.container():
        for symbol in SYMBOLS.keys():
            df = get_data(symbol)

            if df is not None and not df.empty:
                last = df.iloc[-1]
                price = float(last['Close'])
                ema = float(last['ema'])

                # NaN check
                if pd.isna(ema):
                    st.warning(f"**{symbol}** | Price: {price:.2f} | EMA calculating...")
                    continue

                signal = "HOLD ⚪"
                if price > ema: signal = "LONG BIAS 🟢"
                if price < ema: signal = "SHORT BIAS 🔴"

                st.success(f"**{symbol}** | Price: {price:.2f} | EMA{EMA_LENGTH}: {ema:.2f} | {signal}")
            else:
                st.warning(f"**{symbol}**: Data nahi mila")

        st.caption(f"Last Update: {time.strftime('%H:%M:%S')} | Auto refresh: {REFRESH_SEC}s")

    time.sleep(REFRESH_SEC)
    st.rerun()