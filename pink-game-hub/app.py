import streamlit as st
import streamlit.components.v1 as components
from games import puzzle, sudoku, tile_match
import os
import base64

# 1. Cấu hình trang
st.set_page_config(page_title="Game của Thư 🌸", page_icon="🎀", layout="centered")

# Hàm mã hóa ảnh nền sang Base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 2. Xử lý Ảnh nền động (Hình 2: bg_cherry_blossom.png)[cite: 21]
bg_img_path = "assets/ui/bg_cherry_blossom.png"

if os.path.exists(bg_img_path):
    bin_str = get_base64_of_bin_file(bg_img_path)
    st.html(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: 'Comic Sans MS', 'Fredoka', cursive, sans-serif;
    }}
    </style>
    """)
else:
    st.html("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #ffdeeb 0%, #ffe6fa 50%, #ffd1dc 100%);
    }
    </style>
    """)

# 3. CSS tùy chỉnh để căn giữa hoàn toàn khung nội dung (Ảnh 1)[cite: 20], chữ to, rõ, màu hồng nổi bật
st.html("""
<style>
    /* Căn giữa và tạo khung kính mờ sang trọng cho toàn bộ block chính */
    .block-container {
        max-width: 750px;
        padding: 3rem;
        background: rgba(255, 255, 255, 0.85);
        border-radius: 35px;
        box-shadow: 0 15px 35px rgba(255, 150, 180, 0.4);
        margin: 5vh auto;
        text-align: center;
        backdrop-filter: blur(5px);
        border: 3px solid #FFB6C1;
    }

    .main-title {
        font-size: 55px;
        font-weight: 900;
        color: #FF3366;
        text-align: center;
        text-shadow: 3px 3px 0px #FFF275, 6px 6px 12px rgba(0, 0, 0, 0.15);
        letter-spacing: 2px;
        margin-bottom: 30px;
        animation: float 2.5s ease-in-out infinite;
    }

    .game-title {
        font-size: 45px;
        font-weight: 900;
        color: #D6336C;
        text-align: center;
        text-shadow: 2px 2px 0px #FFF275;
        margin-bottom: 25px;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(-1deg); }
        50% { transform: translateY(-8px) rotate(1deg); }
    }

    /* Tùy chỉnh nút bấm chung */
    div.stButton > button {
        background: linear-gradient(180deg, #FF85A1 0%, #FF3366 100%) !important;
        color: white !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border-radius: 30px !important;
        border: 4px solid #FFFFFF !important;
        box-shadow: 0px 8px 20px rgba(255, 51, 102, 0.4) !important;
        padding: 12px 30px !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%;
    }

    div.stButton > button:hover {
        transform: scale(1.06) !important;
        box-shadow: 0px 14px 25px rgba(255, 51, 102, 0.6) !important;
        background: linear-gradient(180deg, #FF99B2 0%, #FF1A53 100%) !important;
    }

    .game-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        border: 3px solid #FF85A1;
        box-shadow: 0 8px 16px rgba(0,0,0,0.08);
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #C70039;
    }
</style>
""")

# Quản lý trạng thái màn hình
if "screen" not in st.session_state:
    st.session_state.screen = "welcome"
if "selected_game" not in st.session_state:
    st.session_state.selected_game = None
if "selected_level" not in st.session_state:
    st.session_state.selected_level = 1

# Hàm phát nhạc nền và hiệu ứng âm thanh
def play_sound(sfx_name):
    sound_map = {
        "click": "assets/bg_click.mp3",
        "win": "assets/win.mp3",
        "lose": "assets/lose.mp3",
        "bgm": "assets/bgm.mp3"
    }
    path = sound_map.get(sfx_name, "")
    if os.path.exists(path):
        if sfx_name == "bgm":
            sound_script = f"""
                <audio autoplay loop>
                    <source src="app/static/{path}" type="audio/mp3">
                </audio>
                <script>
                    var audio = new Audio("{path}");
                    audio.loop = true;
                    audio.play().catch(error => console.log("BGM autoplay blocked"));
                </script>
            """
        else:
            sound_script = f"""
                <script>
                    var audio = new Audio("{path}");
                    audio.play().catch(error => console.log("Audio blocked"));
                </script>
            """
        components.html(sound_script, height=0, width=0)

# Tự động phát nhạc nền khi khởi động ứng dụng[cite: 5]
if "bgm_played" not in st.session_state:
    play_sound("bgm")
    st.session_state.bgm_played = True

# ==================== MÀN HÌNH WELCOME ====================
if st.session_state.screen == "welcome":
    st.html('<div class="main-title">🌸 Game của Thư 🌸</div>')
    st.write("")
    
    # Hiển thị nút Play dạng Hình 3 (btn_play.png) ở chính giữa có thể ấn được[cite: 22]
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        btn_img_path = "assets/ui/btn_play.png"
        if os.path.exists(btn_img_path):
            st.image(btn_img_path, use_container_width=True)
            if st.button("🌸 BẮT ĐẦU CHƠI NGAY 🌸", key="btn_play_image"):
                play_sound("click")
                st.session_state.screen = "select_game"
                st.rerun()
        else:
            if st.button("▶ PLAY NOW"):
                play_sound("click")
                st.session_state.screen = "select_game"
                st.rerun()

# ==================== MÀN HÌNH CHỌN TRÒ CHƠI ====================
elif st.session_state.screen == "select_game":
    st.html('<div class="main-title" style="font-size: 45px;">CHỌN TRÒ CHƠI</div>')
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.html('<div class="game-card">🧩 Xếp Hình<br><span style="font-size:15px; color:#666;">Jigsaw Puzzle</span></div>')
        if st.button("Chơi Trò 1", key="btn_g1"):
            play_sound("click")
            st.session_state.selected_game = "Xếp Hình"
            st.session_state.screen = "select_level"
            st.rerun()
            
    with c2:
        st.html('<div class="game-card">🔢 Sudoku<br><span style="font-size:15px; color:#666;">Sudoku 9x9</span></div>')
        if st.button("Chơi Trò 2", key="btn_g2"):
            play_sound("click")
            st.session_state.selected_game = "Sudoku"
            st.session_state.screen = "select_level"
            st.rerun()

    with c3:
        st.html('<div class="game-card">🐯 Ghép 3 Ô<br><span style="font-size:15px; color:#666;">Tile Match 3D</span></div>')
        if st.button("Chơi Trò 3", key="btn_g3"):
            play_sound("click")
            st.session_state.selected_game = "Ghép 3"
            st.session_state.screen = "select_level"
            st.rerun()
            
    st.write("<br>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("⬅ Trang chủ"):
            play_sound("click")
            st.session_state.screen = "welcome"
            st.rerun()

# ==================== MÀN HÌNH CHỌN 5 MÀN (TẶNG HOA) ====================
elif st.session_state.screen == "select_level":
    st.html(f'<div class="game-title">{st.session_state.selected_game}</div>')
    st.markdown("### 🌸 Chọn màn chơi (Level 1 - 5):", help="Chọn cấp độ thử thách")
    
    cols = st.columns(5)
    for i in range(1, 6):
        with cols[i-1]:
            is_completed = st.session_state.get(f"level_completed_{i}", False)
            
            if st.button(f"Màn {i}", key=f"lvl_{i}"):
                play_sound("click")
                st.session_state.selected_level = i
                st.session_state.screen = "play"
                st.rerun()
                
            flower_path = "assets/ui/flower_reward.png"
            if os.path.exists(flower_path) and is_completed:
                st.image(flower_path, width=50)
            else:
                st.html("<p style='text-align: center; color: #b0b0b0; font-size: 22px;'>🌱</p>")

    st.write("<br>", unsafe_allow_html=True)
    if st.button("⬅ Chọn trò chơi khác"):
        play_sound("click")
        st.session_state.screen = "select_game"
        st.rerun()

# ==================== MÀN HÌNH CHƠI GAME ====================
elif st.session_state.screen == "play":
    st.html(f'<div class="game-title">{st.session_state.selected_game} - Màn {st.session_state.selected_level}</div>')
    
    game = st.session_state.selected_game
    level = st.session_state.selected_level
    
    if game == "Xếp Hình":
        puzzle.play(level)
    elif game == "Sudoku":
        sudoku.play(level)
    elif game == "Ghép 3":
        tile_match.play(level)

    st.divider()
    if st.button("⬅ Quay lại chọn Màn"):
        play_sound("click")
        st.session_state.screen = "select_level"
        st.rerun()
