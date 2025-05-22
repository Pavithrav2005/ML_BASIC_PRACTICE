import streamlit as st
import pandas as pd
import io
import chardet

st.set_page_config(page_title="🧼 Auto Data Cleaner Tool")

st.title("🧼 Auto Data Cleaner Tool")
st.markdown("Upload your **CSV or Excel file**, and this tool will clean missing values and correct data types automatically.")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])

def load_csv_with_fallbacks(file_obj):
    # Read raw bytes to detect encoding
    raw_data = file_obj.read()
    file_obj.seek(0)
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    
    st.info(f"Detected file encoding: `{encoding}`")
    
    # Try multiple delimiters
    delimiters = [',', ';', '\t']
    
    for delim in delimiters:
        try:
            file_obj.seek(0)
            df = pd.read_csv(file_obj, encoding=encoding, delimiter=delim)
            if not df.empty and df.columns.size > 1:
                return df
        except Exception:
            continue
    raise ValueError("Failed to parse CSV with detected encoding and known delimiters.")

if uploaded_file:
    ext = uploaded_file.name.split('.')[-1].lower()

    try:
        if ext == 'csv':
            df = load_csv_with_fallbacks(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
    else:
        st.success("✅ File loaded successfully!")

        st.subheader("🔍 Original Data")
        st.dataframe(df.head())

        # Fill missing values
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype == 'object':
                    df[col].fillna(df[col].mode(dropna=True)[0], inplace=True)
                else:
                    df[col].fillna(df[col].mean(), inplace=True)

        # Convert column types
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                pass
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass

        st.subheader("🧽 Cleaned Data")
        st.dataframe(df.head())

        # Download button
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button("📥 Download Cleaned CSV", csv_buffer.getvalue(), "cleaned_data.csv", "text/csv")
