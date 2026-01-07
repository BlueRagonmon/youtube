import streamlit as st
import pandas as pd
from main import (
    extract_video_id,
    get_youtube_client,
    get_video_info,
    download_thumbnail,
    get_comments
)

st.set_page_config(
    page_title="YouTube 영상 요약 분석",
    layout="wide"
)

st.title("📊 YouTube 댓글 & 영상 정보 요약")

# 🔐 secrets에서 API 키 불러오기
API_KEY = st.secrets["YOUTUBE_API_KEY"]

video_input = st.text_input("🎬 YouTube 영상 URL 또는 ID")

if st.button("분석 시작") and video_input:

    video_id = extract_video_id(video_input)
    youtube = get_youtube_client(API_KEY)
    info = get_video_info(youtube, video_id)

    if not info:
        st.error("❌ 영상 정보를 가져올 수 없습니다.")
        st.stop()

    # -----------------------
    # 썸네일
    # -----------------------
    st.subheader("🖼 썸네일")
    st.image(info["thumbnail_url"], width=480)

    st.download_button(
        label="썸네일 다운로드",
        data=download_thumbnail(info["thumbnail_url"]),
        file_name=f"{video_id}_thumbnail.jpg",
        mime="image/jpeg"
    )

    # -----------------------
    # 핵심 지표
    # -----------------------
    st.subheader("📌 영상 핵심 정보")

    col1, col2, col3 = st.columns(3)
    col1.metric("👁 조회수", f"{info['view_count']:,}")
    col2.metric("👍 좋아요", f"{info['like_count']:,}")
    col3.metric("💬 댓글 수", f"{info['comment_count']:,}")

    st.markdown(f"""
    **🎬 제목:** {info['title']}  
    **📺 채널:** {info['channel']}  
    **📅 업로드 날짜:** {info['published_date']}
    """)

    # -----------------------
    # 댓글
    # -----------------------
    st.subheader("💬 댓글 미리보기 (상위 50개)")
    comments = get_comments(youtube, video_id)

    df = pd.DataFrame(comments)
    st.dataframe(df, use_container_width=True)

else:
    st.info("YouTube 영상 URL 또는 ID를 입력하세요.")
