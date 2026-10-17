import streamlit as st

def play(level):
    st.markdown(f"### 🔢 Sudoku - Màn {level}")
    empty_cells = level * 8
    st.write(f"Màn {level}: Điền các số từ 1 đến 9 (Số ô trống: {empty_cells}).")

    level_key = f"sudoku_completed_{level}"
    if level_key not in st.session_state:
        st.session_state[level_key] = False

    if not st.session_state[level_key]:
        cols = st.columns(3)
        for i in range(3):
            with cols[i]:
                st.number_input(f"Ô {i+1}", min_value=1, max_value=9, key=f"s_cell_{level}_{i}")

        if st.button("Kiểm tra đáp án Sudoku", key=f"check_sudoku_{level}"):
            st.session_state[level_key] = True
            st.session_state[f"level_completed_{level}"] = True  # Kích hoạt nhận hoa thưởng
            st.success(f"🎉 Xuất sắc! Đã giải xong Sudoku Màn {level}!")
            st.balloons()
            st.rerun()
    else:
        st.success(f"✅ Bạn đã hoàn thành Màn {level} này rồi!")
        if st.button("Chơi lại màn này", key=f"replay_sudoku_{level}"):
            st.session_state[level_key] = False
            st.rerun()