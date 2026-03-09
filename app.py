import streamlit as st
import pandas as pd
import random

# ─────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="日本語 単語帳",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CSS 스타일
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;700&family=Noto+Serif+JP:wght@400;700&family=Inter:wght@300;400;600&display=swap');

.stApp {
    background: linear-gradient(135deg, #fff7f0 0%, #fff0f5 50%, #f0f4ff 100%);
    font-family: 'Inter', sans-serif;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a0a2e 0%, #2d1b4e 100%);
    border-right: 1px solid rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] * { color: #f0e6ff !important; }

.main-title {
    font-family: 'Noto Serif JP', serif;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #b5179e, #7209b7, #3a0ca3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 0.2rem;
    letter-spacing: 0.05em;
}
.sub-title {
    text-align: center;
    color: #9b6fa0;
    font-size: 0.9rem;
    letter-spacing: 0.2em;
    margin-bottom: 2rem;
    font-weight: 300;
}
.word-card {
    background: white;
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin: 0.5rem 0;
    box-shadow: 0 2px 12px rgba(114,9,183,0.08);
    border-left: 4px solid #b5179e;
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
}
.word-card:hover {
    transform: translateX(4px);
    box-shadow: 0 4px 20px rgba(114,9,183,0.15);
}
.word-kanji { font-family: 'Noto Serif JP', serif; font-size: 1.6rem; font-weight: 700; color: #1a0a2e; }
.word-hira  { font-family: 'Noto Sans JP', sans-serif; font-size: 0.95rem; color: #b5179e; margin: 0.1rem 0; }
.word-romaji { font-size: 0.8rem; color: #aaa; font-style: italic; }
.word-meaning { font-size: 1rem; color: #444; margin-top: 0.3rem; }
.word-tag {
    display: inline-block;
    background: linear-gradient(135deg, #f0e6ff, #ffe0f5);
    color: #7209b7;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 0.4rem;
}
.quiz-card {
    background: white;
    border-radius: 24px;
    padding: 2.5rem;
    text-align: center;
    box-shadow: 0 8px 40px rgba(114,9,183,0.12);
    border: 2px solid rgba(181,23,158,0.15);
    margin: 1rem 0;
}
.quiz-question { font-family: 'Noto Serif JP', serif; font-size: 3rem; font-weight: 700; color: #1a0a2e; margin-bottom: 0.5rem; }
.quiz-hint { color: #b5179e; font-size: 1rem; margin-bottom: 2rem; }
.stat-card { background: white; border-radius: 16px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 16px rgba(114,9,183,0.1); }
.stat-num { font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #b5179e, #7209b7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.stat-label { color: #888; font-size: 0.85rem; margin-top: 0.3rem; }
.correct-badge { background: linear-gradient(135deg, #10b981, #059669); color: white; border-radius: 12px; padding: 1rem 2rem; text-align: center; font-size: 1.2rem; font-weight: 700; margin: 1rem 0; }
.wrong-badge { background: linear-gradient(135deg, #ef4444, #dc2626); color: white; border-radius: 12px; padding: 1rem 2rem; text-align: center; font-size: 1.2rem; font-weight: 700; margin: 1rem 0; }
.section-header { font-family: 'Noto Serif JP', serif; font-size: 1.4rem; color: #1a0a2e; border-bottom: 2px solid #b5179e; padding-bottom: 0.4rem; margin: 1.5rem 0 1rem 0; }
.trace-container {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 4px 24px rgba(114,9,183,0.12);
    margin: 1rem 0;
    text-align: center;
}
.trace-word {
    font-family: 'Noto Serif JP', serif;
    font-size: 5rem;
    font-weight: 700;
    color: rgba(181,23,158,0.15);
    letter-spacing: 0.2em;
    line-height: 1.2;
    user-select: none;
}
.trace-guide { font-size: 0.85rem; color: #aaa; margin-top: 0.5rem; }
hr { border-color: rgba(181,23,158,0.15) !important; }
.stButton > button { border-radius: 10px; font-family: 'Inter', sans-serif; font-weight: 600; transition: all 0.2s; }
.stButton > button:hover { transform: translateY(-1px); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 기본 단어 데이터 (40개)
# ─────────────────────────────────────────
DEFAULT_WORDS = [
    {"kanji": "食べる",   "hiragana": "たべる",     "romaji": "taberu",      "meaning": "먹다",       "category": "동사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "飲む",     "hiragana": "のむ",       "romaji": "nomu",        "meaning": "마시다",     "category": "동사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "見る",     "hiragana": "みる",       "romaji": "miru",        "meaning": "보다",       "category": "동사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "行く",     "hiragana": "いく",       "romaji": "iku",         "meaning": "가다",       "category": "동사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "来る",     "hiragana": "くる",       "romaji": "kuru",        "meaning": "오다",       "category": "동사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "書く",     "hiragana": "かく",       "romaji": "kaku",        "meaning": "쓰다",       "category": "동사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "読む",     "hiragana": "よむ",       "romaji": "yomu",        "meaning": "읽다",       "category": "동사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "話す",     "hiragana": "はなす",     "romaji": "hanasu",      "meaning": "말하다",     "category": "동사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "聞く",     "hiragana": "きく",       "romaji": "kiku",        "meaning": "듣다/묻다",  "category": "동사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "買う",     "hiragana": "かう",       "romaji": "kau",         "meaning": "사다",       "category": "동사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "学校",     "hiragana": "がっこう",   "romaji": "gakkou",      "meaning": "학교",       "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "電車",     "hiragana": "でんしゃ",   "romaji": "densha",      "meaning": "전철",       "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "友達",     "hiragana": "ともだち",   "romaji": "tomodachi",   "meaning": "친구",       "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "今日",     "hiragana": "きょう",     "romaji": "kyou",        "meaning": "오늘",       "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "昨日",     "hiragana": "きのう",     "romaji": "kinou",       "meaning": "어제",       "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "明日",     "hiragana": "あした",     "romaji": "ashita",      "meaning": "내일",       "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "空",       "hiragana": "そら",       "romaji": "sora",        "meaning": "하늘",       "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "海",       "hiragana": "うみ",       "romaji": "umi",         "meaning": "바다",       "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "山",       "hiragana": "やま",       "romaji": "yama",        "meaning": "산",         "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "花",       "hiragana": "はな",       "romaji": "hana",        "meaning": "꽃",         "category": "명사",   "favorite": True,  "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "猫",       "hiragana": "ねこ",       "romaji": "neko",        "meaning": "고양이",     "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "犬",       "hiragana": "いぬ",       "romaji": "inu",         "meaning": "강아지",     "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "水",       "hiragana": "みず",       "romaji": "mizu",        "meaning": "물",         "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "火",       "hiragana": "ひ",         "romaji": "hi",          "meaning": "불",         "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "木",       "hiragana": "き",         "romaji": "ki",          "meaning": "나무",       "category": "명사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "美しい",   "hiragana": "うつくしい", "romaji": "utsukushii",  "meaning": "아름답다",   "category": "형용사", "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "楽しい",   "hiragana": "たのしい",   "romaji": "tanoshii",    "meaning": "즐겁다",     "category": "형용사", "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "難しい",   "hiragana": "むずかしい", "romaji": "muzukashii",  "meaning": "어렵다",     "category": "형용사", "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "嬉しい",   "hiragana": "うれしい",   "romaji": "ureshii",     "meaning": "기쁘다",     "category": "형용사", "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "悲しい",   "hiragana": "かなしい",   "romaji": "kanashii",    "meaning": "슬프다",     "category": "형용사", "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "暖かい",   "hiragana": "あたたかい", "romaji": "atatakai",    "meaning": "따뜻하다",   "category": "형용사", "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "寒い",     "hiragana": "さむい",     "romaji": "samui",       "meaning": "춥다",       "category": "형용사", "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "暑い",     "hiragana": "あつい",     "romaji": "atsui",       "meaning": "덥다",       "category": "형용사", "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "とても",   "hiragana": "とても",     "romaji": "totemo",      "meaning": "매우",       "category": "부사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "少し",     "hiragana": "すこし",     "romaji": "sukoshi",     "meaning": "조금",       "category": "부사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "もう",     "hiragana": "もう",       "romaji": "mou",         "meaning": "이미/벌써",  "category": "부사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "まだ",     "hiragana": "まだ",       "romaji": "mada",        "meaning": "아직",       "category": "부사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "いつも",   "hiragana": "いつも",     "romaji": "itsumo",      "meaning": "항상",       "category": "부사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "一緒に",   "hiragana": "いっしょに", "romaji": "issho ni",    "meaning": "함께",       "category": "부사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
    {"kanji": "ゆっくり", "hiragana": "ゆっくり",   "romaji": "yukkuri",     "meaning": "천천히",     "category": "부사",   "favorite": False, "correct": 0, "wrong": 0, "trace_count": 0},
]

CATEGORIES = ["전체", "동사", "명사", "형용사", "부사", "기타"]

# ─────────────────────────────────────────
# 세션 상태 초기화
# ─────────────────────────────────────────
def init_state():
    defaults = {
        "words": DEFAULT_WORDS.copy(),
        "quiz_index": 0, "quiz_words": [], "quiz_answered": False,
        "quiz_result": None, "quiz_score": {"correct": 0, "wrong": 0},
        "quiz_mode": "not_started", "quiz_type": "kanji→뜻",
        "show_kanji": True, "show_hiragana": True,
        "show_romaji": True, "show_meaning": True,
        "trace_idx": 0, "trace_words": [], "trace_mode": "not_started",
        "trace_user_input": "", "trace_checked": False,
        "trace_check_result": None, "trace_show": "한국어 뜻만",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────
# 헬퍼 함수
# ─────────────────────────────────────────
def toggle_favorite(idx):
    st.session_state.words[idx]["favorite"] = not st.session_state.words[idx]["favorite"]

def delete_word(idx):
    st.session_state.words.pop(idx)

def render_word_card(w, sk, sh, sr, sm, border_color="#b5179e"):
    parts = []
    if sk: parts.append(f'<span class="word-kanji">{w["kanji"]}</span>')
    if sh: parts.append(f'<div class="word-hira">{w["hiragana"]}</div>')
    if sr: parts.append(f'<div class="word-romaji">{w["romaji"]}</div>')
    if sm: parts.append(f'<div class="word-meaning">🔹 {w["meaning"]}</div>')
    acc = round(w["correct"]/(w["correct"]+w["wrong"])*100) if (w["correct"]+w["wrong"]) > 0 else None
    tags = f'<span class="word-tag">{w["category"]}</span>'
    if acc is not None: tags += f' <span class="word-tag">정답률 {acc}%</span>'
    if w.get("trace_count", 0) > 0: tags += f' <span class="word-tag">✍️ {w["trace_count"]}회</span>'
    parts.append(tags)
    return f'<div class="word-card" style="border-left-color:{border_color};">{"".join(parts)}</div>'

def start_quiz(word_list, quiz_type):
    shuffled = word_list.copy(); random.shuffle(shuffled)
    st.session_state.quiz_words = shuffled
    st.session_state.quiz_index = 0
    st.session_state.quiz_answered = False
    st.session_state.quiz_result = None
    st.session_state.quiz_score = {"correct": 0, "wrong": 0}
    st.session_state.quiz_mode = "in_progress"
    st.session_state.quiz_type = quiz_type

def generate_choices(current, all_words, quiz_type):
    others = [w for w in all_words if w["kanji"] != current["kanji"]]
    wrongs = random.sample(others, min(3, len(others)))
    if quiz_type == "뜻→kanji":
        return random.sample([current["kanji"]] + [w["kanji"] for w in wrongs], 4)
    else:
        return random.sample([current["meaning"]] + [w["meaning"] for w in wrongs], 4)

# ─────────────────────────────────────────
# 사이드바
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌸 日本語 単語帳")
    st.markdown("---")
    menu = st.radio("메뉴", ["📖 단어장", "➕ 단어 추가", "❤️ 즐겨찾기", "🧠 퀴즈", "✍️ 따라쓰기", "📊 통계", "⚙️ 표기 설정"], label_visibility="collapsed")
    st.markdown("---")
    total  = len(st.session_state.words)
    favs   = sum(1 for w in st.session_state.words if w["favorite"])
    learned= sum(1 for w in st.session_state.words if w["correct"] > 0)
    traced = sum(1 for w in st.session_state.words if w.get("trace_count", 0) > 0)
    st.markdown(f"**전체 단어** `{total}개`")
    st.markdown(f"**즐겨찾기** `{favs}개`")
    st.markdown(f"**퀴즈 학습** `{learned}개`")
    st.markdown(f"**따라쓰기** `{traced}개`")
    st.markdown("---")
    st.markdown("**⚙️ 빠른 표기 설정**")
    st.session_state.show_kanji    = st.checkbox("한자",      st.session_state.show_kanji,    key="sb_kanji")
    st.session_state.show_hiragana = st.checkbox("히라가나",  st.session_state.show_hiragana, key="sb_hira")
    st.session_state.show_romaji   = st.checkbox("로마자",    st.session_state.show_romaji,   key="sb_romaji")
    st.session_state.show_meaning  = st.checkbox("한국어 뜻",st.session_state.show_meaning,  key="sb_meaning")

# 타이틀
st.markdown('<div class="main-title">日本語 単語帳</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">🌸 JAPANESE VOCABULARY NOTEBOOK 🌸</div>', unsafe_allow_html=True)

SK = st.session_state.show_kanji
SH = st.session_state.show_hiragana
SR = st.session_state.show_romaji
SM = st.session_state.show_meaning

# ═══════════════════════════════════════════
# 📖 단어장
# ═══════════════════════════════════════════
if menu == "📖 단어장":
    col_s, col_c = st.columns([3, 1])
    with col_s: search = st.text_input("🔍 검색 (한자·히라가나·뜻)", placeholder="예: 食べる / たべる / 먹다")
    with col_c: cat_filter = st.selectbox("카테고리", CATEGORIES)

    words = st.session_state.words
    if search:    words = [w for w in words if search in w["kanji"] or search in w["hiragana"] or search in w["meaning"]]
    if cat_filter != "전체": words = [w for w in words if w["category"] == cat_filter]

    st.markdown(f'<div class="section-header">단어 목록 <span style="font-size:1rem;color:#b5179e;">({len(words)}개)</span></div>', unsafe_allow_html=True)

    if not words:
        st.info("표시할 단어가 없습니다.")
    else:
        for w in words:
            real_idx = st.session_state.words.index(w)
            star = "⭐" if w["favorite"] else "☆"
            c1, c2, c3, c4 = st.columns([6, 1, 1, 1])
            with c1: st.markdown(render_word_card(w, SK, SH, SR, SM), unsafe_allow_html=True)
            with c2:
                if st.button(star, key=f"fav_{real_idx}"): toggle_favorite(real_idx); st.rerun()
            with c3:
                if st.button("✏️", key=f"edit_{real_idx}"):
                    st.session_state[f"editing_{real_idx}"] = not st.session_state.get(f"editing_{real_idx}", False); st.rerun()
            with c4:
                if st.button("🗑️", key=f"del_{real_idx}"): delete_word(real_idx); st.rerun()

            if st.session_state.get(f"editing_{real_idx}", False):
                with st.expander("✏️ 단어 편집", expanded=True):
                    e1 = st.text_input("한자",     value=w["kanji"],    key=f"ek_{real_idx}")
                    e2 = st.text_input("히라가나", value=w["hiragana"], key=f"eh_{real_idx}")
                    e3 = st.text_input("로마자",   value=w["romaji"],   key=f"er_{real_idx}")
                    e4 = st.text_input("뜻",       value=w["meaning"],  key=f"em_{real_idx}")
                    opts = ["동사","명사","형용사","부사","기타"]
                    e5 = st.selectbox("카테고리", opts, index=opts.index(w["category"]) if w["category"] in opts else 0, key=f"ec_{real_idx}")
                    ca, cb = st.columns(2)
                    with ca:
                        if st.button("💾 저장", key=f"save_{real_idx}"):
                            st.session_state.words[real_idx].update({"kanji":e1,"hiragana":e2,"romaji":e3,"meaning":e4,"category":e5})
                            st.session_state[f"editing_{real_idx}"] = False; st.rerun()
                    with cb:
                        if st.button("❌ 취소", key=f"cancel_{real_idx}"):
                            st.session_state[f"editing_{real_idx}"] = False; st.rerun()

# ═══════════════════════════════════════════
# ➕ 단어 추가
# ═══════════════════════════════════════════
elif menu == "➕ 단어 추가":
    st.markdown('<div class="section-header">새 단어 추가</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["✍️ 직접 입력", "📂 CSV 업로드"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            nk = st.text_input("한자 / 표기",  placeholder="例: 食べる")
            nh = st.text_input("히라가나",      placeholder="例: たべる")
            nr = st.text_input("로마자(발음)", placeholder="例: taberu")
        with c2:
            nm = st.text_input("한국어 뜻",    placeholder="例: 먹다")
            nc = st.selectbox("카테고리", ["동사","명사","형용사","부사","기타"])
            nf = st.checkbox("⭐ 즐겨찾기에 추가")
        if st.button("➕ 단어 추가하기", use_container_width=True):
            if nk and nh and nm:
                st.session_state.words.append({"kanji":nk,"hiragana":nh,"romaji":nr,"meaning":nm,"category":nc,"favorite":nf,"correct":0,"wrong":0,"trace_count":0})
                st.success(f"✅ '{nk}' 단어가 추가되었습니다!")
                st.balloons()
            else:
                st.warning("한자, 히라가나, 뜻은 필수입니다.")

    with tab2:
        st.info("CSV 형식: `kanji, hiragana, romaji, meaning, category`")
        st.code("食べる,たべる,taberu,먹다,동사", language="")
        uploaded = st.file_uploader("CSV 파일 업로드", type="csv")
        if uploaded:
            try:
                df = pd.read_csv(uploaded, header=None, names=["kanji","hiragana","romaji","meaning","category"])
                cnt = 0
                for _, row in df.iterrows():
                    st.session_state.words.append({"kanji":str(row.get("kanji","")),"hiragana":str(row.get("hiragana","")),"romaji":str(row.get("romaji","")),"meaning":str(row.get("meaning","")),"category":str(row.get("category","기타")),"favorite":False,"correct":0,"wrong":0,"trace_count":0})
                    cnt += 1
                st.success(f"✅ {cnt}개 단어를 추가했습니다!"); st.rerun()
            except Exception as e:
                st.error(f"오류: {e}")

# ═══════════════════════════════════════════
# ❤️ 즐겨찾기
# ═══════════════════════════════════════════
elif menu == "❤️ 즐겨찾기":
    st.markdown('<div class="section-header">⭐ 즐겨찾기 단어</div>', unsafe_allow_html=True)
    favs = [(i, w) for i, w in enumerate(st.session_state.words) if w["favorite"]]
    if not favs:
        st.info("즐겨찾기한 단어가 없습니다. 단어장에서 ☆ 버튼을 눌러보세요!")
    else:
        for real_idx, w in favs:
            c1, c2 = st.columns([8, 1])
            with c1: st.markdown(render_word_card(w, SK, SH, SR, SM, "#f59e0b"), unsafe_allow_html=True)
            with c2:
                if st.button("⭐", key=f"unfav_{real_idx}"): toggle_favorite(real_idx); st.rerun()

# ═══════════════════════════════════════════
# 🧠 퀴즈
# ═══════════════════════════════════════════
elif menu == "🧠 퀴즈":
    st.markdown('<div class="section-header">🧠 단어 퀴즈</div>', unsafe_allow_html=True)

    if st.session_state.quiz_mode == "not_started":
        c1, c2 = st.columns(2)
        with c1: quiz_source = st.selectbox("단어 범위", ["전체 단어","즐겨찾기만","동사만","명사만","형용사만","부사만"])
        with c2: quiz_type   = st.selectbox("퀴즈 유형", ["kanji→뜻","뜻→kanji","hiragana→뜻"])

        src = {"전체 단어": lambda w: True, "즐겨찾기만": lambda w: w["favorite"],
               "동사만": lambda w: w["category"]=="동사", "명사만": lambda w: w["category"]=="명사",
               "형용사만": lambda w: w["category"]=="형용사", "부사만": lambda w: w["category"]=="부사"}
        pool = [w for w in st.session_state.words if src[quiz_source](w)]
        num_q = st.slider("문제 수", 5, max(5, min(30, len(pool))), min(10, max(5, len(pool))))

        if st.button("🚀 퀴즈 시작!", use_container_width=True):
            if len(pool) < 4: st.warning("최소 4개 이상의 단어가 필요합니다.")
            else: start_quiz(random.sample(pool, num_q), quiz_type); st.rerun()

    elif st.session_state.quiz_mode == "in_progress":
        q_idx = st.session_state.quiz_index
        q_words = st.session_state.quiz_words
        total_q = len(q_words)
        st.progress(q_idx / total_q, text=f"문제 {q_idx+1} / {total_q}  |  ✅ {st.session_state.quiz_score['correct']}  ❌ {st.session_state.quiz_score['wrong']}")

        current = q_words[q_idx]
        qtype   = st.session_state.quiz_type
        choices = generate_choices(current, st.session_state.words, qtype)

        if qtype == "kanji→뜻":
            q_display, q_hint, answer = current["kanji"], current["hiragana"], current["meaning"]
        elif qtype == "뜻→kanji":
            q_display, q_hint, answer = current["meaning"], "한국어 → 일본어(한자)", current["kanji"]
        else:
            q_display, q_hint, answer = current["hiragana"], "히라가나 → 한국어 뜻", current["meaning"]

        st.markdown(f'<div class="quiz-card"><div class="quiz-question">{q_display}</div><div class="quiz-hint">{q_hint}</div></div>', unsafe_allow_html=True)

        if not st.session_state.quiz_answered:
            cols = st.columns(2)
            for i, choice in enumerate(choices):
                with cols[i % 2]:
                    if st.button(choice, key=f"ch_{i}", use_container_width=True):
                        correct = (choice == answer)
                        st.session_state.quiz_answered = True
                        st.session_state.quiz_result   = (correct, choice, answer)
                        ri = next((j for j,w in enumerate(st.session_state.words) if w["kanji"]==current["kanji"]), None)
                        if ri is not None:
                            k = "correct" if correct else "wrong"
                            st.session_state.words[ri][k] += 1
                            st.session_state.quiz_score[k] += 1
                        st.rerun()
        else:
            correct, _, right = st.session_state.quiz_result
            if correct: st.markdown('<div class="correct-badge">🎉 정답입니다!</div>', unsafe_allow_html=True)
            else:       st.markdown(f'<div class="wrong-badge">❌ 틀렸습니다. 정답: <b>{right}</b></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="word-card" style="margin:1rem 0;"><span class="word-kanji">{current["kanji"]}</span><div class="word-hira">{current["hiragana"]} · {current["romaji"]}</div><div class="word-meaning">🔹 {current["meaning"]}</div></div>', unsafe_allow_html=True)

            if q_idx + 1 < total_q:
                if st.button("다음 문제 →", use_container_width=True):
                    st.session_state.quiz_index += 1; st.session_state.quiz_answered = False; st.session_state.quiz_result = None; st.rerun()
            else:
                if st.button("📊 결과 보기", use_container_width=True):
                    st.session_state.quiz_mode = "finished"; st.rerun()

    elif st.session_state.quiz_mode == "finished":
        score = st.session_state.quiz_score
        total_q = score["correct"] + score["wrong"]
        pct   = round(score["correct"] / total_q * 100) if total_q > 0 else 0
        emoji = "🎊" if pct >= 80 else ("👍" if pct >= 60 else "💪")
        msg   = "훌륭해요!" if pct >= 80 else ("잘했어요!" if pct >= 60 else "더 연습해봐요!")
        st.markdown(f'<div class="quiz-card"><div style="font-size:4rem;">{emoji}</div><div style="font-family:Noto Serif JP,serif;font-size:2rem;font-weight:700;color:#1a0a2e;margin:1rem 0;">{msg}</div><div style="font-size:3rem;font-weight:700;background:linear-gradient(135deg,#b5179e,#7209b7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{pct}점</div><div style="color:#888;margin-top:0.5rem;">정답 {score["correct"]}개 / 오답 {score["wrong"]}개 (총 {total_q}문제)</div></div>', unsafe_allow_html=True)
        if st.button("🔄 다시 퀴즈 시작", use_container_width=True):
            st.session_state.quiz_mode = "not_started"; st.rerun()

# ═══════════════════════════════════════════
# ✍️ 따라쓰기
# ═══════════════════════════════════════════
elif menu == "✍️ 따라쓰기":
    st.markdown('<div class="section-header">✍️ 따라쓰기 연습</div>', unsafe_allow_html=True)

    if st.session_state.trace_mode == "not_started":
        st.markdown('<div style="background:white;border-radius:16px;padding:1.2rem 1.5rem;box-shadow:0 2px 12px rgba(114,9,183,0.08);margin-bottom:1rem;color:#555;">단어를 보고 노트에 직접 써보거나, 입력창에 히라가나·로마자·한자를 입력해 정답을 확인하세요. 필획 순서 링크도 제공됩니다!</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1: tr_src  = st.selectbox("연습할 단어 범위", ["전체 단어","즐겨찾기만","동사만","명사만","형용사만","오답 단어"])
        with c2: tr_show = st.selectbox("힌트 표시", ["한국어 뜻만","뜻+한자","뜻+히라가나","모두 보기"])
        tr_cnt = st.slider("연습할 단어 수", 3, min(20, len(st.session_state.words)), 5)

        src = {"전체 단어": lambda w: True, "즐겨찾기만": lambda w: w["favorite"],
               "동사만": lambda w: w["category"]=="동사", "명사만": lambda w: w["category"]=="명사",
               "형용사만": lambda w: w["category"]=="형용사", "오답 단어": lambda w: w["wrong"] > 0}
        pool = [w for w in st.session_state.words if src[tr_src](w)]

        if st.button("✍️ 따라쓰기 시작!", use_container_width=True):
            if not pool: st.warning("해당 범위에 단어가 없습니다.")
            else:
                shuffled = pool.copy(); random.shuffle(shuffled)
                st.session_state.trace_words = shuffled[:tr_cnt]
                st.session_state.trace_idx   = 0
                st.session_state.trace_mode  = "in_progress"
                st.session_state.trace_show  = tr_show
                st.session_state.trace_checked = False
                st.session_state.trace_check_result = None
                st.rerun()

    elif st.session_state.trace_mode == "in_progress":
        t_idx   = st.session_state.trace_idx
        t_words = st.session_state.trace_words
        total_t = len(t_words)
        current = t_words[t_idx]

        st.progress(t_idx / total_t, text=f"✍️ {t_idx+1} / {total_t} 번째 단어")

        tr_show = st.session_state.get("trace_show", "한국어 뜻만")
        hint_k  = current["kanji"]    if tr_show in ["뜻+한자","모두 보기"] else ""
        hint_h  = current["hiragana"] if tr_show in ["뜻+히라가나","모두 보기"] else ""
        hint_r  = current["romaji"]   if tr_show == "모두 보기" else ""

        sep = "&nbsp;&nbsp;·&nbsp;&nbsp;"
        hint_line = f'🔹 {current["meaning"]}'
        if hint_k: hint_line += sep + hint_k
        if hint_h: hint_line += sep + hint_h
        if hint_r: hint_line += sep + hint_r

        st.markdown(f"""
        <div class="trace-container">
            <div style="font-size:0.9rem;color:#b5179e;font-weight:600;letter-spacing:0.1em;margin-bottom:1rem;">{hint_line}</div>
            <div class="trace-word">{current['kanji']}</div>
            <div class="trace-guide">위 단어를 보고 노트에 써보거나, 아래 입력창에 타이핑해 보세요</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 📝 정답 입력 (히라가나·로마자·한자 모두 가능)")
        ci, cb = st.columns([4, 1])
        with ci:
            user_input = st.text_input("입력", value="", placeholder=f"예: {current['hiragana']} 또는 {current['romaji']}", key=f"ti_{t_idx}", label_visibility="collapsed")
        with cb:
            check_btn = st.button("✅ 확인", key=f"tc_{t_idx}", use_container_width=True)

        if check_btn and user_input.strip():
            inp = user_input.strip().lower().replace(" ", "")
            is_correct = inp in [
                current["hiragana"].replace(" ",""),
                current["romaji"].lower().replace(" ",""),
                current["kanji"].replace(" ","")
            ]
            st.session_state.trace_checked      = True
            st.session_state.trace_check_result = is_correct
            ri = next((j for j,w in enumerate(st.session_state.words) if w["kanji"]==current["kanji"]), None)
            if ri is not None:
                st.session_state.words[ri]["trace_count"] = st.session_state.words[ri].get("trace_count", 0) + 1
            st.rerun()

        if st.session_state.trace_checked:
            result = st.session_state.trace_check_result
            if result:
                st.markdown(f'<div class="correct-badge">🎉 정답! &nbsp; <b>{current["kanji"]}</b> ({current["hiragana"]}) = {current["meaning"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="wrong-badge">❌ 다시 도전! &nbsp; 정답: <b>{current["kanji"]}</b> · {current["hiragana"]} · {current["romaji"]}</div>', unsafe_allow_html=True)

            st.markdown(f'<div style="text-align:center;margin-top:0.5rem;"><a href="https://jisho.org/search/{current["kanji"]}%20%23kanji" target="_blank" style="color:#7209b7;font-size:0.85rem;text-decoration:none;">📖 {current["kanji"]} 필획 순서 보기 (jisho.org) →</a></div>', unsafe_allow_html=True)

            cn, cr = st.columns(2)
            with cn:
                next_label = "다음 단어 →" if t_idx + 1 < total_t else "🏁 완료"
                if st.button(next_label, use_container_width=True, key=f"tn_{t_idx}"):
                    if t_idx + 1 < total_t:
                        st.session_state.trace_idx += 1
                        st.session_state.trace_checked = False
                        st.session_state.trace_check_result = None
                    else:
                        st.session_state.trace_mode = "finished"
                    st.rerun()
            with cr:
                if st.button("🔄 다시 쓰기", use_container_width=True, key=f"tret_{t_idx}"):
                    st.session_state.trace_checked = False; st.session_state.trace_check_result = None; st.rerun()
        else:
            if st.button("⏭️ 건너뛰기", key=f"tsk_{t_idx}"):
                if t_idx + 1 < total_t:
                    st.session_state.trace_idx += 1; st.session_state.trace_checked = False
                else:
                    st.session_state.trace_mode = "finished"
                st.rerun()

    elif st.session_state.trace_mode == "finished":
        total_trace = sum(w.get("trace_count", 0) for w in st.session_state.words)
        st.markdown(f'<div class="quiz-card"><div style="font-size:4rem;">✍️</div><div style="font-family:Noto Serif JP,serif;font-size:2rem;font-weight:700;color:#1a0a2e;margin:1rem 0;">따라쓰기 완료!</div><div style="font-size:1.2rem;color:#7209b7;font-weight:600;">오늘 {len(st.session_state.trace_words)}개 단어 연습 완료</div><div style="color:#888;margin-top:0.5rem;">누적 따라쓰기 {total_trace}회</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">이번 연습 단어</div>', unsafe_allow_html=True)
        for w in st.session_state.trace_words:
            st.markdown(f'<div class="word-card" style="border-left-color:#6366f1;"><span class="word-kanji">{w["kanji"]}</span><div class="word-hira">{w["hiragana"]} · {w["romaji"]}</div><div class="word-meaning">🔹 {w["meaning"]}</div><span class="word-tag">✍️ {w.get("trace_count",0)}회</span></div>', unsafe_allow_html=True)
        if st.button("🔄 다시 따라쓰기", use_container_width=True):
            st.session_state.trace_mode = "not_started"; st.rerun()

# ═══════════════════════════════════════════
# 📊 통계
# ═══════════════════════════════════════════
elif menu == "📊 통계":
    st.markdown('<div class="section-header">📊 학습 통계</div>', unsafe_allow_html=True)
    words = st.session_state.words
    total = len(words)
    favs  = sum(1 for w in words if w["favorite"])
    learned = sum(1 for w in words if w["correct"] > 0)
    traced  = sum(1 for w in words if w.get("trace_count", 0) > 0)
    tc = sum(w["correct"] for w in words); tw = sum(w["wrong"] for w in words)
    overall_acc = round(tc/(tc+tw)*100) if (tc+tw) > 0 else 0

    c1,c2,c3,c4,c5 = st.columns(5)
    for col, num, label in [(c1,total,"전체 단어"),(c2,favs,"즐겨찾기"),(c3,learned,"퀴즈 학습"),(c4,traced,"따라쓰기"),(c5,f"{overall_acc}%","전체 정답률")]:
        with col: st.markdown(f'<div class="stat-card"><div class="stat-num">{num}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header" style="margin-top:2rem;">카테고리별 단어 수</div>', unsafe_allow_html=True)
    cat_counts = {}
    for w in words: cat_counts[w["category"]] = cat_counts.get(w["category"], 0) + 1
    if cat_counts:
        st.bar_chart(pd.DataFrame(list(cat_counts.items()), columns=["카테고리","단어 수"]).set_index("카테고리"))

    cl, cr = st.columns(2)
    with cl:
        st.markdown('<div class="section-header">✅ 정답률 TOP 5</div>', unsafe_allow_html=True)
        scored = sorted([(w, round(w["correct"]/(w["correct"]+w["wrong"])*100)) for w in words if (w["correct"]+w["wrong"])>0], key=lambda x:-x[1])
        if scored:
            for w, acc in scored[:5]: st.markdown(f'<div class="word-card"><span class="word-kanji">{w["kanji"]}</span><span style="float:right;font-size:1.2rem;font-weight:700;color:#10b981;">{acc}%</span><div class="word-hira">{w["hiragana"]} · {w["meaning"]}</div></div>', unsafe_allow_html=True)
        else: st.info("아직 퀴즈 기록이 없습니다.")
    with cr:
        st.markdown('<div class="section-header">❌ 오답 많은 단어 TOP 5</div>', unsafe_allow_html=True)
        hard = sorted([(w,w["wrong"]) for w in words if w["wrong"]>0], key=lambda x:-x[1])
        if hard:
            for w, cnt in hard[:5]: st.markdown(f'<div class="word-card" style="border-left-color:#ef4444;"><span class="word-kanji">{w["kanji"]}</span><span style="float:right;font-size:1.2rem;font-weight:700;color:#ef4444;">오답 {cnt}회</span><div class="word-hira">{w["hiragana"]} · {w["meaning"]}</div></div>', unsafe_allow_html=True)
        else: st.info("오답 기록이 없습니다!")

    st.markdown('<div class="section-header">✍️ 따라쓰기 TOP 5</div>', unsafe_allow_html=True)
    tr_list = sorted([(w, w.get("trace_count",0)) for w in words if w.get("trace_count",0)>0], key=lambda x:-x[1])
    if tr_list:
        for w, cnt in tr_list[:5]: st.markdown(f'<div class="word-card" style="border-left-color:#6366f1;"><span class="word-kanji">{w["kanji"]}</span><span style="float:right;font-size:1.2rem;font-weight:700;color:#6366f1;">✍️ {cnt}회</span><div class="word-hira">{w["hiragana"]} · {w["meaning"]}</div></div>', unsafe_allow_html=True)
    else: st.info("따라쓰기 기록이 없습니다.")

# ═══════════════════════════════════════════
# ⚙️ 표기 설정
# ═══════════════════════════════════════════
elif menu == "⚙️ 표기 설정":
    st.markdown('<div class="section-header">⚙️ 표기 방식 설정</div>', unsafe_allow_html=True)
    st.markdown('<div style="background:white;border-radius:16px;padding:1.2rem 1.5rem;box-shadow:0 2px 12px rgba(114,9,183,0.08);margin-bottom:1.5rem;color:#555;">단어장·즐겨찾기에서 표시할 정보를 선택하세요. 사이드바 하단에서도 빠르게 변경 가능합니다.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 표시 항목 선택")
        sk = st.toggle("🈶 한자 표시",       value=st.session_state.show_kanji)
        sh = st.toggle("あ 히라가나 표시",   value=st.session_state.show_hiragana)
        sr = st.toggle("📝 로마자 표시",     value=st.session_state.show_romaji)
        sm = st.toggle("🔹 한국어 뜻 표시", value=st.session_state.show_meaning)
        if st.button("💾 설정 적용", use_container_width=True):
            st.session_state.show_kanji    = sk
            st.session_state.show_hiragana = sh
            st.session_state.show_romaji   = sr
            st.session_state.show_meaning  = sm
            st.success("✅ 설정이 저장되었습니다!"); st.rerun()
        st.markdown("---")
        st.markdown("#### 🎯 프리셋")
        p1, p2, p3 = st.columns(3)
        with p1:
            if st.button("📖 학습\n모드", use_container_width=True):
                st.session_state.show_kanji = st.session_state.show_hiragana = st.session_state.show_romaji = st.session_state.show_meaning = True; st.rerun()
        with p2:
            if st.button("🧪 테스트\n모드", use_container_width=True):
                st.session_state.show_kanji = st.session_state.show_hiragana = st.session_state.show_romaji = True
                st.session_state.show_meaning = False; st.rerun()
        with p3:
            if st.button("🔥 고급\n모드", use_container_width=True):
                st.session_state.show_kanji = True
                st.session_state.show_hiragana = st.session_state.show_romaji = st.session_state.show_meaning = False; st.rerun()
    with c2:
        st.markdown("#### 👁️ 미리보기")
        if st.session_state.words:
            st.markdown(render_word_card(st.session_state.words[0], sk, sh, sr, sm), unsafe_allow_html=True)
            st.caption("※ 단어장에서 보이는 모습 미리보기")
