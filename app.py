import streamlit as st
from datetime import date, datetime, timedelta
import calendar

# ── 페이지 설정 ────────────────────────────────────────────────
st.set_page_config(
    page_title="할일 & 일정 관리",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 커스텀 CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap');

/* ─── 전역 ─── */
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* ─── 사이드바 ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * { color: #e0e6f0 !important; }
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.95rem;
    padding: 6px 0;
    letter-spacing: 0.03em;
}

/* ─── 메인 배경 ─── */
.main .block-container {
    background: #f5f7fb;
    padding-top: 2rem;
}

/* ─── 헤더 ─── */
.page-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
    color: #fff;
    padding: 1.6rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.8rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 4px 24px rgba(15,52,96,0.25);
}
.page-header h1 {
    margin: 0;
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}
.page-header p {
    margin: 0.2rem 0 0;
    opacity: 0.65;
    font-size: 0.85rem;
}
.page-header .icon { font-size: 2.4rem; }

/* ─── 카드 ─── */
.card {
    background: #fff;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #eef0f5;
    transition: box-shadow 0.2s;
}
.card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.10); }

/* ─── 할일 아이템 ─── */
.todo-item {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.9rem 1rem;
    border-radius: 10px;
    border: 1px solid #eef0f5;
    background: #fff;
    margin-bottom: 0.5rem;
    transition: background 0.15s;
}
.todo-item.done {
    background: #f8fdf8;
    border-color: #d4edda;
}
.todo-item .todo-text { flex: 1; font-size: 0.95rem; }
.todo-item .todo-text.done-text {
    text-decoration: line-through;
    color: #aaa;
}

/* ─── 우선순위 배지 ─── */
.badge {
    display: inline-block;
    padding: 2px 9px;
    border-radius: 20px;
    font-size: 0.73rem;
    font-weight: 600;
    letter-spacing: 0.04em;
}
.badge-high   { background: #fde8e8; color: #c0392b; }
.badge-medium { background: #fef6e4; color: #d68910; }
.badge-low    { background: #e8f4fd; color: #2471a3; }

/* ─── 통계 카드 ─── */
.stat-card {
    background: #fff;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #eef0f5;
}
.stat-num {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1.1;
}
.stat-label {
    font-size: 0.78rem;
    color: #8a94a6;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ─── 캘린더 ─── */
.cal-wrapper {
    background: #fff;
    border-radius: 14px;
    padding: 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #eef0f5;
}
.cal-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 4px;
    margin-top: 0.8rem;
}
.cal-day-header {
    text-align: center;
    font-size: 0.75rem;
    font-weight: 700;
    color: #8a94a6;
    padding: 4px 0;
    letter-spacing: 0.06em;
}
.cal-day {
    aspect-ratio: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding: 6px 4px;
    border-radius: 8px;
    font-size: 0.85rem;
    cursor: pointer;
    border: 1px solid transparent;
    transition: background 0.15s;
    min-height: 52px;
}
.cal-day:hover { background: #f0f4ff; border-color: #c7d2fe; }
.cal-day.today {
    background: #0f3460;
    color: #fff;
    font-weight: 700;
}
.cal-day.has-event::after {
    content: '';
    display: block;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #e74c3c;
    margin-top: 2px;
}
.cal-day.empty { pointer-events: none; }

/* ─── 이벤트 아이템 ─── */
.event-item {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    padding: 0.8rem 1rem;
    border-radius: 10px;
    border-left: 3px solid #0f3460;
    background: #f7f9ff;
    margin-bottom: 0.5rem;
}
.event-time {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #0f3460;
    white-space: nowrap;
    padding-top: 1px;
}
.event-title { font-size: 0.93rem; font-weight: 500; }
.event-loc { font-size: 0.78rem; color: #8a94a6; margin-top: 1px; }

/* ─── 입력 폼 ─── */
.form-card {
    background: linear-gradient(135deg, #f7f9ff 0%, #fff 100%);
    border: 1.5px dashed #c7d2fe;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}

/* ─── Streamlit 요소 재정의 ─── */
div[data-testid="stButton"] > button {
    border-radius: 8px;
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 600;
    transition: all 0.15s;
}
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] select,
div[data-testid="stTextArea"] textarea {
    border-radius: 8px;
    border-color: #dde1ea;
}

/* ─── 탭 ─── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.3rem;
    background: #eef0f5;
    border-radius: 10px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    padding: 0.4rem 1.2rem;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: #fff;
    box-shadow: 0 1px 6px rgba(0,0,0,0.10);
}

/* ─── 구분선 ─── */
hr { border-color: #eef0f5; margin: 1rem 0; }

/* ─── 숨김 ─── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── 세션 상태 초기화 ───────────────────────────────────────────
def init_state():
    if "todos" not in st.session_state:
        st.session_state.todos = [
            {"id": 1, "text": "환경교육 커리큘럼 초안 검토", "done": False, "priority": "high",  "category": "연구", "due": "2026-03-18"},
            {"id": 2, "text": "수업 PPT 업데이트",            "done": False, "priority": "medium","category": "수업", "due": "2026-03-17"},
            {"id": 3, "text": "팀 미팅 자료 준비",            "done": True,  "priority": "low",   "category": "행정", "due": "2026-03-15"},
        ]
    if "events" not in st.session_state:
        st.session_state.events = [
            {"id": 1, "title": "지구환경연구 강의",   "date": "2026-03-17", "start": "09:00", "end": "11:00", "location": "강의실 302", "color": "#0f3460"},
            {"id": 2, "title": "연구팀 주간 미팅",    "date": "2026-03-18", "start": "14:00", "end": "15:30", "location": "회의실 B",   "color": "#1a5276"},
            {"id": 3, "title": "부산시 교육청 보고",   "date": "2026-03-20", "start": "10:00", "end": "12:00", "location": "부산시청",    "color": "#922b21"},
        ]
    if "next_todo_id" not in st.session_state:
        st.session_state.next_todo_id = 10
    if "next_event_id" not in st.session_state:
        st.session_state.next_event_id = 10
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = date.today()

init_state()

# ── 유틸리티 ───────────────────────────────────────────────────
PRIORITY_LABEL = {"high": "높음", "medium": "중간", "low": "낮음"}
PRIORITY_CLASS = {"high": "badge-high", "medium": "badge-medium", "low": "badge-low"}
DAYS_KR = ["월", "화", "수", "목", "금", "토", "일"]

def todo_stats():
    todos = st.session_state.todos
    total = len(todos)
    done  = sum(1 for t in todos if t["done"])
    return total, done, total - done

# ── 사이드바 ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📋 나의 플래너")
    st.markdown("---")
    page = st.radio("메뉴", ["🗒️ 할일 관리", "📅 일정 관리", "📊 대시보드"], label_visibility="collapsed")
    st.markdown("---")

    total, done, remaining = todo_stats()
    st.markdown(f"""
    <div style='font-size:0.8rem; opacity:0.6; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;'>오늘의 현황</div>
    <div style='display:flex; gap:1rem; flex-wrap:wrap;'>
        <div><span style='font-size:1.6rem; font-weight:700; font-family:Space Mono;'>{total}</span><br/><span style='font-size:0.7rem; opacity:0.5;'>전체</span></div>
        <div><span style='font-size:1.6rem; font-weight:700; font-family:Space Mono; color:#2ecc71;'>{done}</span><br/><span style='font-size:0.7rem; opacity:0.5;'>완료</span></div>
        <div><span style='font-size:1.6rem; font-weight:700; font-family:Space Mono; color:#e74c3c;'>{remaining}</span><br/><span style='font-size:0.7rem; opacity:0.5;'>남음</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<div style='font-size:0.75rem; opacity:0.4; text-align:center;'>📅 {date.today().strftime('%Y년 %m월 %d일')}</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 페이지 1: 할일 관리
# ═══════════════════════════════════════════════════════════════
if page == "🗒️ 할일 관리":
    st.markdown("""
    <div class='page-header'>
        <span class='icon'>🗒️</span>
        <div>
            <h1>할일 관리</h1>
            <p>오늘 해야 할 일을 추가하고 완료해보세요</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 새 할일 추가 폼
    with st.expander("➕ 새 할일 추가", expanded=False):
        st.markdown("<div class='form-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            new_text = st.text_input("할일 내용", placeholder="어떤 일을 해야 하나요?", label_visibility="collapsed")
        with col2:
            new_priority = st.selectbox("우선순위", ["high", "medium", "low"],
                                        format_func=lambda x: PRIORITY_LABEL[x])
        col3, col4 = st.columns(2)
        with col3:
            new_category = st.selectbox("카테고리", ["수업", "연구", "행정", "개인", "기타"])
        with col4:
            new_due = st.date_input("마감일", value=date.today())
        if st.button("할일 추가", use_container_width=True, type="primary"):
            if new_text.strip():
                st.session_state.todos.append({
                    "id": st.session_state.next_todo_id,
                    "text": new_text.strip(),
                    "done": False,
                    "priority": new_priority,
                    "category": new_category,
                    "due": str(new_due),
                })
                st.session_state.next_todo_id += 1
                st.success("할일이 추가되었습니다!")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── 필터
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_status = st.selectbox("상태", ["전체", "미완료", "완료"], label_visibility="collapsed")
    with col_f2:
        filter_priority = st.selectbox("우선순위", ["전체", "높음", "중간", "낮음"], label_visibility="collapsed")

    # ── 할일 목록
    todos = st.session_state.todos
    priority_map = {"높음": "high", "중간": "medium", "낮음": "low"}

    filtered = [
        t for t in todos
        if (filter_status == "전체" or (filter_status == "완료") == t["done"])
        and (filter_priority == "전체" or t["priority"] == priority_map.get(filter_priority, t["priority"]))
    ]

    if not filtered:
        st.info("조건에 맞는 할일이 없습니다.")
    else:
        for t in filtered:
            col_check, col_content, col_del = st.columns([0.08, 0.82, 0.10])
            with col_check:
                checked = st.checkbox("", value=t["done"], key=f"chk_{t['id']}")
                if checked != t["done"]:
                    for item in st.session_state.todos:
                        if item["id"] == t["id"]:
                            item["done"] = checked
                    st.rerun()
            with col_content:
                text_style = "color:#aaa; text-decoration:line-through;" if t["done"] else ""
                st.markdown(f"""
                <div style='display:flex; align-items:center; gap:0.6rem; padding:0.4rem 0;'>
                    <span style='{text_style} font-size:0.93rem; flex:1;'>{t['text']}</span>
                    <span class='badge {PRIORITY_CLASS[t["priority"]]}'>{PRIORITY_LABEL[t["priority"]]}</span>
                    <span style='font-size:0.75rem; color:#8a94a6;'>📁 {t['category']}</span>
                    <span style='font-size:0.75rem; color:#8a94a6;'>📅 {t['due']}</span>
                </div>
                """, unsafe_allow_html=True)
            with col_del:
                if st.button("🗑", key=f"del_{t['id']}", help="삭제"):
                    st.session_state.todos = [x for x in st.session_state.todos if x["id"] != t["id"]]
                    st.rerun()
            st.markdown("<hr style='margin:0.2rem 0; border-color:#f0f0f0;'/>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 페이지 2: 일정 관리
# ═══════════════════════════════════════════════════════════════
elif page == "📅 일정 관리":
    st.markdown("""
    <div class='page-header'>
        <span class='icon'>📅</span>
        <div>
            <h1>일정 관리</h1>
            <p>월별 일정을 한눈에 확인하고 추가하세요</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_cal, tab_list, tab_add = st.tabs(["📅 캘린더", "📋 목록", "➕ 추가"])

    # ── 캘린더 뷰
    with tab_cal:
        col_prev, col_title, col_next = st.columns([1, 3, 1])
        with col_prev:
            if st.button("◀", use_container_width=True):
                d = st.session_state.selected_date
                st.session_state.selected_date = (d.replace(day=1) - timedelta(days=1)).replace(day=1)
                st.rerun()
        with col_title:
            d = st.session_state.selected_date
            st.markdown(f"<h3 style='text-align:center; margin:0.4rem 0;'>{d.year}년 {d.month}월</h3>",
                        unsafe_allow_html=True)
        with col_next:
            if st.button("▶", use_container_width=True):
                d = st.session_state.selected_date
                next_month = d.replace(day=28) + timedelta(days=4)
                st.session_state.selected_date = next_month.replace(day=1)
                st.rerun()

        # 캘린더 그리드 생성
        year, month = d.year, d.month
        first_weekday, num_days = calendar.monthrange(year, month)
        first_weekday = (first_weekday) % 7  # 월=0

        # 이벤트 날짜 집합
        event_dates = {e["date"] for e in st.session_state.events}
        today_str = str(date.today())

        day_headers = "".join(f"<div class='cal-day-header'>{d}</div>" for d in DAYS_KR)
        empty_cells = "".join("<div class='cal-day empty'></div>" for _ in range(first_weekday))
        day_cells = []
        for day in range(1, num_days + 1):
            day_str = f"{year}-{month:02d}-{day:02d}"
            cls = "cal-day"
            if day_str == today_str: cls += " today"
            if day_str in event_dates: cls += " has-event"
            day_cells.append(f"<div class='{cls}'><span>{day}</span></div>")

        cal_html = f"""
        <div class='cal-wrapper'>
            <div class='cal-grid'>
                {day_headers}
                {empty_cells}
                {"".join(day_cells)}
            </div>
        </div>
        """
        st.markdown(cal_html, unsafe_allow_html=True)

        # 이번 달 이벤트 목록
        month_prefix = f"{year}-{month:02d}"
        month_events = sorted(
            [e for e in st.session_state.events if e["date"].startswith(month_prefix)],
            key=lambda x: (x["date"], x["start"])
        )
        if month_events:
            st.markdown("<br/>**이번 달 일정**", unsafe_allow_html=True)
            for ev in month_events:
                st.markdown(f"""
                <div class='event-item'>
                    <div class='event-time'>{ev['date'][5:]} {ev['start']}</div>
                    <div>
                        <div class='event-title'>{ev['title']}</div>
                        <div class='event-loc'>📍 {ev['location']} &nbsp;⏱ {ev['start']}–{ev['end']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── 목록 뷰
    with tab_list:
        events_sorted = sorted(st.session_state.events, key=lambda x: (x["date"], x["start"]))
        if not events_sorted:
            st.info("등록된 일정이 없습니다.")
        else:
            prev_date = None
            for ev in events_sorted:
                if ev["date"] != prev_date:
                    st.markdown(f"**📅 {ev['date']}**")
                    prev_date = ev["date"]
                col_ev, col_del = st.columns([0.9, 0.1])
                with col_ev:
                    st.markdown(f"""
                    <div class='event-item'>
                        <div class='event-time'>{ev['start']}<br/>{ev['end']}</div>
                        <div>
                            <div class='event-title'>{ev['title']}</div>
                            <div class='event-loc'>📍 {ev['location']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_del:
                    if st.button("🗑", key=f"evdel_{ev['id']}"):
                        st.session_state.events = [x for x in st.session_state.events if x["id"] != ev["id"]]
                        st.rerun()

    # ── 일정 추가
    with tab_add:
        st.markdown("<div class='form-card'>", unsafe_allow_html=True)
        ev_title = st.text_input("일정 제목", placeholder="강의, 미팅, 약속 등")
        col_d, col_loc = st.columns(2)
        with col_d:
            ev_date = st.date_input("날짜", value=date.today())
        with col_loc:
            ev_location = st.text_input("장소", placeholder="강의실, 온라인 등")
        col_s, col_e = st.columns(2)
        with col_s:
            ev_start = st.time_input("시작 시간", value=datetime.strptime("09:00", "%H:%M").time())
        with col_e:
            ev_end = st.time_input("종료 시간", value=datetime.strptime("10:00", "%H:%M").time())

        if st.button("일정 추가", use_container_width=True, type="primary"):
            if ev_title.strip():
                st.session_state.events.append({
                    "id": st.session_state.next_event_id,
                    "title": ev_title.strip(),
                    "date": str(ev_date),
                    "start": ev_start.strftime("%H:%M"),
                    "end": ev_end.strftime("%H:%M"),
                    "location": ev_location.strip() or "미정",
                    "color": "#0f3460",
                })
                st.session_state.next_event_id += 1
                st.success("일정이 추가되었습니다!")
                st.rerun()
            else:
                st.warning("일정 제목을 입력해주세요.")
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 페이지 3: 대시보드
# ═══════════════════════════════════════════════════════════════
elif page == "📊 대시보드":
    st.markdown("""
    <div class='page-header'>
        <span class='icon'>📊</span>
        <div>
            <h1>대시보드</h1>
            <p>할일과 일정 현황을 한눈에 확인하세요</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    total, done, remaining = todo_stats()
    completion_rate = int(done / total * 100) if total > 0 else 0

    # 통계 카드
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        (c1, str(total),           "#1a1a2e", "전체 할일"),
        (c2, str(done),            "#1a7a4a", "완료"),
        (c3, str(remaining),       "#c0392b", "남은 할일"),
        (c4, f"{completion_rate}%","#1a5276", "완료율"),
    ]
    for col, num, color, label in stats:
        with col:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-num' style='color:{color};'>{num}</div>
                <div class='stat-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    # 미완료 할일 상위 목록
    with col_left:
        st.markdown("#### 🔥 미완료 할일")
        pending = [t for t in st.session_state.todos if not t["done"]]
        priority_order = {"high": 0, "medium": 1, "low": 2}
        pending_sorted = sorted(pending, key=lambda x: priority_order[x["priority"]])
        if pending_sorted:
            for t in pending_sorted[:5]:
                st.markdown(f"""
                <div style='display:flex; align-items:center; gap:0.6rem;
                     padding:0.6rem 0.8rem; border-radius:8px;
                     background:#fff; border:1px solid #eef0f5; margin-bottom:0.4rem;'>
                    <span class='badge {PRIORITY_CLASS[t["priority"]]}'>{PRIORITY_LABEL[t["priority"]]}</span>
                    <span style='font-size:0.9rem; flex:1;'>{t['text']}</span>
                    <span style='font-size:0.75rem; color:#aaa;'>{t['due']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🎉 모든 할일을 완료했습니다!")

    # 다가오는 일정
    with col_right:
        st.markdown("#### 📅 다가오는 일정")
        today = str(date.today())
        upcoming = sorted(
            [e for e in st.session_state.events if e["date"] >= today],
            key=lambda x: (x["date"], x["start"])
        )[:5]
        if upcoming:
            for ev in upcoming:
                days_diff = (date.fromisoformat(ev["date"]) - date.today()).days
                label = "오늘" if days_diff == 0 else f"D-{days_diff}"
                st.markdown(f"""
                <div style='display:flex; align-items:center; gap:0.6rem;
                     padding:0.6rem 0.8rem; border-radius:8px;
                     background:#fff; border:1px solid #eef0f5; margin-bottom:0.4rem;'>
                    <span style='font-family:Space Mono; font-size:0.75rem;
                          background:#0f3460; color:#fff;
                          padding:2px 7px; border-radius:5px;'>{label}</span>
                    <span style='font-size:0.9rem; flex:1;'>{ev['title']}</span>
                    <span style='font-size:0.75rem; color:#aaa;'>{ev['start']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("다가오는 일정이 없습니다.")

    # 카테고리별 현황
    st.markdown("<br/>#### 📁 카테고리별 할일 현황", unsafe_allow_html=True)
    from collections import Counter
    cats = Counter(t["category"] for t in st.session_state.todos)
    if cats:
        max_count = max(cats.values())
        cols = st.columns(len(cats))
        for col, (cat, cnt) in zip(cols, cats.items()):
            with col:
                done_cnt = sum(1 for t in st.session_state.todos if t["category"] == cat and t["done"])
                rate = int(done_cnt / cnt * 100)
                st.markdown(f"""
                <div class='stat-card'>
                    <div style='font-size:0.8rem; color:#8a94a6; margin-bottom:0.3rem;'>{cat}</div>
                    <div class='stat-num' style='font-size:1.5rem; color:#1a1a2e;'>{cnt}</div>
                    <div style='background:#eef0f5; border-radius:4px; height:4px; margin:0.5rem 0;'>
                        <div style='background:#0f3460; width:{rate}%; height:4px; border-radius:4px;'></div>
                    </div>
                    <div style='font-size:0.75rem; color:#8a94a6;'>완료율 {rate}%</div>
                </div>
                """, unsafe_allow_html=True)
