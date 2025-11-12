import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime,timedelta,timezone

Symbol_list =['^TWII','^TWOII','^GSPC','^IXIC','^RUT','^DJI']

def plot_five_tab(symbol):
  raw = yf.Ticker(symbol)
  data = raw.history(period='4Y')
  CLOSE = data['Close'].values.tolist()
  L = np.arange(len(CLOSE))
  p = np.polyfit(L,CLOSE,1)
  trand = np.polyval(p,L)
  STD = np.std(CLOSE-trand)
  STD1 = trand+STD*2
  STD2 = trand+STD
  STD3 = trand-STD
  STD4 = trand-STD*2

  fig = go.Figure()
  fig.add_trace(go.Scatter(x=data.index, y=CLOSE, mode='lines', name='price', line=dict(color='blue')))
  fig.add_trace(go.Scatter(x=data.index, y=trand, mode='lines', name='趨勢', line=dict(color='grey')))
  fig.add_trace(go.Scatter(x=data.index, y=STD1, mode='lines', name='極度樂觀', line=dict(color='purple')))
  fig.add_trace(go.Scatter(x=data.index, y=STD2, mode='lines', name='樂觀', line=dict(color='red')))
  fig.add_trace(go.Scatter(x=data.index, y=STD3, mode='lines', name='悲觀', line=dict(color='brown')))
  fig.add_trace(go.Scatter(x=data.index, y=STD4, mode='lines', name='極度悲觀', line=dict(color='green')))
  fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
  ))
  symbol_dic = {'^TWOII':'櫃買指數','^TWII':'加權指數','^GSPC':'S&P 500','^IXIC':'NASDAQ','^DJI':'DOW 30','^RUT':'Russell 2000'}
  fig.update_layout(title_text=symbol_dic[symbol],title_x=0.5,title_y=0.8)
#   fig.update_layout(paper_bgcolor='white',plot_bgcolor='white',template='plotly_white')
#   fig.show()
  return fig

# for i in Symbol_list:
#   plot_five_tab(i)

utc_now = datetime.now(timezone.utc)
current_time = utc_now + timedelta(hours=8)
# time_string = current_time.strftime("%Y年%m月%d日 %H:%M:%S (%A)")
time_string = current_time.strftime("%Y年%m月%d日 (%A)")
st.title("市場五線譜")
st.write(f"{time_string}")

for i in Symbol_list:
    fig = plot_five_tab(i)
    config_static = {'staticPlot': True}
    st.plotly_chart(fig, use_container_width=True,config=config_static)
    st.markdown("---") 

# st.success("所有標的物圖表已顯示完成。")