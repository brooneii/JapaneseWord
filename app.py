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
# 기본 단어 데이터 (N5~N1 레벨 포함)
# ─────────────────────────────────────────
def _w(kanji, hiragana, romaji, meaning, category, level, favorite=False):
    return {"kanji":kanji,"hiragana":hiragana,"romaji":romaji,"meaning":meaning,
            "category":category,"level":level,"favorite":favorite,
            "correct":0,"wrong":0,"trace_count":0,"kanji_correct":0,"kanji_wrong":0}

DEFAULT_WORDS = [
    # ── N5 ──────────────────────────────────────────
    _w("食べる","たべる","taberu","먹다","동사","N5"),
    _w("飲む","のむ","nomu","마시다","동사","N5"),
    _w("見る","みる","miru","보다","동사","N5"),
    _w("行く","いく","iku","가다","동사","N5"),
    _w("来る","くる","kuru","오다","동사","N5"),
    _w("書く","かく","kaku","쓰다","동사","N5"),
    _w("読む","よむ","yomu","읽다","동사","N5"),
    _w("話す","はなす","hanasu","말하다","동사","N5"),
    _w("聞く","きく","kiku","듣다/묻다","동사","N5"),
    _w("買う","かう","kau","사다","동사","N5"),
    _w("学校","がっこう","gakkou","학교","명사","N5"),
    _w("電車","でんしゃ","densha","전철","명사","N5"),
    _w("友達","ともだち","tomodachi","친구","명사","N5"),
    _w("今日","きょう","kyou","오늘","명사","N5"),
    _w("昨日","きのう","kinou","어제","명사","N5"),
    _w("明日","あした","ashita","내일","명사","N5"),
    _w("空","そら","sora","하늘","명사","N5"),
    _w("海","うみ","umi","바다","명사","N5"),
    _w("山","やま","yama","산","명사","N5"),
    _w("花","はな","hana","꽃","명사","N5",favorite=True),
    _w("猫","ねこ","neko","고양이","명사","N5"),
    _w("犬","いぬ","inu","강아지","명사","N5"),
    _w("水","みず","mizu","물","명사","N5"),
    _w("火","ひ","hi","불","명사","N5"),
    _w("木","き","ki","나무","명사","N5"),
    _w("美しい","うつくしい","utsukushii","아름답다","형용사","N5"),
    _w("楽しい","たのしい","tanoshii","즐겁다","형용사","N5"),
    _w("難しい","むずかしい","muzukashii","어렵다","형용사","N5"),
    _w("嬉しい","うれしい","ureshii","기쁘다","형용사","N5"),
    _w("悲しい","かなしい","kanashii","슬프다","형용사","N5"),
    _w("暖かい","あたたかい","atatakai","따뜻하다","형용사","N5"),
    _w("寒い","さむい","samui","춥다","형용사","N5"),
    _w("暑い","あつい","atsui","덥다","형용사","N5"),
    _w("とても","とても","totemo","매우","부사","N5"),
    _w("少し","すこし","sukoshi","조금","부사","N5"),
    _w("もう","もう","mou","이미/벌써","부사","N5"),
    _w("まだ","まだ","mada","아직","부사","N5"),
    _w("いつも","いつも","itsumo","항상","부사","N5"),
    _w("一緒に","いっしょに","issho ni","함께","부사","N5"),
    _w("ゆっくり","ゆっくり","yukkuri","천천히","부사","N5"),
    # ── N4 ──────────────────────────────────────────
    _w("起きる","おきる","okiru","일어나다","동사","N4"),
    _w("寝る","ねる","neru","자다","동사","N4"),
    _w("着る","きる","kiru","입다","동사","N4"),
    _w("脱ぐ","ぬぐ","nugu","벗다","동사","N4"),
    _w("泳ぐ","およぐ","oyogu","수영하다","동사","N4"),
    _w("走る","はしる","hashiru","달리다","동사","N4"),
    _w("歩く","あるく","aruku","걷다","동사","N4"),
    _w("働く","はたらく","hataraku","일하다","동사","N4"),
    _w("使う","つかう","tsukau","사용하다","동사","N4"),
    _w("教える","おしえる","oshieru","가르치다","동사","N4"),
    _w("病院","びょういん","byouin","병원","명사","N4"),
    _w("駅","えき","eki","역","명사","N4"),
    _w("図書館","としょかん","toshokan","도서관","명사","N4"),
    _w("公園","こうえん","kouen","공원","명사","N4"),
    _w("会社","かいしゃ","kaisha","회사","명사","N4"),
    _w("旅行","りょこう","ryokou","여행","명사","N4"),
    _w("料理","りょうり","ryouri","요리","명사","N4"),
    _w("音楽","おんがく","ongaku","음악","명사","N4"),
    _w("映画","えいが","eiga","영화","명사","N4"),
    _w("運動","うんどう","undou","운동","명사","N4"),
    _w("便利","べんり","benri","편리하다","형용사","N4"),
    _w("親切","しんせつ","shinsetsu","친절하다","형용사","N4"),
    _w("丁寧","ていねい","teinei","정중하다","형용사","N4"),
    _w("大切","たいせつ","taisetsu","소중하다","형용사","N4"),
    _w("有名","ゆうめい","yuumei","유명하다","형용사","N4"),
    # ── N3 ──────────────────────────────────────────
    _w("決める","きめる","kimeru","결정하다","동사","N3"),
    _w("集める","あつめる","atsumeru","모으다","동사","N3"),
    _w("続ける","つづける","tsuzukeru","계속하다","동사","N3"),
    _w("比べる","くらべる","kuraberu","비교하다","동사","N3"),
    _w("変わる","かわる","kawaru","바뀌다","동사","N3"),
    _w("増える","ふえる","fueru","늘다","동사","N3"),
    _w("減る","へる","heru","줄다","동사","N3"),
    _w("経済","けいざい","keizai","경제","명사","N3"),
    _w("社会","しゃかい","shakai","사회","명사","N3"),
    _w("文化","ぶんか","bunka","문화","명사","N3"),
    _w("環境","かんきょう","kankyou","환경","명사","N3"),
    _w("機会","きかい","kikai","기회","명사","N3"),
    _w("関係","かんけい","kankei","관계","명사","N3"),
    _w("意見","いけん","iken","의견","명사","N3"),
    _w("問題","もんだい","mondai","문제","명사","N3"),
    _w("複雑","ふくざつ","fukuzatsu","복잡하다","형용사","N3"),
    _w("重要","じゅうよう","juuyou","중요하다","형용사","N3"),
    _w("必要","ひつよう","hitsuyou","필요하다","형용사","N3"),
    # ── N2 ──────────────────────────────────────────
    _w("把握する","はあくする","haaku suru","파악하다","동사","N2"),
    _w("検討する","けんとうする","kentou suru","검토하다","동사","N2"),
    _w("提案する","ていあんする","teian suru","제안하다","동사","N2"),
    _w("判断する","はんだんする","handan suru","판단하다","동사","N2"),
    _w("確認する","かくにんする","kakunin suru","확인하다","동사","N2"),
    _w("影響","えいきょう","eikyou","영향","명사","N2"),
    _w("状況","じょうきょう","joukyou","상황","명사","N2"),
    _w("結果","けっか","kekka","결과","명사","N2"),
    _w("原因","げんいん","genin","원인","명사","N2"),
    _w("対策","たいさく","taisaku","대책","명사","N2"),
    _w("方針","ほうしん","houshin","방침","명사","N2"),
    _w("観点","かんてん","kanten","관점","명사","N2"),
    _w("効率的","こうりつてき","kouritsu teki","효율적","형용사","N2"),
    _w("具体的","ぐたいてき","gutai teki","구체적","형용사","N2"),
    # ── N1 ──────────────────────────────────────────
    _w("醸し出す","かもしだす","kamoshidasu","자아내다","동사","N1"),
    _w("見据える","みすえる","misueru","직시하다","동사","N1"),
    _w("踏まえる","ふまえる","fumaeru","근거로 하다","동사","N1"),
    _w("培う","つちかう","tsuchikau","키우다/배양하다","동사","N1"),
    _w("葛藤","かっとう","kattou","갈등","명사","N1"),
    _w("矛盾","むじゅん","mujun","모순","명사","N1"),
    _w("概念","がいねん","gainen","개념","명사","N1"),
    _w("倫理","りんり","rinri","윤리","명사","N1"),
    _w("曖昧","あいまい","aimai","애매하다","형용사","N1"),
    _w("顕著","けんちょ","kencho","현저하다","형용사","N1"),
]

# ── 한자 외우기 데이터 (N5~N1) ──
KANJI_DATA = {
    "N5": [
        {"kanji":"日","onyomi":"ニチ・ジツ","kunyomi":"ひ・か","meaning":"날 일","strokes":4,"example":"日本(にほん) 일본"},
        {"kanji":"月","onyomi":"ゲツ・ガツ","kunyomi":"つき","meaning":"달 월","strokes":4,"example":"月曜日(げつようび) 월요일"},
        {"kanji":"火","onyomi":"カ","kunyomi":"ひ","meaning":"불 화","strokes":4,"example":"火曜日(かようび) 화요일"},
        {"kanji":"水","onyomi":"スイ","kunyomi":"みず","meaning":"물 수","strokes":4,"example":"水曜日(すいようび) 수요일"},
        {"kanji":"木","onyomi":"モク・ボク","kunyomi":"き","meaning":"나무 목","strokes":4,"example":"木曜日(もくようび) 목요일"},
        {"kanji":"金","onyomi":"キン・コン","kunyomi":"かね","meaning":"금/돈 금","strokes":8,"example":"金曜日(きんようび) 금요일"},
        {"kanji":"土","onyomi":"ド・ト","kunyomi":"つち","meaning":"흙 토","strokes":3,"example":"土曜日(どようび) 토요일"},
        {"kanji":"山","onyomi":"サン","kunyomi":"やま","meaning":"산 산","strokes":3,"example":"富士山(ふじさん) 후지산"},
        {"kanji":"川","onyomi":"セン","kunyomi":"かわ","meaning":"강 천","strokes":3,"example":"川(かわ) 강"},
        {"kanji":"田","onyomi":"デン","kunyomi":"た","meaning":"논 전","strokes":5,"example":"田中(たなか) 다나카"},
        {"kanji":"人","onyomi":"ジン・ニン","kunyomi":"ひと","meaning":"사람 인","strokes":2,"example":"人(ひと) 사람"},
        {"kanji":"口","onyomi":"コウ・ク","kunyomi":"くち","meaning":"입 구","strokes":3,"example":"入口(いりぐち) 입구"},
        {"kanji":"目","onyomi":"モク・ボク","kunyomi":"め","meaning":"눈 목","strokes":5,"example":"目(め) 눈"},
        {"kanji":"耳","onyomi":"ジ","kunyomi":"みみ","meaning":"귀 이","strokes":6,"example":"耳(みみ) 귀"},
        {"kanji":"手","onyomi":"シュ","kunyomi":"て","meaning":"손 수","strokes":4,"example":"手紙(てがみ) 편지"},
        {"kanji":"足","onyomi":"ソク","kunyomi":"あし","meaning":"발/다리 족","strokes":7,"example":"足(あし) 발"},
        {"kanji":"一","onyomi":"イチ・イツ","kunyomi":"ひと","meaning":"한 일","strokes":1,"example":"一番(いちばん) 1등"},
        {"kanji":"二","onyomi":"ニ","kunyomi":"ふた","meaning":"둘 이","strokes":2,"example":"二人(ふたり) 두 명"},
        {"kanji":"三","onyomi":"サン","kunyomi":"み・みつ","meaning":"셋 삼","strokes":3,"example":"三月(さんがつ) 3월"},
        {"kanji":"大","onyomi":"ダイ・タイ","kunyomi":"おお","meaning":"클 대","strokes":3,"example":"大学(だいがく) 대학"},
    ],
    "N4": [
        {"kanji":"安","onyomi":"アン","kunyomi":"やす","meaning":"편안할 안","strokes":6,"example":"安全(あんぜん) 안전"},
        {"kanji":"暗","onyomi":"アン","kunyomi":"くら","meaning":"어두울 암","strokes":13,"example":"暗い(くらい) 어둡다"},
        {"kanji":"医","onyomi":"イ","kunyomi":"","meaning":"의원 의","strokes":7,"example":"医者(いしゃ) 의사"},
        {"kanji":"運","onyomi":"ウン","kunyomi":"はこ","meaning":"운반할 운","strokes":12,"example":"運動(うんどう) 운동"},
        {"kanji":"映","onyomi":"エイ","kunyomi":"うつ","meaning":"비칠 영","strokes":9,"example":"映画(えいが) 영화"},
        {"kanji":"駅","onyomi":"エキ","kunyomi":"","meaning":"역 역","strokes":14,"example":"駅(えき) 역"},
        {"kanji":"音","onyomi":"オン・イン","kunyomi":"おと","meaning":"소리 음","strokes":9,"example":"音楽(おんがく) 음악"},
        {"kanji":"科","onyomi":"カ","kunyomi":"","meaning":"과목 과","strokes":9,"example":"科学(かがく) 과학"},
        {"kanji":"花","onyomi":"カ","kunyomi":"はな","meaning":"꽃 화","strokes":7,"example":"花(はな) 꽃"},
        {"kanji":"夏","onyomi":"カ・ゲ","kunyomi":"なつ","meaning":"여름 하","strokes":10,"example":"夏休み(なつやすみ) 여름방학"},
        {"kanji":"家","onyomi":"カ・ケ","kunyomi":"いえ","meaning":"집 가","strokes":10,"example":"家族(かぞく) 가족"},
        {"kanji":"画","onyomi":"ガ・カク","kunyomi":"え","meaning":"그림 화","strokes":8,"example":"映画(えいが) 영화"},
        {"kanji":"会","onyomi":"カイ・エ","kunyomi":"あ","meaning":"만날 회","strokes":6,"example":"会社(かいしゃ) 회사"},
        {"kanji":"海","onyomi":"カイ","kunyomi":"うみ","meaning":"바다 해","strokes":9,"example":"海(うみ) 바다"},
        {"kanji":"楽","onyomi":"ガク・ラク","kunyomi":"たの","meaning":"즐길 락","strokes":13,"example":"音楽(おんがく) 음악"},
    ],
    "N3": [
        {"kanji":"愛","onyomi":"アイ","kunyomi":"","meaning":"사랑 애","strokes":13,"example":"愛情(あいじょう) 애정"},
        {"kanji":"悪","onyomi":"アク・オ","kunyomi":"わる","meaning":"악할 악","strokes":11,"example":"悪い(わるい) 나쁘다"},
        {"kanji":"以","onyomi":"イ","kunyomi":"","meaning":"써 이","strokes":5,"example":"以上(いじょう) 이상"},
        {"kanji":"意","onyomi":"イ","kunyomi":"","meaning":"뜻 의","strokes":13,"example":"意味(いみ) 의미"},
        {"kanji":"員","onyomi":"イン","kunyomi":"","meaning":"인원 원","strokes":10,"example":"社員(しゃいん) 사원"},
        {"kanji":"引","onyomi":"イン","kunyomi":"ひ","meaning":"끌 인","strokes":4,"example":"引く(ひく) 당기다"},
        {"kanji":"飲","onyomi":"イン","kunyomi":"の","meaning":"마실 음","strokes":12,"example":"飲む(のむ) 마시다"},
        {"kanji":"運","onyomi":"ウン","kunyomi":"はこ","meaning":"운반할 운","strokes":12,"example":"運命(うんめい) 운명"},
        {"kanji":"営","onyomi":"エイ","kunyomi":"いとな","meaning":"경영할 영","strokes":12,"example":"営業(えいぎょう) 영업"},
        {"kanji":"衛","onyomi":"エイ","kunyomi":"まも","meaning":"지킬 위","strokes":16,"example":"衛星(えいせい) 위성"},
        {"kanji":"益","onyomi":"エキ・ヤク","kunyomi":"","meaning":"더할 익","strokes":10,"example":"利益(りえき) 이익"},
        {"kanji":"回","onyomi":"カイ","kunyomi":"まわ","meaning":"돌 회","strokes":6,"example":"回答(かいとう) 회답"},
    ],
    "N2": [
        {"kanji":"握","onyomi":"アク","kunyomi":"にぎ","meaning":"쥘 악","strokes":12,"example":"握手(あくしゅ) 악수"},
        {"kanji":"扱","onyomi":"","kunyomi":"あつか","meaning":"다룰 급","strokes":6,"example":"扱う(あつかう) 다루다"},
        {"kanji":"嵐","onyomi":"ラン","kunyomi":"あらし","meaning":"폭풍 람","strokes":12,"example":"嵐(あらし) 폭풍"},
        {"kanji":"慰","onyomi":"イ","kunyomi":"なぐさ","meaning":"위로할 위","strokes":15,"example":"慰める(なぐさめる) 위로하다"},
        {"kanji":"逸","onyomi":"イツ","kunyomi":"そ","meaning":"달아날 일","strokes":11,"example":"逸脱(いつだつ) 일탈"},
        {"kanji":"陰","onyomi":"イン","kunyomi":"かげ","meaning":"그늘 음","strokes":11,"example":"陰(かげ) 그늘"},
        {"kanji":"影","onyomi":"エイ","kunyomi":"かげ","meaning":"그림자 영","strokes":15,"example":"影響(えいきょう) 영향"},
        {"kanji":"鋭","onyomi":"エイ","kunyomi":"するど","meaning":"날카로울 예","strokes":15,"example":"鋭い(するどい) 날카롭다"},
        {"kanji":"縁","onyomi":"エン","kunyomi":"ふち","meaning":"인연 연","strokes":15,"example":"縁(えん) 인연"},
        {"kanji":"汚","onyomi":"オ","kunyomi":"きたな・よご","meaning":"더러울 오","strokes":6,"example":"汚い(きたない) 더럽다"},
    ],
    "N1": [
        {"kanji":"葛","onyomi":"カツ","kunyomi":"くず","meaning":"칡 갈","strokes":12,"example":"葛藤(かっとう) 갈등"},
        {"kanji":"矛","onyomi":"ム","kunyomi":"ほこ","meaning":"창 모","strokes":5,"example":"矛盾(むじゅん) 모순"},
        {"kanji":"概","onyomi":"ガイ","kunyomi":"おおむ","meaning":"대개 개","strokes":14,"example":"概念(がいねん) 개념"},
        {"kanji":"曖","onyomi":"アイ","kunyomi":"","meaning":"희미할 애","strokes":17,"example":"曖昧(あいまい) 애매"},
        {"kanji":"昧","onyomi":"マイ","kunyomi":"","meaning":"어두울 매","strokes":9,"example":"曖昧(あいまい) 애매"},
        {"kanji":"顕","onyomi":"ケン","kunyomi":"あらわ","meaning":"나타날 현","strokes":18,"example":"顕著(けんちょ) 현저"},
        {"kanji":"醸","onyomi":"ジョウ","kunyomi":"かも","meaning":"빚을 양","strokes":20,"example":"醸造(じょうぞう) 양조"},
        {"kanji":"培","onyomi":"バイ","kunyomi":"つちか","meaning":"북돋울 배","strokes":11,"example":"培養(ばいよう) 배양"},
        {"kanji":"倫","onyomi":"リン","kunyomi":"","meaning":"인륜 륜","strokes":10,"example":"倫理(りんり) 윤리"},
        {"kanji":"擁","onyomi":"ヨウ","kunyomi":"","meaning":"안을 옹","strokes":17,"example":"擁護(ようご) 옹호"},
    ],
}

LEVELS = ["전체", "N5", "N4", "N3", "N2", "N1"]
CATEGORIES = ["전체", "동사", "명사", "형용사", "부사", "기타"]

CATEGORIES = ["전체", "동사", "명사", "형용사", "부사", "기타"]

# ─────────────────────────────────────────
# 세션 상태 초기화
# ─────────────────────────────────────────
def init_state():
    defaults = {
        "words": [dict(w) for w in DEFAULT_WORDS],
        "quiz_index": 0, "quiz_words": [], "quiz_answered": False,
        "quiz_result": None, "quiz_score": {"correct": 0, "wrong": 0},
        "quiz_mode": "not_started", "quiz_type": "kanji→뜻",
        "show_kanji": True, "show_hiragana": True,
        "show_romaji": True, "show_meaning": True,
        "trace_idx": 0, "trace_words": [], "trace_mode": "not_started",
        "trace_user_input": "", "trace_checked": False,
        "trace_check_result": None, "trace_show": "한국어 뜻만",
        # 한자 외우기
        "kj_level": "N5", "kj_idx": 0, "kj_list": [],
        "kj_mode": "not_started", "kj_flipped": False,
        "kj_score": {"correct": 0, "wrong": 0},
        # 레벨 필터
        "word_level_filter": "전체",
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
    if w.get("level"): tags += f' <span class="word-tag" style="background:linear-gradient(135deg,#e0f2fe,#bae6fd);color:#0369a1;">{w["level"]}</span>'
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
    menu = st.radio("메뉴", ["📖 단어장", "➕ 단어 추가", "❤️ 즐겨찾기", "🧠 퀴즈", "✍️ 따라쓰기", "🀄 한자 외우기", "📊 통계", "⚙️ 표기 설정"], label_visibility="collapsed")
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
    col_s, col_c, col_lv = st.columns([3, 1, 1])
    with col_s: search = st.text_input("🔍 검색 (한자·히라가나·뜻)", placeholder="예: 食べる / たべる / 먹다")
    with col_c: cat_filter = st.selectbox("카테고리", CATEGORIES)
    with col_lv: lv_filter = st.selectbox("레벨", LEVELS)

    words = st.session_state.words
    if search:    words = [w for w in words if search in w["kanji"] or search in w["hiragana"] or search in w["meaning"]]
    if cat_filter != "전체": words = [w for w in words if w["category"] == cat_filter]
    if lv_filter != "전체":  words = [w for w in words if w.get("level") == lv_filter]

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
        quiz_level = st.selectbox("레벨 필터", LEVELS, key="quiz_lv")
        pool = [w for w in st.session_state.words if src[quiz_source](w) and (quiz_level=="전체" or w.get("level")==quiz_level)]
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
    import streamlit.components.v1 as components

    st.markdown('<div class="section-header">✍️ 따라쓰기 연습</div>', unsafe_allow_html=True)

    for _k, _v in [("hint_level", 0), ("answer_shown", False)]:
        if _k not in st.session_state:
            st.session_state[_k] = _v

    # ── 시작 전 ──
    if st.session_state.trace_mode == "not_started":
        st.markdown('<div style="background:white;border-radius:16px;padding:1.2rem 1.5rem;box-shadow:0 2px 12px rgba(114,9,183,0.08);margin-bottom:1rem;color:#555;">✏️ 한국어 뜻을 보고 일본어를 캔버스에 직접 써보세요!<br>힌트를 단계별로 확인하고, 다 쓴 후 <b>정답 확인</b> 버튼으로 답을 맞춰보세요 🌸</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: tr_src = st.selectbox("연습할 단어 범위", ["전체 단어","즐겨찾기만","동사만","명사만","형용사만","오답 단어"])
        with c2: tr_cnt = st.slider("연습할 단어 수", 3, min(20, len(st.session_state.words)), 5)
        src_map = {
            "전체 단어":  lambda w: True,
            "즐겨찾기만": lambda w: w["favorite"],
            "동사만":     lambda w: w["category"] == "동사",
            "명사만":     lambda w: w["category"] == "명사",
            "형용사만":   lambda w: w["category"] == "형용사",
            "오답 단어":  lambda w: w["wrong"] > 0,
        }
        tr_lv = st.selectbox("레벨 필터", LEVELS, key="tr_lv")
        pool = [w for w in st.session_state.words if src_map[tr_src](w) and (tr_lv=="전체" or w.get("level")==tr_lv)]
        if st.button("✍️ 따라쓰기 시작!", use_container_width=True):
            if not pool:
                st.warning("해당 범위에 단어가 없습니다.")
            else:
                shuffled = pool.copy(); random.shuffle(shuffled)
                st.session_state.trace_words        = shuffled[:tr_cnt]
                st.session_state.trace_idx          = 0
                st.session_state.trace_mode         = "in_progress"
                st.session_state.trace_checked      = False
                st.session_state.trace_check_result = None
                st.session_state.hint_level         = 0
                st.session_state.answer_shown       = False
                st.rerun()

    # ── 진행 중 ──
    elif st.session_state.trace_mode == "in_progress":
        t_idx     = st.session_state.trace_idx
        t_words   = st.session_state.trace_words
        total_t   = len(t_words)
        current   = t_words[t_idx]
        hl        = st.session_state.hint_level
        ans_shown = st.session_state.answer_shown

        st.progress(t_idx / total_t, text=f"✍️ {t_idx+1} / {total_t} 번째 단어")

        # ghost 글자: hl=0,1→빈칸  hl=2→히라가나반투명  hl=3→한자반투명
        if hl <= 1:
            ghost_char, ghost_alpha = "", "0.0"
        elif hl == 2:
            ghost_char, ghost_alpha = current["hiragana"], "0.15"
        else:
            ghost_char, ghost_alpha = current["kanji"], "0.18"
        ghost_color = f"rgba(181,23,158,{ghost_alpha})"

        # ── 캔버스 HTML ──
        canvas_html = (
            "<!DOCTYPE html><html><head>"
            "<meta name='viewport' content='width=device-width,initial-scale=1.0,user-scalable=no'>"
            "<link href='https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@700&family=Noto+Sans+KR:wght@700&display=swap' rel='stylesheet'>"
            "<style>"
            "*{box-sizing:border-box;margin:0;padding:0;}"
            "body{background:transparent;-webkit-tap-highlight-color:transparent;}"
            ".wrap{background:white;border-radius:20px;padding:1rem;box-shadow:0 4px 24px rgba(114,9,183,0.12);max-width:540px;margin:0 auto;}"
            ".meaning{text-align:center;font-family:'Noto Sans KR',sans-serif;font-size:1.5rem;font-weight:700;color:#b5179e;margin-bottom:0.7rem;}"
            ".cw{position:relative;width:100%;aspect-ratio:4/3;border:2.5px dashed rgba(181,23,158,0.3);border-radius:14px;overflow:hidden;background:#f9f9f9;touch-action:none;user-select:none;}"
            f".ghost{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:'Noto Serif JP',serif;font-size:clamp(4rem,20vw,9rem);font-weight:700;color:{ghost_color};pointer-events:none;user-select:none;letter-spacing:0.06em;}}"
            ".grid{position:absolute;inset:0;pointer-events:none;opacity:0.07;}"
            "canvas{position:absolute;inset:0;width:100%;height:100%;cursor:crosshair;touch-action:none;}"
            ".toolbar{display:flex;gap:7px;margin-top:0.7rem;}"
            ".tbtn{flex:1;padding:0.65rem 0.2rem;border:none;border-radius:10px;font-size:0.85rem;font-weight:700;cursor:pointer;transition:0.15s;-webkit-tap-highlight-color:transparent;}"
            ".tbtn:active{transform:scale(0.95);}"
            ".pen{background:#1a0a2e;color:white;}.ers{background:#fde8d8;color:#b55017;}.clr{background:#f0e6ff;color:#7209b7;}"
            ".tbtn.on{outline:2.5px solid #b5179e;}"
            ".srow{display:flex;gap:8px;margin-top:0.5rem;align-items:center;}"
            ".sdot{width:30px;height:30px;border-radius:50%;border:2px solid #ddd;cursor:pointer;display:flex;align-items:center;justify-content:center;-webkit-tap-highlight-color:transparent;}"
            ".sdot.on{border-color:#b5179e;background:#fdf0ff;}"
            ".cdot{width:22px;height:22px;border-radius:50%;border:2.5px solid transparent;cursor:pointer;-webkit-tap-highlight-color:transparent;}"
            ".cdot.on{border-color:#b5179e;box-shadow:0 0 0 2px #f0e;}"
            ".slbl{font-size:0.72rem;color:#aaa;margin-left:auto;}"
            "</style></head><body>"
            "<div class='wrap'>"
            f"<div class='meaning'>🔹 {current['meaning']}</div>"
            "<div class='cw' id='cw'>"
            "<svg class='grid' viewBox='0 0 100 100' preserveAspectRatio='none'>"
            "<line x1='50' y1='0' x2='50' y2='100' stroke='#777' stroke-width='0.8'/>"
            "<line x1='0' y1='50' x2='100' y2='50' stroke='#777' stroke-width='0.8'/>"
            "<line x1='0' y1='0' x2='100' y2='100' stroke='#777' stroke-width='0.4'/>"
            "<line x1='100' y1='0' x2='0' y2='100' stroke='#777' stroke-width='0.4'/>"
            "</svg>"
            f"<div class='ghost' id='ghost'>{ghost_char}</div>"
            "<canvas id='c'></canvas>"
            "</div>"
            "<div class='toolbar'>"
            "<button class='tbtn pen on' id='bPen' onclick=\"setTool('pen')\">🖊️ 펜</button>"
            "<button class='tbtn ers' id='bErs' onclick=\"setTool('eraser')\">🧹 지우개</button>"
            "<button class='tbtn clr' onclick='clearAll()'>🗑️ 전체삭제</button>"
            "</div>"
            "<div class='srow'>"
            "<div class='sdot on' id='s1' onclick='setSz(4,this)'><div style='width:5px;height:5px;border-radius:50%;background:#333;'></div></div>"
            "<div class='sdot' id='s2' onclick='setSz(9,this)'><div style='width:10px;height:10px;border-radius:50%;background:#333;'></div></div>"
            "<div class='sdot' id='s3' onclick='setSz(16,this)'><div style='width:17px;height:17px;border-radius:50%;background:#333;'></div></div>"
            "<div class='cdot on' id='c1' onclick=\"setClr('#1a0a2e',this)\" style='background:#1a0a2e;margin-left:10px;'></div>"
            "<div class='cdot' id='c2' onclick=\"setClr('#b5179e',this)\" style='background:#b5179e;'></div>"
            "<div class='cdot' id='c3' onclick=\"setClr('#3a0ca3',this)\" style='background:#3a0ca3;'></div>"
            "<span class='slbl'>굵기 · 색상</span>"
            "</div></div>"
            "<script>"
            "const cv=document.getElementById('c'),ctx=cv.getContext('2d'),cw=document.getElementById('cw');"
            "let drawing=false,tool='pen',sz=4,clr='#1a0a2e';"
            "function resize(){const r=cv.getBoundingClientRect();cv.width=r.width;cv.height=r.height;}"
            "resize();new ResizeObserver(resize).observe(cw);"
            "function pt(e){const r=cv.getBoundingClientRect(),s=e.touches?e.touches[0]:e;return[s.clientX-r.left,s.clientY-r.top];}"
            "function down(e){e.preventDefault();drawing=true;const[x,y]=pt(e);ctx.beginPath();ctx.moveTo(x,y);}"
            "function move(e){if(!drawing)return;e.preventDefault();const[x,y]=pt(e);ctx.lineWidth=tool==='eraser'?sz*5:sz;ctx.lineCap='round';ctx.lineJoin='round';ctx.strokeStyle=tool==='eraser'?'#f9f9f9':clr;ctx.globalCompositeOperation=tool==='eraser'?'destination-out':'source-over';ctx.lineTo(x,y);ctx.stroke();ctx.beginPath();ctx.moveTo(x,y);}"
            "function up(){drawing=false;ctx.beginPath();}"
            "cv.addEventListener('mousedown',down,{passive:false});"
            "cv.addEventListener('mousemove',move,{passive:false});"
            "cv.addEventListener('mouseup',up);cv.addEventListener('mouseleave',up);"
            "cv.addEventListener('touchstart',down,{passive:false});"
            "cv.addEventListener('touchmove',move,{passive:false});"
            "cv.addEventListener('touchend',up);"
            "function clearAll(){ctx.clearRect(0,0,cv.width,cv.height);}"
            "function setTool(t){tool=t;document.getElementById('bPen').classList.toggle('on',t==='pen');document.getElementById('bErs').classList.toggle('on',t==='eraser');}"
            "function setSz(s,el){sz=s;document.querySelectorAll('#s1,#s2,#s3').forEach(d=>d.classList.remove('on'));el.classList.add('on');}"
            "function setClr(c,el){clr=c;document.querySelectorAll('#c1,#c2,#c3').forEach(d=>d.classList.remove('on'));el.classList.add('on');if(tool==='eraser')setTool('pen');}"
            "</script></body></html>"
        )

        components.html(canvas_html, height=420, scrolling=False)

        # ── 힌트 3단계 ──
        st.markdown("---")
        st.markdown("**💡 힌트** (모르면 단계별로 확인하세요)")

        def romaji_to_kr(romaji):
            tbl = {
                "tchi":"찌","chi":"치","tsu":"츠","shi":"시","sha":"샤","shu":"슈","sho":"쇼",
                "cha":"차","chu":"추","cho":"초","kya":"캬","kyu":"큐","kyo":"쿄",
                "gya":"갸","gyu":"규","gyo":"교","nya":"냐","nyu":"뉴","nyo":"뇨",
                "hya":"햐","hyu":"휴","hyo":"효","mya":"먀","myu":"뮤","myo":"묘",
                "rya":"랴","ryu":"류","ryo":"료","bya":"뱌","byu":"뷰","byo":"뵤",
                "pya":"퍄","pyu":"퓨","pyo":"표","ka":"카","ki":"키","ku":"쿠","ke":"케","ko":"코",
                "sa":"사","su":"스","se":"세","so":"소","ta":"타","te":"테","to":"토",
                "na":"나","ni":"니","nu":"누","ne":"네","no":"노",
                "ha":"하","hi":"히","fu":"후","he":"헤","ho":"호",
                "ma":"마","mi":"미","mu":"무","me":"메","mo":"모",
                "ya":"야","yu":"유","yo":"요","ra":"라","ri":"리","ru":"루","re":"레","ro":"로",
                "wa":"와","wo":"오","ga":"가","gi":"기","gu":"구","ge":"게","go":"고",
                "za":"자","zu":"즈","ze":"제","zo":"조","da":"다","de":"데","do":"도",
                "ba":"바","bi":"비","bu":"부","be":"베","bo":"보","pa":"파","pi":"피",
                "pu":"푸","pe":"페","po":"포","a":"아","i":"이","u":"우","e":"에","o":"오","n":"ㄴ",
            }
            r = romaji.lower().replace(" ", "").replace("-", "")
            res = ""; i = 0
            while i < len(r):
                matched = False
                for ln in [4, 3, 2, 1]:
                    chunk = r[i:i+ln]
                    if chunk in tbl:
                        res += tbl[chunk]; i += ln; matched = True; break
                if not matched:
                    res += r[i]; i += 1
            return res

        h1, h2, h3 = st.columns(3)
        with h1:
            if hl == 0:
                if st.button("💡 힌트1: 한글발음", use_container_width=True, key=f"h1_{t_idx}"):
                    st.session_state.hint_level = 1; st.rerun()
            else:
                kr = romaji_to_kr(current["romaji"])
                st.markdown(f'<div style="background:#fff7e6;border:2px solid #f59e0b;border-radius:10px;padding:0.55rem;text-align:center;font-size:1.05rem;font-weight:700;color:#92400e;">🔊 {kr}</div>', unsafe_allow_html=True)
        with h2:
            if hl <= 1:
                if st.button("💡 힌트2: 히라가나", use_container_width=True, key=f"h2_{t_idx}", disabled=(hl < 1)):
                    st.session_state.hint_level = 2; st.rerun()
            else:
                st.markdown(f'<div style="background:#f0e6ff;border:2px solid #b5179e;border-radius:10px;padding:0.55rem;text-align:center;font-size:1.05rem;font-weight:700;color:#7209b7;">あ {current["hiragana"]}</div>', unsafe_allow_html=True)
        with h3:
            if hl <= 2:
                if st.button("💡 힌트3: 한자보기", use_container_width=True, key=f"h3_{t_idx}", disabled=(hl < 2)):
                    st.session_state.hint_level = 3; st.rerun()
            else:
                st.markdown(f'<div style="background:#ede9fe;border:2px solid #3a0ca3;border-radius:10px;padding:0.55rem;text-align:center;font-size:1.05rem;font-weight:700;color:#3a0ca3;">字 {current["kanji"]}</div>', unsafe_allow_html=True)

        # ── 정답 확인 ──
        st.markdown("---")
        if not ans_shown:
            ca, cb = st.columns(2)
            with ca:
                if st.button("✅ 정답 확인", use_container_width=True, key=f"ans_{t_idx}"):
                    st.session_state.answer_shown = True
                    ri = next((j for j,w in enumerate(st.session_state.words) if w["kanji"]==current["kanji"]), None)
                    if ri is not None:
                        st.session_state.words[ri]["trace_count"] = st.session_state.words[ri].get("trace_count",0)+1
                    st.rerun()
            with cb:
                if st.button("⏭️ 건너뛰기", use_container_width=True, key=f"tsk_{t_idx}"):
                    if t_idx + 1 < total_t:
                        st.session_state.trace_idx += 1
                        st.session_state.hint_level = 0
                        st.session_state.answer_shown = False
                    else:
                        st.session_state.trace_mode = "finished"
                    st.rerun()
        else:
            # 정답 카드
            st.markdown(
                f'<div style="background:white;border-radius:18px;padding:1.4rem 1.8rem;'
                f'box-shadow:0 4px 20px rgba(114,9,183,0.13);border:2px solid rgba(181,23,158,0.2);'
                f'text-align:center;margin-bottom:0.8rem;">'
                f'<div style="font-size:0.85rem;color:#aaa;margin-bottom:0.3rem;">✅ 정답</div>'
                f'<div style="font-family:Noto Serif JP,serif;font-size:2.8rem;font-weight:700;color:#1a0a2e;">{current["kanji"]}</div>'
                f'<div style="font-size:1.1rem;color:#b5179e;font-weight:600;margin-top:0.3rem;">{current["hiragana"]}</div>'
                f'<div style="font-size:0.9rem;color:#aaa;font-style:italic;">{current["romaji"]}</div>'
                f'<div style="font-size:1rem;color:#444;margin-top:0.5rem;font-weight:500;">🔹 {current["meaning"]}</div>'
                f'<div style="margin-top:0.8rem;">'
                f'<a href="https://jisho.org/search/{current["kanji"]}%20%23kanji" target="_blank" '
                f'style="color:#7209b7;font-size:0.82rem;text-decoration:none;">📖 필획 순서 보기 (jisho.org) →</a>'
                f'</div></div>',
                unsafe_allow_html=True
            )
            st.markdown("**내 손글씨와 비교해보세요!**")
            ev1, ev2, ev3 = st.columns(3)
            def next_word():
                if t_idx + 1 < total_t:
                    st.session_state.trace_idx += 1
                    st.session_state.hint_level = 0
                    st.session_state.answer_shown = False
                else:
                    st.session_state.trace_mode = "finished"
            with ev1:
                if st.button("😊 잘 썼어요", use_container_width=True, key=f"ev_ok_{t_idx}"):
                    ri = next((j for j,w in enumerate(st.session_state.words) if w["kanji"]==current["kanji"]), None)
                    if ri is not None: st.session_state.words[ri]["correct"] += 1
                    next_word(); st.rerun()
            with ev2:
                if st.button("😅 비슷해요", use_container_width=True, key=f"ev_so_{t_idx}"):
                    next_word(); st.rerun()
            with ev3:
                if st.button("😣 틀렸어요", use_container_width=True, key=f"ev_ng_{t_idx}"):
                    ri = next((j for j,w in enumerate(st.session_state.words) if w["kanji"]==current["kanji"]), None)
                    if ri is not None: st.session_state.words[ri]["wrong"] += 1
                    next_word(); st.rerun()

    # ── 완료 ──
    elif st.session_state.trace_mode == "finished":
        total_trace = sum(w.get("trace_count", 0) for w in st.session_state.words)
        st.markdown(
            f'<div class="quiz-card"><div style="font-size:4rem;">✍️</div>'
            f'<div style="font-family:Noto Serif JP,serif;font-size:2rem;font-weight:700;color:#1a0a2e;margin:1rem 0;">따라쓰기 완료!</div>'
            f'<div style="font-size:1.2rem;color:#7209b7;font-weight:600;">오늘 {len(st.session_state.trace_words)}개 단어 연습 완료</div>'
            f'<div style="color:#888;margin-top:0.5rem;">누적 따라쓰기 {total_trace}회</div></div>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="section-header">이번 연습 단어</div>', unsafe_allow_html=True)
        for w in st.session_state.trace_words:
            st.markdown(
                f'<div class="word-card" style="border-left-color:#6366f1;">'
                f'<span class="word-kanji">{w["kanji"]}</span>'
                f'<div class="word-hira">{w["hiragana"]} · {w["romaji"]}</div>'
                f'<div class="word-meaning">🔹 {w["meaning"]}</div>'
                f'<span class="word-tag">✍️ {w.get("trace_count",0)}회</span></div>',
                unsafe_allow_html=True
            )
        if st.button("🔄 다시 따라쓰기", use_container_width=True):
            st.session_state.trace_mode   = "not_started"
            st.session_state.hint_level   = 0
            st.session_state.answer_shown = False
            st.rerun()
# ═══════════════════════════════════════════
# 🀄 한자 외우기
# ═══════════════════════════════════════════
elif menu == "🀄 한자 외우기":
    import streamlit.components.v1 as components_kj

    st.markdown('<div class="section-header">🀄 한자 외우기</div>', unsafe_allow_html=True)

    # ── 레벨 선택 탭 ──
    lv_tabs = st.tabs(["N5", "N4", "N3", "N2", "N1"])
    level_names = ["N5", "N4", "N3", "N2", "N1"]

    # 현재 선택 레벨 (탭 인덱스 → 레벨명)
    if "kj_tab" not in st.session_state:
        st.session_state.kj_tab = 0

    for ti, (tab, lvname) in enumerate(zip(lv_tabs, level_names)):
        with tab:
            kanji_list = KANJI_DATA.get(lvname, [])
            if not kanji_list:
                st.info("데이터 준비 중입니다.")
                continue

            st.markdown(f'<div style="color:#9b6fa0;font-size:0.85rem;margin-bottom:1rem;">총 {len(kanji_list)}자 · 카드를 탭/클릭하면 뒤집힙니다</div>', unsafe_allow_html=True)

            # ── 모드 선택 ──
            kj_mode_key = f"kj_mode_{lvname}"
            kj_idx_key  = f"kj_idx_{lvname}"
            kj_ok_key   = f"kj_ok_{lvname}"
            kj_ng_key   = f"kj_ng_{lvname}"
            kj_order_key= f"kj_order_{lvname}"

            for dk, dv in [(kj_mode_key,"browse"),(kj_idx_key,0),(kj_ok_key,0),(kj_ng_key,0),(kj_order_key,None)]:
                if dk not in st.session_state:
                    st.session_state[dk] = dv
            if st.session_state[kj_order_key] is None:
                st.session_state[kj_order_key] = list(range(len(kanji_list)))

            mode = st.session_state[kj_mode_key]

            m1, m2, m3 = st.columns(3)
            with m1:
                if st.button("📋 목록 보기", use_container_width=True, key=f"mbrowse_{lvname}",
                             type="primary" if mode=="browse" else "secondary"):
                    st.session_state[kj_mode_key] = "browse"; st.rerun()
            with m2:
                if st.button("🃏 플래시카드", use_container_width=True, key=f"mcard_{lvname}",
                             type="primary" if mode=="card" else "secondary"):
                    order = list(range(len(kanji_list))); random.shuffle(order)
                    st.session_state[kj_order_key] = order
                    st.session_state[kj_idx_key]   = 0
                    st.session_state[kj_ok_key]    = 0
                    st.session_state[kj_ng_key]    = 0
                    st.session_state[kj_mode_key]  = "card"; st.rerun()
            with m3:
                if st.button("🧪 퀴즈", use_container_width=True, key=f"mqz_{lvname}",
                             type="primary" if mode=="quiz" else "secondary"):
                    order = list(range(len(kanji_list))); random.shuffle(order)
                    st.session_state[kj_order_key]      = order
                    st.session_state[kj_idx_key]        = 0
                    st.session_state[kj_ok_key]         = 0
                    st.session_state[kj_ng_key]         = 0
                    st.session_state[f"kj_qans_{lvname}"] = None
                    st.session_state[f"kj_qshow_{lvname}"] = False
                    st.session_state[kj_mode_key]       = "quiz"; st.rerun()

            st.markdown("---")

            # ═══ 목록 보기 ═══
            if mode == "browse":
                cols_per_row = 4
                rows = [kanji_list[i:i+cols_per_row] for i in range(0, len(kanji_list), cols_per_row)]
                for row in rows:
                    cols = st.columns(cols_per_row)
                    for ci, kdata in enumerate(row):
                        with cols[ci]:
                            st.markdown(
                                f'<div style="background:white;border-radius:14px;padding:1rem 0.5rem;'
                                f'text-align:center;box-shadow:0 2px 12px rgba(114,9,183,0.08);'
                                f'border-top:3px solid #b5179e;margin-bottom:0.5rem;">' 
                                f'<div style="font-family:Noto Serif JP,serif;font-size:2.2rem;font-weight:700;color:#1a0a2e;">{kdata["kanji"]}</div>'
                                f'<div style="font-size:0.75rem;color:#b5179e;margin:0.2rem 0;">{kdata["onyomi"]} / {kdata["kunyomi"]}</div>'
                                f'<div style="font-size:0.8rem;font-weight:600;color:#444;">{kdata["meaning"]}</div>'
                                f'<div style="font-size:0.7rem;color:#aaa;margin-top:0.3rem;">{kdata["strokes"]}획</div>'
                                f'<div style="font-size:0.7rem;color:#777;margin-top:0.3rem;font-style:italic;">{kdata["example"]}</div>'
                                f'</div>',
                                unsafe_allow_html=True
                            )

            # ═══ 플래시카드 ═══
            elif mode == "card":
                order   = st.session_state[kj_order_key]
                idx     = st.session_state[kj_idx_key]
                ok_cnt  = st.session_state[kj_ok_key]
                ng_cnt  = st.session_state[kj_ng_key]
                total_c = len(order)
                flip_key = f"kj_flip_{lvname}_{idx}"
                if flip_key not in st.session_state:
                    st.session_state[flip_key] = False
                flipped = st.session_state[flip_key]

                if idx >= total_c:
                    # 완료
                    pct = round(ok_cnt/(ok_cnt+ng_cnt)*100) if (ok_cnt+ng_cnt)>0 else 0
                    st.markdown(
                        f'<div class="quiz-card"><div style="font-size:3.5rem;">🀄</div>'
                        f'<div style="font-family:Noto Serif JP,serif;font-size:1.8rem;font-weight:700;color:#1a0a2e;margin:0.8rem 0;">학습 완료!</div>'
                        f'<div style="font-size:2.5rem;font-weight:700;background:linear-gradient(135deg,#b5179e,#7209b7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{pct}%</div>'
                        f'<div style="color:#888;">✅ {ok_cnt}개 알았어요 / ❌ {ng_cnt}개 몰랐어요</div></div>',
                        unsafe_allow_html=True
                    )
                    if st.button("🔄 다시 학습", use_container_width=True, key=f"kj_restart_{lvname}"):
                        order2 = list(range(len(kanji_list))); random.shuffle(order2)
                        st.session_state[kj_order_key] = order2
                        st.session_state[kj_idx_key]   = 0
                        st.session_state[kj_ok_key]    = 0
                        st.session_state[kj_ng_key]    = 0
                        st.rerun()
                else:
                    kdata = kanji_list[order[idx]]
                    st.progress(idx / total_c, text=f"🀄 {idx+1} / {total_c}  ·  ✅{ok_cnt}  ❌{ng_cnt}")

                    # 플래시카드 HTML
                    front_html = (
                        f'<div style="font-family:Noto Serif JP,serif;font-size:5rem;font-weight:700;color:#1a0a2e;">{kdata["kanji"]}</div>'
                        f'<div style="color:#b5179e;margin-top:0.5rem;font-size:0.9rem;">{lvname} · {kdata["strokes"]}획</div>'
                        f'<div style="color:#aaa;font-size:0.85rem;margin-top:0.3rem;">탭하면 뒷면 확인</div>'
                    )
                    back_html  = (
                        f'<div style="font-family:Noto Serif JP,serif;font-size:3.5rem;font-weight:700;color:#1a0a2e;">{kdata["kanji"]}</div>'
                        f'<div style="font-size:1rem;font-weight:700;color:#b5179e;margin-top:0.4rem;">{kdata["meaning"]}</div>'
                        f'<div style="font-size:0.85rem;color:#555;margin-top:0.3rem;">음독: {kdata["onyomi"]}</div>'
                        f'<div style="font-size:0.85rem;color:#555;">훈독: {kdata["kunyomi"]}</div>'
                        f'<div style="font-size:0.78rem;color:#888;margin-top:0.4rem;font-style:italic;">{kdata["example"]}</div>'
                    )
                    card_content = back_html if flipped else front_html
                    bg = "#fff7fb" if flipped else "white"
                    border = "#b5179e" if flipped else "#e0e0e0"
                    jisho_btn = f'<div style="margin-top:0.8rem;"><a href="https://jisho.org/search/{kdata["kanji"]}%20%23kanji" target="_blank" style="color:#7209b7;font-size:0.8rem;text-decoration:none;">📖 필획 순서 보기 →</a></div>' if flipped else ""

                    st.markdown(
                        f'<div onclick="" style="background:{bg};border:2px solid {border};border-radius:20px;'
                        f'padding:2rem;text-align:center;box-shadow:0 6px 24px rgba(114,9,183,0.1);'
                        f'min-height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;'
                        f'cursor:pointer;transition:all 0.3s;">{card_content}{jisho_btn}</div>',
                        unsafe_allow_html=True
                    )

                    if not flipped:
                        if st.button("🔄 뒤집기", use_container_width=True, key=f"kj_flip_btn_{lvname}_{idx}"):
                            st.session_state[flip_key] = True; st.rerun()
                    else:
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("✅ 알았어요", use_container_width=True, key=f"kj_ok_btn_{lvname}_{idx}"):
                                st.session_state[kj_ok_key]    += 1
                                st.session_state[kj_idx_key]   += 1
                                st.session_state[flip_key]      = False; st.rerun()
                        with c2:
                            if st.button("❌ 몰랐어요", use_container_width=True, key=f"kj_ng_btn_{lvname}_{idx}"):
                                st.session_state[kj_ng_key]    += 1
                                st.session_state[kj_idx_key]   += 1
                                st.session_state[flip_key]      = False; st.rerun()

            # ═══ 퀴즈 ═══
            elif mode == "quiz":
                order    = st.session_state[kj_order_key]
                idx      = st.session_state[kj_idx_key]
                ok_cnt   = st.session_state[kj_ok_key]
                ng_cnt   = st.session_state[kj_ng_key]
                total_c  = len(order)
                qans_key = f"kj_qans_{lvname}"
                qshow_key= f"kj_qshow_{lvname}"
                if qans_key  not in st.session_state: st.session_state[qans_key]  = None
                if qshow_key not in st.session_state: st.session_state[qshow_key] = False

                if idx >= total_c:
                    pct = round(ok_cnt/(ok_cnt+ng_cnt)*100) if (ok_cnt+ng_cnt)>0 else 0
                    st.markdown(
                        f'<div class="quiz-card"><div style="font-size:3.5rem;">🎉</div>'
                        f'<div style="font-family:Noto Serif JP,serif;font-size:1.8rem;font-weight:700;color:#1a0a2e;margin:0.8rem 0;">퀴즈 완료!</div>'
                        f'<div style="font-size:2.5rem;font-weight:700;background:linear-gradient(135deg,#b5179e,#7209b7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{pct}점</div>'
                        f'<div style="color:#888;">정답 {ok_cnt}개 / 오답 {ng_cnt}개</div></div>',
                        unsafe_allow_html=True
                    )
                    if st.button("🔄 다시 퀴즈", use_container_width=True, key=f"kj_qrestart_{lvname}"):
                        order2 = list(range(len(kanji_list))); random.shuffle(order2)
                        st.session_state[kj_order_key]  = order2
                        st.session_state[kj_idx_key]    = 0
                        st.session_state[kj_ok_key]     = 0
                        st.session_state[kj_ng_key]     = 0
                        st.session_state[qans_key]      = None
                        st.session_state[qshow_key]     = False
                        st.rerun()
                else:
                    kdata = kanji_list[order[idx]]
                    st.progress(idx / total_c, text=f"🧪 {idx+1} / {total_c}  ·  ✅{ok_cnt}  ❌{ng_cnt}")

                    # 퀴즈 유형: 한자 → 뜻
                    st.markdown(
                        f'<div class="quiz-card">'
                        f'<div style="font-size:0.85rem;color:#aaa;margin-bottom:0.5rem;">이 한자의 뜻은?</div>'
                        f'<div style="font-family:Noto Serif JP,serif;font-size:4rem;font-weight:700;color:#1a0a2e;">{kdata["kanji"]}</div>'
                        f'<div style="font-size:0.85rem;color:#b5179e;margin-top:0.3rem;">{kdata["strokes"]}획</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    # 보기 4개 생성
                    others = [k for i2, k in enumerate(kanji_list) if i2 != order[idx]]
                    wrong3 = random.sample(others, min(3, len(others)))
                    choices = random.sample([kdata["meaning"]] + [k["meaning"] for k in wrong3], min(4, len(wrong3)+1))

                    answered = st.session_state[qans_key]
                    if answered is None:
                        qc1, qc2 = st.columns(2)
                        for ci2, ch in enumerate(choices):
                            with (qc1 if ci2%2==0 else qc2):
                                if st.button(ch, use_container_width=True, key=f"kj_ch_{lvname}_{idx}_{ci2}"):
                                    st.session_state[qans_key]  = ch
                                    st.session_state[qshow_key] = True
                                    if ch == kdata["meaning"]:
                                        st.session_state[kj_ok_key] += 1
                                    else:
                                        st.session_state[kj_ng_key] += 1
                                    st.rerun()
                    else:
                        is_ok = (answered == kdata["meaning"])
                        if is_ok:
                            st.markdown('<div class="correct-badge">🎉 정답!</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="wrong-badge">❌ 오답 · 정답: {kdata["meaning"]}</div>', unsafe_allow_html=True)
                        st.markdown(
                            f'<div style="background:white;border-radius:14px;padding:1rem 1.5rem;'
                            f'box-shadow:0 2px 12px rgba(114,9,183,0.08);margin:0.5rem 0;text-align:center;">'
                            f'<div style="font-family:Noto Serif JP,serif;font-size:2rem;font-weight:700;">{kdata["kanji"]}</div>'
                            f'<div style="color:#b5179e;font-size:0.9rem;">{kdata["onyomi"]} / {kdata["kunyomi"]}</div>'
                            f'<div style="color:#444;font-size:0.85rem;margin-top:0.2rem;">{kdata["example"]}</div>'
                            f'<a href="https://jisho.org/search/{kdata["kanji"]}%20%23kanji" target="_blank" '
                            f'style="color:#7209b7;font-size:0.78rem;text-decoration:none;">📖 필획 순서 →</a>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                        if st.button("다음 →", use_container_width=True, key=f"kj_next_{lvname}_{idx}"):
                            st.session_state[kj_idx_key]  += 1
                            st.session_state[qans_key]     = None
                            st.session_state[qshow_key]    = False
                            st.rerun()

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
