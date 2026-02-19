import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="달력 일정 관리", page_icon="🗓️")

st.title("🗓️ 달력 기반 일정 관리 앱")

# 1. 데이터 초기화
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# 2. 사이드바 - 일정 입력
with st.sidebar:
    st.header("➕ 일정 추가")
    title = st.text_input("일정 제목")
    start_date = st.date_input("날짜", datetime.now())
    color = st.color_picker("색상 선택", "#3788d8")
    add_btn = st.button("달력에 추가")

    if add_btn and title:
        # 달력 컴포넌트 형식에 맞게 데이터 저장
        new_event = {
            "title": title,
            "start": start_date.strftime("%Y-%m-%d"),
            "backgroundColor": color,
            "borderColor": color
        }
        st.session_state.tasks.append(new_event)
        st.success("추가 완료!")

# 3. 달력 설정 및 표시
calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridMonth,dayGridWeek,dayGridDay",
    },
    "initialView": "dayGridMonth",
}

st.subheader("📅 이번 달 스케줄")
state = calendar(
    events=st.session_state.tasks,
    options=calendar_options,
    key='calendar',
)

# 4. 등록된 일정 리스트 출력
st.divider()
st.subheader("📋 전체 일정 요약")
if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)[["title", "start"]]
    df.columns = ["일정 내용", "날짜"]
    st.table(df)
else:
    st.info("등록된 일정이 없습니다.")
