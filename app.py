import streamlit as st
import json
from datetime import date, datetime
import random

# ─── SAYFA AYARLARI ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GünIşığı ☀️",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Baloo+2:wght@500;700;800&display=swap');

/* Genel arka plan */
.stApp {
    background: linear-gradient(135deg, #FFF9F0 0%, #F0F8FF 50%, #FFF0F8 100%);
    font-family: 'Nunito', sans-serif;
}

/* Başlık */
h1, h2, h3 {
    font-family: 'Baloo 2', cursive !important;
    color: #4A4A8A !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E8F4FD 0%, #F3E8FF 100%) !important;
    border-right: 3px solid #C8A8E9;
}

[data-testid="stSidebar"] .stRadio label {
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    color: #5A5A9A !important;
    padding: 8px 12px !important;
    border-radius: 12px !important;
    transition: all 0.2s ease;
}

/* Büyük renkli kartlar */
.big-card {
    background: white;
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 8px 24px rgba(100, 100, 200, 0.12);
    border: 3px solid transparent;
    transition: all 0.3s ease;
    text-align: center;
    cursor: pointer;
}

.big-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(100, 100, 200, 0.2);
}

/* Duygu kartları */
.emotion-card {
    background: white;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    transition: all 0.25s ease;
    border: 3px solid #E8E8F8;
}

.emotion-card:hover {
    transform: scale(1.05);
}

/* Görev kartları */
.task-card {
    background: white;
    border-radius: 18px;
    padding: 18px 24px;
    margin: 10px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.07);
    border-left: 6px solid #A8D8EA;
    font-size: 1.05rem;
    font-weight: 600;
    color: #333366;
    display: flex;
    align-items: center;
    gap: 14px;
}

.task-done {
    border-left-color: #90EE90 !important;
    background: #F5FFF5 !important;
    text-decoration: line-through;
    color: #888 !important;
}

/* Rozetler */
.badge {
    display: inline-block;
    font-size: 2.5rem;
    margin: 8px;
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.15));
    transition: transform 0.2s;
}

.badge:hover {
    transform: scale(1.2) rotate(5deg);
}

/* Başarı kutusu */
.success-box {
    background: linear-gradient(135deg, #D4EDDA, #C3E6CB);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    border: 3px solid #90EE90;
    margin: 16px 0;
}

/* Sosyal kart */
.social-card {
    background: linear-gradient(135deg, #FFF5E6, #FFE8CC);
    border-radius: 20px;
    padding: 24px;
    border: 3px solid #FFD59E;
    margin: 12px 0;
}

/* Progress bar özelleştirme */
.stProgress > div > div {
    border-radius: 10px !important;
    height: 18px !important;
}

/* Butonlar */
.stButton button {
    border-radius: 16px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    padding: 12px 24px !important;
    transition: all 0.2s ease !important;
    border: none !important;
}

.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important;
}

/* Seçili duygu */
.selected-emotion {
    background: linear-gradient(135deg, #E8F5FF, #D0EAFF) !important;
    border-color: #70B8FF !important;
}

/* Ödül animasyonu */
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
}

.bouncing {
    animation: bounce 1s ease infinite;
    display: inline-block;
}

/* Günlük takvim */
.calendar-day {
    background: white;
    border-radius: 14px;
    padding: 14px;
    text-align: center;
    box-shadow: 0 3px 10px rgba(0,0,0,0.07);
    border: 2px solid #E8E8F8;
}

/* Nefes egzersizi */
.breathe-box {
    background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
    border-radius: 30px;
    padding: 40px;
    text-align: center;
    border: 4px solid #A5D6A7;
}

/* Welcome banner */
.welcome-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 28px;
    padding: 32px 40px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.35);
}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE BAŞLANGICI ─────────────────────────────────────────────────
if "yildizlar" not in st.session_state:
    st.session_state.yildizlar = 0
if "tamamlanan_gorevler" not in st.session_state:
    st.session_state.tamamlanan_gorevler = set()
if "secilen_duygu" not in st.session_state:
    st.session_state.secilen_duygu = None
if "rozetler" not in st.session_state:
    st.session_state.rozetler = []
if "cocuk_adi" not in st.session_state:
    st.session_state.cocuk_adi = "Kahraman"

# ─── VERİ ─────────────────────────────────────────────────────────────────────
GUNLUK_GOREVLER = [
    {"id": 1, "ikon": "🌅", "metin": "Sabah uyanıp yatağımı topluyorum", "renk": "#FFE4B5"},
    {"id": 2, "ikon": "🦷", "metin": "Dişlerimi fırçalıyorum", "renk": "#E4F7F7"},
    {"id": 3, "ikon": "👕", "metin": "Giysilerimi giyiyorum", "renk": "#E4ECF7"},
    {"id": 4, "ikon": "🍳", "metin": "Kahvaltımı yapıyorum", "renk": "#FFF0E4"},
    {"id": 5, "ikon": "🎒", "metin": "Çantamı hazırlıyorum", "renk": "#F0E4FF"},
    {"id": 6, "ikon": "📚", "metin": "Ödevlerimi bitiriyorum", "renk": "#E4FFEC"},
    {"id": 7, "ikon": "🛁", "metin": "Banyomu yapıyorum", "renk": "#E4F0FF"},
    {"id": 8, "ikon": "🌙", "metin": "Uyumadan önce kitap okuyorum", "renk": "#F7E4FF"},
]

DUYGULAR = [
    {"ikon": "😊", "ad": "Mutlu", "renk": "#FFF176", "mesaj": "Harika! Mutlu olmak çok güzel bir his! 🌟"},
    {"ikon": "😢", "ad": "Üzgün", "renk": "#BBDEFB", "mesaj": "Üzülmek tamam. Bazen hepimiz üzülürüz. Seni seviyoruz 💙"},
    {"ikon": "😡", "ad": "Sinirli", "renk": "#FFCDD2", "mesaj": "Derin nefes alabilirsin. 1-2-3... Her şey yoluna girecek 🌈"},
    {"ikon": "😨", "ad": "Korkmuş", "renk": "#E1BEE7", "mesaj": "Korktuğunda güvendiğin birine söyleyebilirsin. Yalnız değilsin! 🤗"},
    {"ikon": "😴", "ad": "Yorgun", "renk": "#B2EBF2", "mesaj": "Dinlenmek çok önemli. Biraz mola vermen iyi olabilir 😴"},
    {"ikon": "🤩", "ad": "Heyecanlı", "renk": "#F8BBD0", "mesaj": "Heyecan harika! Bu enerjiyi paylaşmak ister misin? ⭐"},
    {"ikon": "🤔", "ad": "Kafası Karışık", "renk": "#DCEDC8", "mesaj": "Anlamadığında sormak her zaman iyidir! 💡"},
    {"ikon": "🥰", "ad": "Sevgi Dolu", "renk": "#FCE4EC", "mesaj": "Sevgi paylaştıkça çoğalır! Sen çok seviliyorsun ❤️"},
]

SOSYAL_SENARYOLAR = [
    {
        "baslik": "Arkadaşına merhaba demek 👋",
        "aciklama": "Okul koridorunda bir arkadaşınla karşılaştın.",
        "adimlar": ["Gülümse 😊", "Gözlerine bak 👀", "'Merhaba!' de", "Nasıl olduğunu sor"],
        "renk": "#FFF9C4",
    },
    {
        "baslik": "Yardım istemek 🙋",
        "aciklama": "Bir şeyi anlamadın ve öğretmenden yardım isteyeceksin.",
        "adimlar": ["Elini kaldır ✋", "Öğretmenin gelmesini bekle", "'Anlamadım, yardım eder misiniz?' de", "Teşekkür et 🙏"],
        "renk": "#C8E6C9",
    },
    {
        "baslik": "Sıraya girmek 🚶",
        "aciklama": "Yemekhanede herkes sıraya girmiş.",
        "adimlar": ["En arkaya git", "Sabırla bekle ⏰", "Sıra sana gelince ilerle", "Kibarca seçimini yap"],
        "renk": "#BBDEFB",
    },
    {
        "baslik": "Oyuna katılmak 🎮",
        "aciklama": "Arkadaşların bir oyun oynuyor ve sen de katılmak istiyorsun.",
        "adimlar": ["Oyunu izle 👀", "'Ben de oynayabilir miyim?' diye sor", "Kuralları dinle 📋", "Eğlen! 🎉"],
        "renk": "#E1BEE7",
    },
]

NEFES_ADIMLARI = [
    ("🌬️ Nefes Al", "Burnundan yavaşça nefes al... 1, 2, 3, 4", "#E3F2FD"),
    ("🫁 Tut", "Nefesini tut... 1, 2, 3, 4", "#E8EAF6"),
    ("😮‍💨 Ver", "Ağzından yavaşça ver... 1, 2, 3, 4, 5, 6", "#E8F5E9"),
    ("✨ Tekrarla", "Harika! Tekrar yapalım mı?", "#FFF9C4"),
]

# ─── ROZET SİSTEMİ ────────────────────────────────────────────────────────────
def rozet_kontrol():
    yildiz = st.session_state.yildizlar
    tum_rozetler = [
        (5, "⭐", "İlk Adım"),
        (10, "🌟", "Parlayan Yıldız"),
        (20, "🏆", "Şampiyon"),
        (30, "🦁", "Cesur Aslan"),
        (50, "🚀", "Uzay Kaşifi"),
        (100, "👑", "Büyük Kahraman"),
    ]
    for puan, rozet, ad in tum_rozetler:
        if yildiz >= puan and rozet not in st.session_state.rozetler:
            st.session_state.rozetler.append(rozet)
            st.balloons()
            st.success(f"🎉 Yeni rozet kazandın: {rozet} {ad}!")

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding: 16px 0;'>
        <div style='font-size:3rem;'>☀️</div>
        <div style='font-family: Baloo 2, cursive; font-size:1.6rem; font-weight:800; color:#4A4A8A;'>GünIşığı</div>
        <div style='color:#888; font-size:0.85rem;'>Senin güzel günün</div>
    </div>
    """, unsafe_allow_html=True)

    isim = st.text_input("👶 Adın ne?", value=st.session_state.cocuk_adi)
    if isim:
        st.session_state.cocuk_adi = isim

    st.markdown("---")
    st.markdown(f"""
    <div style='text-align:center; background:white; border-radius:16px; padding:16px; margin:8px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.08);'>
        <div style='font-size:2rem;'>⭐</div>
        <div style='font-family: Baloo 2; font-size:2rem; font-weight:800; color:#F4A228;'>{st.session_state.yildizlar}</div>
        <div style='color:#666; font-size:0.9rem; font-weight:600;'>Yıldız</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.rozetler:
        st.markdown(f"""
        <div style='text-align:center; background:white; border-radius:16px; padding:12px; margin:8px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.08);'>
            <div style='font-size:0.85rem; color:#888; font-weight:700; margin-bottom:6px;'>ROZETLERİM</div>
            <div>{"".join([f'<span class="badge">{r}</span>' for r in st.session_state.rozetler])}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    menu = st.radio(
        "📍 Nereye gidelim?",
        ["🏠 Ana Sayfa", "📋 Günlük Görevler", "😊 Duygularım", "🤝 Sosyal Beceriler", "🌬️ Sakinleşme Köşesi"],
        label_visibility="collapsed"
    )

# ─── ANA SAYFA ────────────────────────────────────────────────────────────────
if menu == "🏠 Ana Sayfa":
    st.markdown(f"""
    <div class='welcome-banner'>
        <div style='font-family: Baloo 2; font-size:2rem; font-weight:800; margin-bottom:8px;'>
            Merhaba, {st.session_state.cocuk_adi}! 🌟
        </div>
        <div style='font-size:1.1rem; opacity:0.9;'>
            Bugün {date.today().strftime("%d %B %Y")} — Harika bir gün seni bekliyor!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hızlı durum kartları
    col1, col2, col3, col4 = st.columns(4)

    gorev_sayisi = len(GUNLUK_GOREVLER)
    tamamlanan = len(st.session_state.tamamlanan_gorevler)
    yuzde = int((tamamlanan / gorev_sayisi) * 100)

    with col1:
        st.markdown(f"""
        <div class='big-card' style='border-color:#FFD59E; background: linear-gradient(135deg, #FFF9F0, #FFF0DC);'>
            <div style='font-size:2.5rem;'>📋</div>
            <div style='font-family: Baloo 2; font-size:1.8rem; font-weight:800; color:#E67E22;'>{tamamlanan}/{gorev_sayisi}</div>
            <div style='color:#888; font-weight:700;'>Görev</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='big-card' style='border-color:#A8D8EA; background: linear-gradient(135deg, #F0F8FF, #DCF0FF);'>
            <div style='font-size:2.5rem;'>⭐</div>
            <div style='font-family: Baloo 2; font-size:1.8rem; font-weight:800; color:#3498DB;'>{st.session_state.yildizlar}</div>
            <div style='color:#888; font-weight:700;'>Yıldız</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='big-card' style='border-color:#C8A8E9; background: linear-gradient(135deg, #F8F0FF, #EDD8FF);'>
            <div style='font-size:2.5rem;'>🏅</div>
            <div style='font-family: Baloo 2; font-size:1.8rem; font-weight:800; color:#8E44AD;'>{len(st.session_state.rozetler)}</div>
            <div style='color:#888; font-weight:700;'>Rozet</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        duygu_ikon = "😊" if not st.session_state.secilen_duygu else st.session_state.secilen_duygu["ikon"]
        st.markdown(f"""
        <div class='big-card' style='border-color:#A8E9C0; background: linear-gradient(135deg, #F0FFF4, #DCFFE8);'>
            <div style='font-size:2.5rem;'>{duygu_ikon}</div>
            <div style='font-family: Baloo 2; font-size:1.2rem; font-weight:800; color:#27AE60;'>
                {st.session_state.secilen_duygu["ad"] if st.session_state.secilen_duygu else "Nasılsın?"}
            </div>
            <div style='color:#888; font-weight:700;'>Bugünkü Duygu</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # İlerleme çubuğu
    st.markdown(f"### 🌈 Bugünkü ilerleme: %{yuzde}")
    st.progress(yuzde / 100)

    st.markdown("<br>", unsafe_allow_html=True)

    # Motivasyon mesajı
    mesajlar = [
        "💪 Sen çok güçlüsün, bunu biliyoruz!",
        "🌟 Her gün bir adım daha ileriye!",
        "🦋 Sen özelsin ve seviliyorsun!",
        "🌈 Bugün harika şeyler yapacaksın!",
        "⭐ Küçük adımlar büyük başarılar getirir!",
    ]
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #fff9c4, #ffecb3); border-radius:20px; padding:24px; 
                text-align:center; border:3px solid #FFD54F; box-shadow: 0 4px 16px rgba(255,213,79,0.3);'>
        <div style='font-size:1.3rem; font-weight:800; color:#5D4037;'>{random.choice(mesajlar)}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── GÜNLÜK GÖREVLER ──────────────────────────────────────────────────────────
elif menu == "📋 Günlük Görevler":
    st.markdown("## 📋 Bugünün Görevleri")
    st.markdown(f"*Bir görevi tamamladığında onu işaretle, {st.session_state.cocuk_adi}!*")
    st.markdown("")

    tamamlanan_onceki = len(st.session_state.tamamlanan_gorevler)

    for gorev in GUNLUK_GOREVLER:
        gid = gorev["id"]
        tamamlandi = gid in st.session_state.tamamlanan_gorevler

        col_cb, col_text = st.columns([0.08, 0.92])
        with col_cb:
            kontrol = st.checkbox("", value=tamamlandi, key=f"gorev_{gid}")
        with col_text:
            css_class = "task-card task-done" if tamamlandi else "task-card"
            st.markdown(f"""
            <div class='{css_class}' style='background:{gorev["renk"]};'>
                <span style='font-size:1.5rem;'>{gorev["ikon"]}</span>
                <span>{gorev["metin"]}</span>
                {"<span style='margin-left:auto;'>✅</span>" if tamamlandi else ""}
            </div>
            """, unsafe_allow_html=True)

        if kontrol and gid not in st.session_state.tamamlanan_gorevler:
            st.session_state.tamamlanan_gorevler.add(gid)
            st.session_state.yildizlar += 2
            rozet_kontrol()
            st.rerun()
        elif not kontrol and gid in st.session_state.tamamlanan_gorevler:
            st.session_state.tamamlanan_gorevler.discard(gid)
            st.session_state.yildizlar = max(0, st.session_state.yildizlar - 2)
            st.rerun()

    st.markdown("---")
    tamamlanan = len(st.session_state.tamamlanan_gorevler)
    if tamamlanan == len(GUNLUK_GOREVLER):
        st.markdown("""
        <div class='success-box'>
            <div style='font-size:3rem;'>🎉🏆🎉</div>
            <div style='font-family: Baloo 2; font-size:1.5rem; font-weight:800; color:#2E7D32;'>
                TÜM GÖREVLERİ TAMAMLADIN!
            </div>
            <div style='color:#388E3C; font-weight:700; margin-top:8px;'>Sen gerçekten harikasin! 🌟</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='text-align:center; color:#666; font-weight:700; font-size:1.1rem;'>
            {tamamlanan} / {len(GUNLUK_GOREVLER)} görev tamamlandı 
            — {len(GUNLUK_GOREVLER) - tamamlanan} tane daha var! 💪
        </div>
        """, unsafe_allow_html=True)

# ─── DUYGULARIM ───────────────────────────────────────────────────────────────
elif menu == "😊 Duygularım":
    st.markdown("## 😊 Bugün nasıl hissediyorsun?")
    st.markdown("*İçinden geçen duyguyu seç. Her duygu önemlidir!*")
    st.markdown("")

    cols = st.columns(4)
    for i, duygu in enumerate(DUYGULAR):
        with cols[i % 4]:
            secili = st.session_state.secilen_duygu == duygu
            css_extra = "selected-emotion" if secili else ""
            st.markdown(f"""
            <div class='emotion-card {css_extra}'>
                <div style='font-size:3rem;'>{duygu["ikon"]}</div>
                <div style='font-weight:800; color:#4A4A8A; margin-top:8px;'>{duygu["ad"]}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Seç", key=f"duygu_{i}", use_container_width=True):
                st.session_state.secilen_duygu = duygu
                if st.session_state.yildizlar < 1 or True:
                    st.session_state.yildizlar += 1
                    rozet_kontrol()
                st.rerun()

    # Seçilen duygu mesajı
    if st.session_state.secilen_duygu:
        d = st.session_state.secilen_duygu
        st.markdown(f"""
        <br>
        <div style='background:linear-gradient(135deg, {d["renk"]}99, {d["renk"]}66); 
                    border-radius:24px; padding:28px; text-align:center;
                    border: 3px solid {d["renk"]}; margin-top:16px;
                    box-shadow: 0 8px 24px {d["renk"]}44;'>
            <div style='font-size:3.5rem; margin-bottom:12px;'>{d["ikon"]}</div>
            <div style='font-family: Baloo 2; font-size:1.4rem; font-weight:800; color:#4A4A8A; margin-bottom:8px;'>
                {d["ad"]} hissediyorsun
            </div>
            <div style='font-size:1.1rem; color:#555; font-weight:600;'>{d["mesaj"]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📖 Duygu Günlüğüm")
    st.markdown("*Bugün ne yaşadın? Yazmak ister misin?*")
    gunluk = st.text_area(
        "",
        placeholder="Bugün şöyle hissettim çünkü...",
        height=120,
        label_visibility="collapsed"
    )
    if st.button("📝 Kaydet", use_container_width=False):
        if gunluk.strip():
            st.session_state.yildizlar += 3
            rozet_kontrol()
            st.success("✅ Günlüğün kaydedildi! +3 yıldız kazandın ⭐")

# ─── SOSYAL BECERİLER ─────────────────────────────────────────────────────────
elif menu == "🤝 Sosyal Beceriler":
    st.markdown("## 🤝 Sosyal Beceriler")
    st.markdown("*Günlük hayatta karşılaşabileceğin durumlar ve nasıl davranabileceğin!*")
    st.markdown("")

    for i, senaryo in enumerate(SOSYAL_SENARYOLAR):
        with st.expander(f"{senaryo['baslik']}", expanded=(i == 0)):
            st.markdown(f"""
            <div class='social-card' style='background: linear-gradient(135deg, {senaryo["renk"]}, {senaryo["renk"]}88);
                         border-color: {senaryo["renk"]};'>
                <div style='font-size:1.05rem; color:#555; font-weight:700; margin-bottom:16px;'>
                    📍 Durum: {senaryo["aciklama"]}
                </div>
                <div style='font-weight:800; color:#4A4A8A; margin-bottom:12px; font-size:1.1rem;'>📌 Ne yapmalıyım?</div>
            """, unsafe_allow_html=True)

            for j, adim in enumerate(senaryo["adimlar"]):
                st.markdown(f"""
                <div style='background:white; border-radius:12px; padding:12px 18px; margin:8px 0;
                             border-left:5px solid {senaryo["renk"]}; font-weight:700; color:#333;'>
                    <span style='color:#888; margin-right:10px;'>{j+1}.</span> {adim}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            col_btn, col_empty = st.columns([1, 3])
            with col_btn:
                if st.button(f"✅ Anladım! +5⭐", key=f"sosyal_{i}", use_container_width=True):
                    st.session_state.yildizlar += 5
                    rozet_kontrol()
                    st.success(f"🎉 Harika! 5 yıldız kazandın!")

# ─── SAKİNLEŞME KÖŞESİ ───────────────────────────────────────────────────────
elif menu == "🌬️ Sakinleşme Köşesi":
    st.markdown("## 🌬️ Sakinleşme Köşesi")
    st.markdown("*Bazen bunalmış veya sinirli hissedebiliriz. Bu tamamen normal! Burada sakinleşebilirsin.*")
    st.markdown("")

    tab1, tab2, tab3 = st.tabs(["🌬️ Nefes Egzersizi", "🎨 Renkleri Say", "💆 Beden Taraması"])

    with tab1:
        st.markdown("""
        <div class='breathe-box'>
            <div style='font-size:4rem; margin-bottom:16px;' class='bouncing'>🫁</div>
            <div style='font-family: Baloo 2; font-size:1.6rem; font-weight:800; color:#2E7D32; margin-bottom:8px;'>
                Kutu Nefesi
            </div>
            <div style='color:#388E3C; font-size:1rem; font-weight:600;'>
                Bu teknik seni sakinleştirmeye yardım eder
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        adim_no = st.session_state.get("nefes_adim", 0)

        a = NEFES_ADIMLARI[adim_no % len(NEFES_ADIMLARI)]
        st.markdown(f"""
        <div style='background:{a[2]}; border-radius:20px; padding:28px; text-align:center;
                    border:3px solid {a[2]}; margin:12px 0;
                    box-shadow: 0 6px 20px {a[2]}88;'>
            <div style='font-size:2.5rem; margin-bottom:12px;'>{a[0].split()[0]}</div>
            <div style='font-family: Baloo 2; font-size:1.4rem; font-weight:800; color:#4A4A8A;'>{a[0]}</div>
            <div style='color:#666; font-size:1.05rem; font-weight:600; margin-top:8px;'>{a[1]}</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("➡️ Sonraki Adım", use_container_width=True):
                st.session_state.nefes_adim = (adim_no + 1) % len(NEFES_ADIMLARI)
                if (adim_no + 1) % len(NEFES_ADIMLARI) == 0:
                    st.session_state.yildizlar += 3
                    rozet_kontrol()
                    st.success("🎉 Bir tur nefes egzersizi tamamladın! +3⭐")
                st.rerun()

    with tab2:
        st.markdown("### 🌈 5-4-3-2-1 Sakinleştirici Teknik")
        st.markdown("""
        <div style='background:white; border-radius:20px; padding:24px; box-shadow: 0 4px 16px rgba(0,0,0,0.08);'>
        """, unsafe_allow_html=True)

        teknig = [
            ("👀", "5", "şey GÖR", "#FFECB3"),
            ("✋", "4", "şey DOKUN", "#C8E6C9"),
            ("👂", "3", "şey DUYUN", "#BBDEFB"),
            ("👃", "2", "şey KOK", "#E1BEE7"),
            ("👅", "1", "şey TAD", "#FFCDD2"),
        ]
        for ikon, sayi, eylem, renk in teknig:
            st.markdown(f"""
            <div style='background:{renk}; border-radius:14px; padding:16px 20px; margin:10px 0;
                         display:flex; align-items:center; gap:16px; font-weight:700; color:#333;
                         font-size:1.05rem;'>
                <span style='font-size:1.8rem;'>{ikon}</span>
                <span style='font-family: Baloo 2; font-size:1.5rem; font-weight:800; color:#4A4A8A; min-width:30px;'>{sayi}</span>
                <span>{eylem} etrafında ne var?</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("✅ Tamamladım! +4⭐", use_container_width=True):
                st.session_state.yildizlar += 4
                rozet_kontrol()
                st.success("🌟 Harika iş! 4 yıldız kazandın!")

    with tab3:
        st.markdown("### 💆 Beden Taraması")
        st.markdown("*Vücudunun her bölümünü sırayla gevşet.*")

        bedenler = [
            ("🦶", "Ayaklarını gevşet", "Ayaklarını yere bas, sonra bırak."),
            ("🦵", "Bacaklarını gevşet", "Bacaklarını sık, sonra bırak."),
            ("🧘", "Omuzlarını gevşet", "Omuzlarını kulaklarına kadar çek, sonra bırak."),
            ("✊", "Ellerini gevşet", "Yumruk yap, sonra aç."),
            ("😊", "Yüzünü gevşet", "Gözlerini kıs, sonra aç. Büyük gülümse!"),
        ]

        for ikon, baslik, aciklama in bedenler:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #E8F5E9, #C8E6C9); border-radius:16px; 
                         padding:18px 22px; margin:10px 0; border-left:5px solid #81C784;'>
                <div style='display:flex; align-items:center; gap:14px;'>
                    <span style='font-size:2rem;'>{ikon}</span>
                    <div>
                        <div style='font-weight:800; color:#2E7D32; font-size:1.1rem;'>{baslik}</div>
                        <div style='color:#555; font-weight:600;'>{aciklama}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("💆 Tamamladım! +4⭐", key="beden_btn", use_container_width=True):
                st.session_state.yildizlar += 4
                rozet_kontrol()
                st.success("🌟 Mükemmel! Bedenini dinlemeyi öğreniyorsun! +4⭐")

# ─── ALT BİLGİ ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#AAA; font-size:0.85rem; padding:12px;'>
    ☀️ GünIşığı — Otizmli çocuklar için sevgiyle tasarlandı 💙
</div>
""", unsafe_allow_html=True)
