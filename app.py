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

st.markdown("<h1 style='text-align: center;'>🧹 Data Sweeper</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Easily clean, analyze, and convert your CSV and Excel files.</h3>", unsafe_allow_html=True)

# ---------------- Growth Mindset Section ---------------- #
st.markdown("<h2 style='text-align: center;'>🚀 Growth Mindset Challenge: Web App with Streamlit</h2>", unsafe_allow_html=True)

st.markdown("""
### 🌱 What is a Growth Mindset?
A **growth mindset** is the belief that abilities and intelligence can be developed through **hard work, perseverance, and learning from mistakes**. This concept, popularized by **Carol Dweck**, challenges the idea that our skills are fixed. Instead, it emphasizes that every challenge is an opportunity to learn and grow.

### 💡 Why Adopt a Growth Mindset?
- **🚀 Embrace Challenges:** See obstacles as opportunities to grow, not as setbacks.
- **📖 Learn from Mistakes:** Mistakes are a natural part of learning—each error is a stepping stone to improvement.
- **💪 Persist Through Difficulties:** Stay determined even when things get tough.
- **🎉 Celebrate Effort:** Recognize the effort you put in, not just the outcome.
- **🔎 Keep an Open Mind:** Stay curious and be willing to adjust your approach.

### 🔥 How Can You Practice a Growth Mindset?
✅ **Set Learning Goals:** Focus on developing skills rather than just achieving high grades.  
✅ **Reflect on Your Learning:** Regularly think about what you’ve learned from successes and challenges.  
✅ **Seek Feedback:** Embrace constructive criticism to improve.  
✅ **Stay Positive:** Believe in your ability to grow and encourage others to do the same.  

Remember, your journey isn’t just about proving your intelligence—it’s about developing it. 🌟  
Every step, whether forward or backward, is part of the learning process. **Embrace your potential and keep striving for growth!** 🚀

_Wishing you success on your journey of continuous improvement!_ ✨
""", unsafe_allow_html=True)

# ---------------- File Upload Section ---------------- #
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
