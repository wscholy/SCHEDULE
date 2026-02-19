import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="스마트 일정 관리", page_icon="📅")

st.title("📅 나만의 스마트 일정 관리기")

# 1. 데이터 저장소 초기화 (세션 상태 이용)
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame(columns=["할 일", "마감일", "상태"])

# 2. 사이드바 - 새로운 일정 추가
with st.sidebar:
    st.header("➕ 새로운 일정")
    new_task = st.text_input("무엇을 해야 하나요?")
    due_date = st.date_input("마감일", datetime.now())
    add_btn = st.button("추가하기")

    if add_btn and new_task:
        new_row = pd.DataFrame([{"할 일": new_task, "마감일": due_date, "상태": "진행 중"}])
        st.session_state.tasks = pd.concat([st.session_state.tasks, new_row], ignore_index=True)
        st.success("일정이 추가되었습니다!")

# 3. 메인 화면 - 일정 목록 및 관리
st.subheader("📝 현재 일정 목록")

if not st.session_state.tasks.empty:
    # 데이터프레임 표시 (편집 가능하도록)
    edited_df = st.data_editor(
        st.session_state.tasks,
        column_config={
            "상태": st.column_config.SelectboxColumn(
                "상태", options=["진행 중", "완료", "보류"], required=True
            )
        },
        use_container_width=True,
        num_rows="dynamic"
    )
    st.session_state.tasks = edited_df

    # 4. 통계 시각화
    st.divider()
    st.subheader("📊 진행 상황 요약")
    
    status_counts = st.session_state.tasks["상태"].value_counts().reset_index()
    status_counts.columns = ["상태", "개수"]
    
    fig = px.pie(status_counts, values="개수", names="상태", 
                 color="상태", 
                 color_discrete_map={'진행 중':'#EF553B', '완료':'#00CC96', '보류':'#636EFA'},
                 hole=0.4)
    st.plotly_chart(fig)
else:
    st.info("현재 등록된 일정이 없습니다. 사이드바에서 일정을 추가해 보세요!")
