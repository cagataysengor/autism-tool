import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ─── SAYFA AYARLARI VE CSS ───────────────────────────────────────────────────────────
st.set_page_config(page_title="GünIşığı ☀️", page_icon="☀️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Baloo+2:wght@500;700;800&display=swap');
.stApp { background: linear-gradient(135deg, #FFF9F0 0%, #F0F8FF 50%, #FFF0F8 100%); font-family: 'Nunito', sans-serif; }
h1, h2, h3 { font-family: 'Baloo 2', cursive !important; color: #4A4A8A !important; }
.big-card { background: white; border-radius: 24px; padding: 28px; box-shadow: 0 8px 24px rgba(100, 100, 200, 0.12); text-align: center; }
.task-card { background: white; border-radius: 18px; padding: 18px 24px; margin: 10px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.07); border-left: 6px solid #A8D8EA; font-size: 1.05rem; font-weight: 600; display: flex; align-items: center; justify-content: space-between; }
.breathe-box { background: linear-gradient(135deg, #E8F5E9, #C8E6C9); border-radius: 30px; padding: 40px; text-align: center; border: 4px solid #A5D6A7; }
.welcome-banner { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 28px; padding: 32px 40px; color: white; margin-bottom: 28px; box-shadow: 0 12px 40px rgba(102, 126, 234, 0.35); }
.emotion-card { background: white; border-radius: 20px; padding: 20px; text-align: center; box-shadow: 0 4px 16px rgba(0,0,0,0.08); transition: all 0.25s ease; border: 3px solid #E8E8F8; cursor: pointer; }
.emotion-card:hover { transform: scale(1.05); }
div[data-testid="stButton"] button { border-radius: 12px; font-weight: bold; }
.diary-card { background: white; border-radius: 15px; padding: 20px; margin-bottom: 15px; border-left: 5px solid #FFD59E; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

# ─── VERİTABANI KURULUMU ────────────────────────────────────────────────────────────
DB_NAME = "gunisigi.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, child_name TEXT, points INTEGER, status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ledger (id INTEGER PRIMARY KEY, child_name TEXT, amount INTEGER, description TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS moods (id INTEGER PRIMARY KEY, child_name TEXT, mood TEXT, note TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS parent_notes (id INTEGER PRIMARY KEY, child_name TEXT, note TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    try:
        c.execute("ALTER TABLE moods ADD COLUMN note TEXT")
    except sqlite3.OperationalError:
        pass
        
    conn.commit()
    conn.close()

init_db()

def run_query(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

def fetch_data(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_child_stars(child_name):
    df = fetch_data("SELECT SUM(amount) as total FROM ledger WHERE child_name = ?", (child_name,))
    return int(df.iloc[0]['total']) if pd.notna(df.iloc[0]['total']) else 0

# ─── SESSION STATE (Oturum Yönetimi) ────────────────────────────────────────────────
if 'role' not in st.session_state:
    st.session_state.role = None
if 'child_name' not in st.session_state:
    st.session_state.child_name = ""

DUYGULAR = [
    {"ikon": "😊", "ad": "Mutlu"}, {"ikon": "😌", "ad": "Sakin"},
    {"ikon": "😡", "ad": "Sinirli"}, {"ikon": "😨", "ad": "Kaygılı"},
    {"ikon": "😢", "ad": "Üzgün"}
]
ODULLER = [
    {"id": 1, "ikon": "📺", "metin": "15 Dk Çizgi Film", "bedel": 10},
    {"id": 2, "ikon": "🏞️", "metin": "Parka Gitme", "bedel": 20},
    {"id": 3, "ikon": "🎮", "metin": "Oyun Süresi", "bedel": 25}
]

# ─── GİRİŞ EKRANI ───────────────────────────────────────────────────────────────────
if st.session_state.role is None:
    st.markdown("<div style='text-align:center; margin-top:50px;'><h1 style='font-size:4rem;'>☀️ GünIşığı</h1><p style='font-size:1.5rem; color:#666;'>Otizm Destek ve Günlük Rutin Uygulaması</p></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    with col2:
        if st.button("👨‍👩‍👧 Ebeveyn Girişi", use_container_width=True, type="primary"):
            st.session_state.role = "parent"
            st.rerun()
    with col3:
        if st.button("🌟 Çocuk Girişi", use_container_width=True):
            st.session_state.role = "child"
            st.rerun()

# ─── EBEVEYN PANELİ ─────────────────────────────────────────────────────────────────
elif st.session_state.role == "parent":
    with st.sidebar:
        st.markdown("### 👨‍👩‍👧 Ebeveyn Menüsü")
        if st.button("🚪 Çıkış Yap"):
            st.session_state.role = None
            st.rerun()

    st.markdown("<h1>⚙️ Ebeveyn Yönetim Paneli</h1>", unsafe_allow_html=True)
    
    # YENİ: 5. Sekme Eklendi (Ayarlar)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Görev Ekle", "📋 Aktif Görevler", "💖 Çocuğun Günlüğü", "📓 Ebeveyn Notları", "⚙️ Ayarlar"])
    
    with tab1:
        with st.form("add_task_form"):
            st.subheader("Yeni Rutin/Aktivite Ekle")
            t_title = st.text_input("Aktivite Adı (Örn: 🦷 Diş Fırçalama)")
            t_child = st.text_input("Çocuğun Adı")
            t_points = st.number_input("Kazanılacak Yıldız", min_value=1, max_value=10, value=2)
            submitted = st.form_submit_button("Kaydet ve Listeye Ekle")
            if submitted and t_title and t_child:
                run_query("INSERT INTO tasks (title, child_name, points) VALUES (?, ?, ?)", (t_title, t_child, t_points))
                st.success(f"{t_title} eklendi!")
                st.rerun()
                
    with tab2:
        st.subheader("Tüm Rutinler")
        tasks_df = fetch_data("SELECT id, title, child_name, points, status, created_at FROM tasks ORDER BY created_at DESC")
        if not tasks_df.empty:
            for _, row in tasks_df.iterrows():
                durum = "✅ Tamamlandı" if row['status'] == 'completed' else "⏳ Bekliyor"
                
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"**{row['title']}** - {row['child_name']} ({row['points']}⭐) | Durum: {durum}")
                with col2:
                    if st.button("🗑️ Sil", key=f"del_task_{row['id']}"):
                        run_query("DELETE FROM tasks WHERE id=?", (row['id'],))
                        st.rerun()
                st.divider()
        else:
            st.info("Henüz eklenmiş bir rutin yok.")

    with tab3:
        st.subheader("💖 Çocuğun Kendi Tuttuğu Günlükler ve Duygular")
        moods_df = fetch_data("SELECT id, child_name, mood, note, created_at FROM moods ORDER BY created_at DESC LIMIT 20")
        if not moods_df.empty:
            for _, row in moods_df.iterrows():
                tarih = str(row['created_at'])[:16]
                not_metni = row['note'] if pd.notna(row['note']) and row['note'].strip() != "" else "*(Sadece duygu seçti, not yazmadı)*"
                
                col1, col2 = st.columns([6, 1])
                with col1:
                    st.markdown(f"""
                    <div class='diary-card'>
                        <div style='color:#888; font-size:0.9rem; margin-bottom:5px;'>🗓️ {tarih} | 👦 <b>{row['child_name']}</b></div>
                        <div style='font-size:1.2rem; font-weight:bold; color:#4A4A8A; margin-bottom:8px;'>Hissiyat: {row['mood']}</div>
                        <div style='font-size:1.05rem; color:#333; background:#F8F9FA; padding:10px; border-radius:8px;'>✍️ <b>Çocuğun Notu:</b> {not_metni}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("🗑️ Sil", key=f"del_mood_{row['id']}"):
                        run_query("DELETE FROM moods WHERE id=?", (row['id'],))
                        st.rerun()
        else:
            st.info("Çocuğunuz henüz bir duygu veya günlük paylaşmadı.")

    with tab4:
        st.subheader("📓 Sizin Gözlemleriniz (Ebeveyn Notları)")
        with st.form("add_note_form"):
            n_child = st.text_input("Çocuğun Adı")
            n_text = st.text_area("Bugün nasıl geçti? Hangi konularda zorlandı, neleri başardı?")
            note_submitted = st.form_submit_button("Notu Kaydet")
            
            if note_submitted and n_child and n_text:
                run_query("INSERT INTO parent_notes (child_name, note) VALUES (?, ?)", (n_child, n_text))
                st.success("Not başarıyla kaydedildi!")
                st.rerun()
                
        st.markdown("---")
        st.subheader("Geçmiş Gözlemleriniz")
        notes_df = fetch_data("SELECT id, child_name, note, created_at FROM parent_notes ORDER BY created_at DESC")
        if not notes_df.empty:
            for _, row in notes_df.iterrows():
                tarih = str(row['created_at'])[:16] 
                col1, col2 = st.columns([6, 1])
                with col1:
                    st.markdown(f"**👦 {row['child_name']}** - *🗓️ {tarih}*")
                    st.info(row['note'])
                with col2:
                    if st.button("🗑️ Sil", key=f"del_note_{row['id']}"):
                        run_query("DELETE FROM parent_notes WHERE id=?", (row['id'],))
                        st.rerun()
        else:
            st.info("Henüz kaydedilmiş bir not bulunmuyor.")

    # YENİ: SİSTEMİ SIFIRLAMA SEKMESİ
    with tab5:
        st.subheader("⚠️ Sistemi Sıfırla")
        st.warning("Bu alandaki işlem uygulamadaki **TÜM** verileri (Görevler, Yıldızlar, Ebeveyn Notları ve Çocuk Günlükleri) kalıcı olarak siler. Test aşamasından sonra temiz bir başlangıç yapmak için kullanabilirsiniz.")
        
        st.markdown("### Toplam Yıldız Durumu")
        yildiz_df = fetch_data("SELECT child_name, SUM(amount) as total FROM ledger GROUP BY child_name")
        st.dataframe(yildiz_df, use_container_width=True)

        st.markdown("---")
        if st.button("🚨 TÜM VERİLERİ SİL VE SIFIRLA", type="primary"):
            run_query("DELETE FROM tasks")
            run_query("DELETE FROM ledger")
            run_query("DELETE FROM moods")
            run_query("DELETE FROM parent_notes")
            st.success("Tüm veriler başarıyla silindi! Uygulama sıfırlandı.")
            st.rerun()

# ─── ÇOCUK PANELİ ───────────────────────────────────────────────────────────────────
elif st.session_state.role == "child":
    
    if not st.session_state.child_name:
        st.markdown("<h1>👋 Merhaba! Sen Kimsin?</h1>", unsafe_allow_html=True)
        cocuklar = fetch_data("SELECT DISTINCT child_name FROM tasks")['child_name'].tolist()
        if cocuklar:
            secilen = st.selectbox("Adını seç:", [""] + cocuklar)
            if secilen:
                st.session_state.child_name = secilen
                st.rerun()
        else:
            st.warning("Ebeveynin henüz bir görev eklememiş. Lütfen önce ebeveyn panelinden giriş yapıp görev ekleyin.")
            if st.button("Geri Dön"):
                st.session_state.role = None
                st.rerun()
    
    else:
        child = st.session_state.child_name
        mevcut_yildiz = get_child_stars(child)
        
        with st.sidebar:
            st.markdown(f"### 🌟 Hoş geldin, {child}!")
            st.markdown(f"**Yıldızların: ⭐ {mevcut_yildiz}**")
            st.markdown("---")
            menu = st.radio("Nereye Gidelim?", ["🏠 Ana Sayfa", "📋 Aktivitelerim", "✍️ Duygularım & Günlüğüm", "🎁 Ödüller", "🌬️ Sakinleşme Köşesi"], label_visibility="collapsed")
            st.markdown("---")
            if st.button("🚪 Çıkış Yap"):
                st.session_state.role = None
                st.session_state.child_name = ""
                st.rerun()

        if menu == "🏠 Ana Sayfa":
            st.markdown(f"<div class='welcome-banner'><h1>Merhaba, {child}! 🌟</h1><p style='font-size:1.2rem;'>Bugün harika şeyler yapacaksın!</p></div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<div class='big-card'><h2>⭐ {mevcut_yildiz}</h2><p>Toplam Yıldızın</p></div>", unsafe_allow_html=True)
            with col2:
                bekleyen = fetch_data("SELECT COUNT(*) as c FROM tasks WHERE child_name=? AND status='pending'", (child,)).iloc[0]['c']
                st.markdown(f"<div class='big-card'><h2>📋 {bekleyen}</h2><p>Bekleyen Aktivite</p></div>", unsafe_allow_html=True)

        elif menu == "📋 Aktivitelerim":
            st.markdown("<h1>📋 Bugünün Aktiviteleri</h1>", unsafe_allow_html=True)
            tasks = fetch_data("SELECT * FROM tasks WHERE child_name=? AND status='pending'", (child,))
            
            if tasks.empty:
                st.success("Tüm aktivitelerini tamamladın! Harikasın! 🎉")
                st.balloons()
            else:
                for _, task in tasks.iterrows():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"<div class='task-card'><span>{task['title']}</span> <span style='color:#E67E22;'>+{task['points']}⭐</span></div>", unsafe_allow_html=True)
                    with col2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("✅ Yaptım!", key=f"task_{task['id']}", use_container_width=True):
                            run_query("UPDATE tasks SET status='completed' WHERE id=?", (task['id'],))
                            run_query("INSERT INTO ledger (child_name, amount, description) VALUES (?, ?, ?)", (child, task['points'], f"Görev: {task['title']}"))
                            st.snow()
                            st.rerun()

        elif menu == "✍️ Duygularım & Günlüğüm":
            st.markdown("<h1>✍️ Bugün Neler Oldu?</h1>", unsafe_allow_html=True)
            st.markdown("Burada hislerini seçebilir ve istersen neden böyle hissettiğini yazabilirsin.")
            
            with st.form("child_diary_form"):
                st.markdown("### 1️⃣ Şu an nasıl hissediyorsun?")
                duygu_listesi = [d['ikon'] + " " + d['ad'] for d in DUYGULAR]
                secilen_duygu = st.radio("Duygunu Seç:", duygu_listesi, horizontal=True)
                
                st.markdown("### 2️⃣ Neden böyle hissediyorsun? (İsteğe bağlı)")
                cocuk_notu = st.text_area("Bana biraz anlatmak ister misin? Neler yaşadın?", height=100)
                
                submit_btn = st.form_submit_button("Günlüğüme Kaydet ve Paylaş 💙")
                
                if submit_btn:
                    run_query("INSERT INTO moods (child_name, mood, note) VALUES (?, ?, ?)", (child, secilen_duygu, cocuk_notu))
                    st.success("Harika! Hislerin ve notun günlüğüne eklendi. Seni çok iyi anlıyoruz. 🌟")

        elif menu == "🎁 Ödüller":
            st.markdown(f"<h1>🎁 Ödül Mağazası</h1><p>Mevcut Yıldızın: ⭐ {mevcut_yildiz}</p>", unsafe_allow_html=True)
            cols = st.columns(3)
            for i, odul in enumerate(ODULLER):
                with cols[i % 3]:
                    st.markdown(f"<div class='big-card' style='border: 2px solid #FFD59E;'><div style='font-size:3rem;'>{odul['ikon']}</div><h4>{odul['metin']}</h4><h3 style='color:#E67E22;'>⭐ {odul['bedel']}</h3></div>", unsafe_allow_html=True)
                    if mevcut_yildiz >= odul['bedel']:
                        if st.button("🎁 Al", key=f"odul_{odul['id']}", use_container_width=True):
                            run_query("INSERT INTO ledger (child_name, amount, description) VALUES (?, ?, ?)", (child, -odul['bedel'], f"Ödül: {odul['metin']}"))
                            st.balloons()
                            st.success(f"{odul['metin']} ödülünü kazandın!")
                            st.rerun()
                    else:
                        st.button("Yetersiz Yıldız", key=f"odul_no_{odul['id']}", disabled=True, use_container_width=True)

        elif menu == "🌬️ Sakinleşme Köşesi":
            st.markdown("<h1>🌬️ Sakinleşme Köşesi</h1>", unsafe_allow_html=True)
            st.markdown("<div class='breathe-box'><div style='font-size:4rem;'>🫁</div><h2>Kutu Nefesi Egzersizi</h2><p style='font-size:1.2rem;'>Burnundan yavaşça nefes al (1,2,3,4)...<br>Nefesini tut (1,2,3,4)...<br>Ağzından yavaşça ver (1,2,3,4,5,6)...</p></div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sakinleştim (+2⭐)"):
                run_query("INSERT INTO ledger (child_name, amount, description) VALUES (?, ?, ?)", (child, 2, "Nefes Egzersizi"))
                st.success("Harika hissediyorsun! +2 Yıldız kazandın.")