import streamlit as st
import pandas as pd
import os
from io import BytesIO

def set_theme():
    st.markdown("""
    <style>
    .stApp {
        transition: background-color 0.5s ease;
    }
    .light-theme {
        background-color: #ffffff;
        color: #000000;
    }
    .dark-theme {
        background-color: #1E1E1E;
        color: #ffffff;
    }
    .big-font {
        font-size:20px !important;
    }
    .user-card {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .light-theme .user-card {
        background-color: #f0f2f6;
    }
    .dark-theme .user-card {
        background-color: #2E2E2E;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Data Sweeper", layout='wide')
set_theme()

st.title("🧹 Data Sweeper")
st.markdown("### Easily clean, analyze, and convert your CSV and Excel files.")

uploaded_files = st.file_uploader(
    "📂 Upload your files (CSV or Excel)",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        st.success(f"✅ **Uploaded:** {file.name} ({file.size} bytes)")
        st.write("🔍 **Preview of Data**")
        st.dataframe(df.head())

        st.subheader("🧹 Data Cleaning")
        if st.checkbox(f"Clean Data for **{file.name}**"):
            col1, col2 = st.columns(2)
            with col1:
                if st.checkbox("🚮 Remove Duplicates"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ **Duplicates Removed!**")
            with col2:
                if st.checkbox("🛠️ Fill Missing Values"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ **Missing values filled with column mean!**")

        st.subheader("📌 Select Columns")
        columns = st.multiselect(f"Choose columns for **{file.name}**", df.columns, default=df.columns)
        df = df[columns]

        st.subheader("📊 Quick Visualization")
        if st.checkbox(f"📉 Show Chart for **{file.name}**"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])

        st.subheader("📂 Convert File Format")
        conversion_type = st.radio(f"Choose format for **{file.name}**", ["CSV", "Excel"], key=file.name)

        if st.button(f"🔄 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                buffer.seek(0)
                file_name = os.path.splitext(file.name)[0] + ".csv"
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False)
                buffer.seek(0)
                file_name = os.path.splitext(file.name)[0] + ".xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            st.download_button(
                label=f"📥 Download Converted {file.name} as {conversion_type}",
                data=buffer.getvalue(),
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 **Thank you for using Data Sweeper!**")
