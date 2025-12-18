import streamlit as st
import plotly.graph_objects as go

# --- 1. The Stage Setup (頁面設定) ---
st.set_page_config(page_title="Chartbuster: The Truth Check", layout="centered")

# --- 2. Language Selector (語言選擇器 - 這是新功能) ---
# 我們放在側邊欄的最上面，讓用戶第一眼就能選
lang_choice = st.sidebar.radio(
    "🌐 Language / 語言",
    ("English", "中文"),
    horizontal=True
)

# --- 3. The Script Dictionary (劇本資料庫) ---
# 這裡儲存所有的對白，方便管理双語
script = {
    "English": {
        "title": "🎬 The Liquidation Truth",
        "intro": """
        > *"Numbers don't lie, but they don't always tell the whole story until you make them speak.*
        > *Let's figure out exactly where you stand, so you can walk into that meeting with your head held high."*
        """,
        "sidebar_title": "⚙️ Scenario Settings",
        "sidebar_info": "Adjust these values to match your Term Sheet.",
        "lbl_exit": "Total Exit Value ($M)",
        "lbl_debt": "Debt ($M) - Paid First",
        "lbl_pref_a": "Series A Pref ($M)",
        "lbl_pref_b": "Series B Pref ($M)",
        "chart_title": "<b>Follow the Money</b>",
        "chart_steps": ["Total Exit", "Debt", "Series A", "Series B", "Founders"],
        "analysis_title": "📝 Chartbuster Diagnosis",
        "status_critical": "Critical Alert 🚨",
        "msg_critical": "Listen to me closely. Right now, the terms are eating everything. You're walking away with nothing. We need to renegotiate the Liquidation Preference cap immediately before you sign anything.",
        "status_caution": "Caution Needed ⚠️",
        "msg_caution": "You're in the game, but it's a tight squeeze. With less than 20% left for the founding team, you might feel like you're working for the investors. Let's see if we can convert some of that Preferred stock to Common.",
        "status_solid": "Solid Ground ✅",
        "msg_solid": "This is a decent outcome. You've covered your debts, paid your investors, and there's a healthy portion left for the team. It's fair, but always check if we can push for a bit more.",
        "status_outstanding": "Outstanding 🌟",
        "msg_outstanding": "This is what we fight for. You've built enough value that everyone wins, and you're taking home the lion's share. Well done.",
        "download_btn": "📄 Download Report",
        "download_tip": "💡 **Tip:** To save the chart image, hover over the top-right corner of the chart and look for the camera icon (📸).",
        "footer": "*\"Don't just look at the data. Own it.\"* — **Chartbuster**",
        "report_header": "CHARTBUSTER EXECUTIVE REPORT",
        "report_breakdown": "[The Breakdown]",
        "report_net": "FOUNDER'S NET",
        "report_expert": "[Expert Analysis]"
    },
    "中文": {
        "title": "🎬 清算的真相 (The Liquidation Truth)",
        "intro": """
        > *「數字不會說謊，但在你讓它們開口之前，它們往往只說了一半的故事。*
        > *讓我們釐清你的真實處境，這樣你才能昂首挺胸地走進那間會議室。」*
        """,
        "sidebar_title": "⚙️ 情境設定",
        "sidebar_info": "請依照你的投資條款清單 (Term Sheet) 調整數值。",
        "lbl_exit": "出場總估值 ($M)",
        "lbl_debt": "優先債務 ($M)",
        "lbl_pref_a": "A輪優先清算權 ($M)",
        "lbl_pref_b": "B輪優先清算權 ($M)",
        "chart_title": "<b>資金流向瀑布圖</b>",
        "chart_steps": ["總估值", "債務", "A輪優先股", "B輪優先股", "創始團隊"],
        "analysis_title": "📝 Chartbuster 專業診斷",
        "status_critical": "緊急警報 🚨",
        "msg_critical": "仔細聽我說。目前的條款正在吞噬一切，這樣下去你將一無所有。在簽字之前，我們必須立刻重新談判優先清算權的上限。",
        "status_caution": "需要警戒 ⚠️",
        "msg_caution": "你在局內，但處境艱難。創始團隊只剩下不到 20%，你會感覺像是在為投資人打工。讓我們看看能不能把部分優先股轉換為普通股。",
        "status_solid": "穩健的結果 ✅",
        "msg_solid": "這是一個不錯的結果。你償還了債務，回報了投資人，團隊也拿到了健康的份額。這很公平，但永遠要記得檢查是否有爭取更多的空間。",
        "status_outstanding": "傑出的表現 🌟",
        "msg_outstanding": "這就是我們奮鬥的目標。你創造了足夠的價值讓每個人都贏，而且你拿走了最大的一份。幹得好。",
        "download_btn": "📄 下載診斷報告",
        "download_tip": "💡 **小撇步：** 如果要存圖，請將滑鼠移到圖表右上角，點擊相機圖示 (📸) 即可下載。",
        "footer": "*「別只是看著數據。駕馭它。」* — **Chartbuster**",
        "report_header": "CHARTBUSTER 高層診斷報告",
        "report_breakdown": "[資金分配明細]",
        "report_net": "創始團隊淨利",
        "report_expert": "[專家分析]"
    }
}

# 設定當前語言包
t = script[lang_choice]

# --- 4. Render UI (渲染畫面) ---
st.title(t["title"])
st.markdown(t["intro"])
st.write("---")

# --- 5. Controls & Calculations (控制與計算) ---
st.sidebar.header(t["sidebar_title"])
st.sidebar.info(t["sidebar_info"])

exit_value = st.sidebar.slider(t["lbl_exit"], min_value=10, max_value=200, value=100, step=5)
debt = st.sidebar.number_input(t["lbl_debt"], value=20)
pref_a = st.sidebar.number_input(t["lbl_pref_a"], value=20)
pref_b = st.sidebar.number_input(t["lbl_pref_b"], value=30)

founder_value = max(0, exit_value - debt - pref_a - pref_b)
founder_share = (founder_value / exit_value) * 100 if exit_value > 0 else 0

# --- 6. The Logic (判斷邏輯) ---
def get_analysis_message(share, text_dict):
    if share <= 0:
        return text_dict["status_critical"], text_dict["msg_critical"]
    elif share < 20:
        return text_dict["status_caution"], text_dict["msg_caution"]
    elif share < 50:
        return text_dict["status_solid"], text_dict["msg_solid"]
    else:
        return text_dict["status_outstanding"], text_dict["msg_outstanding"]

status, message = get_analysis_message(founder_share, t)

# --- 7. The Visual (瀑布圖) ---
fig = go.Figure(go.Waterfall(
    name = "Distribution", orientation = "v",
    measure = ["absolute", "relative", "relative", "relative", "total"],
    x = t["chart_steps"], # 使用語言包中的標籤
    textposition = "outside",
    text = [f"${exit_value}M", f"-${debt}M", f"-${pref_a}M", f"-${pref_b}M", f"${founder_value}M"],
    y = [exit_value, -debt, -pref_a, -pref_b, founder_value],
    connector = {"line":{"color":"#B0B0B0"}},
    
    # 您的黑金配色 (Black & Gold)
    decreasing = {"marker":{"color":"#F0F2F6"}},
    increasing = {"marker":{"color":"#1E1E1E"}},
    totals     = {"marker":{"color":"#D4AF37"}}
))

fig.update_layout(
    title = dict(text=t["chart_title"], font=dict(size=24, color="#333333")),
    showlegend = False,
    plot_bgcolor = 'white',
    font = dict(family="Helvetica", size=14),
    yaxis = dict(showgrid=False, zeroline=True, showticklabels=False),
    height = 500
)

st.plotly_chart(fig, use_container_width=True)

# --- 8. The Diagnosis & Report (診斷與報告) ---
st.write(f"### {t['analysis_title']}")

if founder_share <= 0:
    st.error(f"**{status}**\n\n{message}")
elif founder_share < 20:
    st.warning(f"**{status}**\n\n{message}")
else:
    st.success(f"**{status}**\n\n{message}")

# 準備下載的文字檔內容
report_text = f"""
{t['report_header']}
----------------------------
Scenario: Total Exit Value of ${exit_value}M

{t['report_breakdown']}
- Debt: ${debt}M
- Series A: ${pref_a}M
- Series B: ${pref_b}M
----------------------------
{t['report_net']}: ${founder_value}M ({founder_share:.1%})

{t['report_expert']}
{message}

Generated by Chartbuster Logic Engine
"""

col1, col2 = st.columns([1, 2])

with col1:
    st.download_button(
        label=t["download_btn"],
        data=report_text,
        file_name="chartbuster_report.txt",
        mime="text/plain"
    )

with col2:
    st.caption(t["download_tip"])

# --- Footer ---
st.write("---")
st.markdown(t["footer"])
