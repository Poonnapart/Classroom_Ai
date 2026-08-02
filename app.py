import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Classroom Finder AI", page_icon="🏫", layout="centered"
)

hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)


@st.cache_data
def load_data():
  return pd.read_csv("classrooms.csv")


df = load_data()

st.markdown(
    "<h1 style='text-align: center; color: #1f1f1f; margin-top:"
    " 50px;'>วันนี้คุณมีเรียนวิชาอะไร?</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #666; margin-bottom: 40px;'>พิมพ์วันและช่วงเวลา เช่น 'วันจันทร์เช้า', 'วันจันทร์บ่าย' หรือพิมพ์รหัสวิชาได้เลยครับ</p>",
    unsafe_allow_html=True,
)

user_query = st.chat_input("พิมพ์เช่น วันจันทร์เช้า, EG1801 ...")

if user_query:
  with st.chat_message("user"):
    st.write(user_query)

  query_lower = user_query.strip().lower()

  result = df[
      df["day"].str.lower().str.contains(query_lower)
      | df["time"].str.lower().str.contains(query_lower)
      | df["code"].str.lower().str.contains(query_lower)
      | df["name"].str.lower().str.contains(query_lower)
  ]

  with st.chat_message("assistant"):
    if not result.empty:
      st.write(f"พบข้อมูลทั้งหมด {len(result)} รายการครับ:")
      for index, row in result.iterrows():
        response_text = (
            f"📚 **{row['code']} - {row['name']}**\n\n"
            f"📅 **วัน/เวลา:** วัน{row['day']} รอบ{row['time']}\n"
            f"📍 **สถานที่:** {row['building']} | ชั้น {row['floor']} | ห้อง {row['room']}\n"
            f"👨‍🏫 **อาจารย์ผู้สอน:** {row['instructor']}"
        )
        st.info(response_text)
    else:
      st.warning(
          f"ขออภัยครับ ไม่พบตารางเรียนสำหรับคำว่า '{user_query}'"
          " ลองใหม่อีกครั้งนะครับ"
      )
