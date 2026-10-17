import streamlit as st

def play(level):
    st.markdown(f"### 🧩 Xếp Hình - Màn {level}")
    grid_size = level + 1 
    st.write(f"Độ khó: Lưới {grid_size} x {grid_size} mảnh ghép.")
    
    # Khóa trạng thái hoàn thành theo từng level riêng biệt
    level_key = f"puzzle_completed_{level}"
    if level_key not in st.session_state:
        st.session_state[level_key] = False

    if not st.session_state[level_key]:
        st.info("💡 Sắp xếp các mảnh ghép vào đúng vị trí để hoàn thành bức tranh.")
        if st.button("Hoàn thành màn chơi này", key=f"win_puzzle_{level}"):
            st.session_state[level_key] = True
            st.session_state[f"level_completed_{level}"] = True  # Kích hoạt nhận hoa thưởng
            st.success(f"🎉 Chúc mừng bạn đã vượt qua Xếp Hình Màn {level}!")
            st.balloons()
            st.rerun()
    else:
        st.success(f"✅ Bạn đã hoàn thành Màn {level} này rồi!")
        if st.button("Chơi lại màn này", key=f"replay_puzzle_{level}"):
            st.session_state[level_key] = False
            st.rerun()