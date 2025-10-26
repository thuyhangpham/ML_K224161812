import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# --- 1. Tải và xử lý dữ liệu ---

@st.cache_data
def load_data_and_model():
    # Tải dữ liệu
    try:
        df = pd.read_csv('True_News.csv')
    except FileNotFoundError:
        st.error("LỖI: Không tìm thấy tệp 'True_News.csv'.")
        st.error("Vui lòng tải tệp và đặt vào cùng thư mục với app.py")
        return None, None

    # Đổi tên cột (nếu cần)
    if 'Title' in df.columns:
        df = df.rename(columns={'Title':'title'})
    elif 'headline' in df.columns:
        df = df.rename(columns={'headline':'title'})

    if 'Category' in df.columns:
        df = df.rename(columns={'Category':'category'})
    elif 'subject' in df.columns:
        df = df.rename(columns={'subject':'category'})

    # Xử lý dữ liệu (giống hệt notebook của bạn)
    df = df[['category', 'title']].dropna().head(1000)
    df['entities'] = df['title'].apply(lambda x: ' '.join(x.split()[:3]))

    def clean_text(text):
        return str(text).replace(":", "").replace("|", "").replace("\n", " ")

    df['title_clean'] = df['title'].apply(clean_text)
    df['entities_clean'] = df['entities'].apply(clean_text)

    # "Huấn luyện" mô hình khuyến nghị
    vectorizer = CountVectorizer()
    X_features = vectorizer.fit_transform(df['title_clean'] + ' ' + df['entities_clean'])
    X_embeddings = X_features.toarray()
    similarity_matrix = cosine_similarity(X_embeddings)
    
    return df, similarity_matrix

# --- 2. Hàm khuyến nghị ---

def get_recommendations(article_index, similarity_matrix, df, top_k=5):
    sim_scores = similarity_matrix[article_index]
    sim_indices = np.argsort(sim_scores)[::-1]
    sim_indices = sim_indices[sim_indices != article_index]  # loại bỏ chính nó
    top_indices = sim_indices[:top_k]

    rec_list = []
    for idx in top_indices:
        rec_list.append({
            'recommended_title': df.iloc[idx]['title'],
            'recommended_category': df.iloc[idx]['category'],
            'similarity_score': sim_scores[idx]
        })
    return pd.DataFrame(rec_list)

# --- 3. Xây dựng giao diện ứng dụng Streamlit ---

st.set_page_config(page_title="Hệ thống Khuyến nghị", layout="wide")
st.title("Hệ thống Khuyến nghị")

# Tải dữ liệu và mô hình
df, similarity_matrix = load_data_and_model()

# Nếu tải dữ liệu thành công thì mới hiển thị phần còn lại
if df is not None and similarity_matrix is not None:
    
    st.header("1. Chọn một bài báo")
    
    # Tạo một dropdown (selectbox) cho phép người dùng chọn tiêu đề bài báo
    # 'options' là danh sách các tiêu đề
    all_titles = df['title']
    selected_title = st.selectbox(
        label="Chọn tiêu đề bài báo bạn muốn tìm bài tương tự:",
        options=all_titles
    )

    # Lấy index của bài báo đã chọn
    selected_index = df[df['title'] == selected_title].index[0]

    # Hiển thị thông tin bài báo gốc
    st.subheader("Bài báo gốc:")
    original_article = df.iloc[selected_index]
    st.write(f"**Tiêu đề:** {original_article['title']}")
    st.write(f"**Chủ đề:** {original_article['category']}")
    
    st.write("---") # Đường kẻ ngang
    
    # Hiển thị các bài báo khuyến nghị
    st.header("2. Các bài báo được khuyến nghị")
    
    # Gọi hàm khuyến nghị
    df_recommend = get_recommendations(selected_index, similarity_matrix, df, top_k=5)
    
    # Hiển thị kết quả dưới dạng bảng
    st.dataframe(df_recommend, use_container_width=True)