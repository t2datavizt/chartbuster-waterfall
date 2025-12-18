import streamlit as st
import plotly.graph_objects as go

# --- 1. The Stage Setup (網頁設定) ---
st.set_page_config(page_title="Chartbuster: Liquidation Waterfall", layout="centered")

st.title("🎬 The Liquidation Waterfall")
st.markdown("### Founder's Reality Check: How much do you actually keep?")

# --- 2. The Control Panel (側邊欄控制台) ---
st.sidebar.header("💰 Scenario Settings")
exit_value = st.sidebar.slider("Total Exit Value ($M)", min_value=50, max_value=200, value=100, step=5)
debt = st.sidebar.number_input("Debt ($M)", value=20)
pref_a = st.sidebar.number_input("Series A Pref ($M)", value=20)
pref_b = st.sidebar.number_input("Series B Pref ($M)", value=30)

# 計算邏輯
founder_value = max(0, exit_value - debt - pref_a - pref_b)

# --- 3. The "Cinema" Effect (製作動態瀑布圖) ---
fig = go.Figure(go.Waterfall(
    name = "20", orientation = "v",
    measure = ["absolute", "relative", "relative", "relative", "total"],
    x = ["Total Exit", "Debt", "Series A", "Series B", "Founders"],
    textposition = "outside",
    text = [f"${exit_value}M", f"-${debt}M", f"-${pref_a}M", f"-${pref_b}M", f"${founder_value}M"],
    y = [exit_value, -debt, -pref_a, -pref_b, founder_value],
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
    
    # McKinsey Style Colors
    decreasing = {"marker":{"color":"#E0E0E0"}},  # 灰色代表被拿走的錢
    increasing = {"marker":{"color":"#051C2C"}},  # 深藍色代表總額
    totals     = {"marker":{"color":"#005EB8"}}   # 亮藍色代表創始人拿到的
))

# --- 4. Style & Animation Settings (美術指導) ---
fig.update_layout(
    title = dict(text="<b>Follow the Money</b>", font=dict(size=24)),
    showlegend = False,
    plot_bgcolor = 'white',
    font = dict(family="Arial", size=14),
    yaxis = dict(showgrid=False, zeroline=True, showticklabels=False), # 隱藏Y軸
    # Plotly 自帶進場動畫
    transition = {'duration': 500, 'easing': 'cubic-in-out'} 
)

# --- 5. Action! (顯示在網頁上) ---
st.plotly_chart(fig, use_container_width=True)

# 加上一句震撼的結論
if founder_value <= 0:
    st.error("🚨 警告：在這個估值下，創始人一毛錢都拿不到！")
else:
    st.success(f"🎉 恭喜：創始人最後帶走 ${founder_value}M (佔總額的 {founder_value/exit_value:.1%})")

st.caption("Powered by Chartbuster Logic Engine")
