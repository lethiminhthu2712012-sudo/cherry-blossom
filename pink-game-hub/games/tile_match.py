import streamlit as st

def play(level):
    st.markdown(f"### 🐯 Ghép 3 Ô (Tile Match) - Màn {level}")
    total_tiles = level * 6
    st.write(f"Màn {level}: Cần xóa tổng cộng {total_tiles} thẻ bài.")

    level_key = f"tile_completed_{level}"
    if level_key not in st.session_state:
        st.session_state[level_key] = False

    if not st.session_state[level_key]:
        st.info("👇 Bấm chọn thẻ bài để đưa vào khay chờ (3 thẻ giống nhau sẽ biến mất):")
        animal_icons = ["🐼", "🐨", "🦊", "🐯", "🐰", "🦁"]
        
        cols = st.columns(6)
        for idx, icon in enumerate(animal_icons):
            with cols[idx]:
                if st.button(f"{icon}", key=f"tile_{level}_{idx}"):
                    st.toast(f"Đã chọn thẻ {icon}!")

        if st.button("Hoàn thành màn chơi (Mô phỏng thắng)", key=f"win_tile_{level}"):
            st.session_state[level_key] = True
            st.session_state[f"level_completed_{level}"] = True  # Kích hoạt nhận hoa thưởng
            st.success(f"🎉 Tuyệt vời! Bạn đã vượt qua Màn {level} Ghép 3!")
            st.balloons()
            st.rerun()
    else:
        st.success(f"✅ Bạn đã hoàn thành Màn {level} này rồi!")
        if st.button("Chơi lại màn này", key=f"replay_tile_{level}"):
            st.session_state[level_key] = False
            st.rerun()