import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime

st.set_page_config(page_title="🧾 Enhanced DataFrame Comparator", layout="wide")
st.title("🧮 Enhanced DataFrame Comparator")

@st.cache_data(show_spinner=False)
def read_uploaded_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith((".xlsx", ".xls")):
        return pd.read_excel(file)
    elif file.name.endswith(".parquet"):
        return pd.read_parquet(file)
    else:
        return None

def clean_dataframe(df, ignore_case=False):
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()
            if ignore_case:
                df[col] = df[col].str.lower()
            df[col] = df[col].replace(r'^\s*$', np.nan, regex=True)
    return df

# Upload
tab1, tab2, tab3, tab4 = st.tabs(["📂 Upload & Settings", "📊 Summary", "📑 Row-Level Diff", "📥 Export"])

with tab1:
    st.header("📂 Upload CSV, Excel, or Parquet files")
    file1 = st.file_uploader("Upload First File", type=["csv", "xlsx", "xls", "parquet"], key="file1")
    file2 = st.file_uploader("Upload Second File", type=["csv", "xlsx", "xls", "parquet"], key="file2")

    st.divider()
    st.subheader("⚙️ Comparison Settings")

    ignore_col_order = st.checkbox("Ignore Column Order", value=True)
    ignore_case = st.checkbox("Ignore Case in String Columns", value=True)
    exclude_cols = st.text_input("Columns to Ignore (comma-separated)", value="")

    options = {
        "ignore_col_order": ignore_col_order,
        "ignore_case": ignore_case,
        "exclude_cols": [col.strip() for col in exclude_cols.split(",") if col.strip()]
    }

    if file1 and file2:
        df1 = read_uploaded_file(file1)
        df2 = read_uploaded_file(file2)

        df1 = df1.drop(columns=options["exclude_cols"], errors='ignore')
        df2 = df2.drop(columns=options["exclude_cols"], errors='ignore')

        df1 = clean_dataframe(df1, ignore_case=options["ignore_case"])
        df2 = clean_dataframe(df2, ignore_case=options["ignore_case"])

        st.session_state.df1 = df1
        st.session_state.df2 = df2
        st.session_state.options = options

        # Column Filter
        combined_cols = sorted(set(df1.columns).union(df2.columns))
        combined_cols.insert(0, "All Columns")
        selected_column = st.selectbox("🔽 Filter by Column (applies to all tabs)", combined_cols, key="column_filter")
        st.session_state.column_filter




with tab2:
    st.header("📊 Summary Overview")

    if "df1" in st.session_state:
        df1 = st.session_state.df1
        df2 = st.session_state.df2
        options = st.session_state.options
        selected_col = st.session_state.column_filter

        def column_match():
            if options["ignore_col_order"]:
                return set(df1.columns) == set(df2.columns)
            else:
                return list(df1.columns) == list(df2.columns)

        summary_data = {
            "Check": [
                "Column Names Equal",
                "Data Types Equal",
                "Shape Equal",
                "Null Count Equal",
                "All Values Equal"
            ],
            "Result": [
                column_match(),
                df1.dtypes.equals(df2.dtypes),
                df1.shape == df2.shape,
                (df1.isnull().sum().reindex(df2.columns) == df2.isnull().sum()).all(),
                df1.equals(df2)
            ]
        }

        summary_df = pd.DataFrame(summary_data)

        def highlight_result(val):
            if val is True:
                return "background-color: green; color: white"
            elif val is False:
                return "background-color: red; color: white"
            return ""

        styled = summary_df.style.applymap(highlight_result, subset=["Result"])
        st.dataframe(styled, use_container_width=True)

        st.subheader("📌 Column Names Side-by-Side Comparison")

        # Compare column names positionally
        max_len = max(len(df1.columns), len(df2.columns))
        df1_cols = list(df1.columns) + [""] * (max_len - len(df1.columns))
        df2_cols = list(df2.columns) + [""] * (max_len - len(df2.columns))

        col_comparisons = [
            {
                "DF1 Column": c1,
                "DF2 Column": c2,
                "Match": "✅" if c1 == c2 and c1 != "" and c2 != "" else "❌"
            }
            for c1, c2 in zip(df1_cols, df2_cols)
        ]

        col_comp_df = pd.DataFrame(col_comparisons)
        if selected_col != "All Columns":
            col_comp_df = col_comp_df[
                (col_comp_df["DF1 Column"] == selected_col) |
                (col_comp_df["DF2 Column"] == selected_col)
            ]
        st.dataframe(col_comp_df, use_container_width=True)





with tab3:
    st.header("📑 Row-Level Differences (Grouped View)")

    if "df1" in st.session_state:
        df1 = st.session_state.df1.copy()
        df2 = st.session_state.df2.copy()
        selected_col = st.session_state.column_filter

        # Align indexes and columns
        df1_aligned, df2_aligned = df1.align(df2, join="outer", axis=1, fill_value=np.nan)
        df1_aligned, df2_aligned = df1_aligned.align(df2_aligned, join="outer", axis=0, fill_value=np.nan)

        data = {}
        columns_to_compare = [selected_col] if selected_col != "All Columns" else df1_aligned.columns

        for col in columns_to_compare:
            df1_col = df1_aligned[col]
            df2_col = df2_aligned[col]

            try:
                diff = df1_col - df2_col
            except:
                diff = np.where(df1_col != df2_col, "Changed", "")

            data[(col, "DF1")] = df1_col
            data[(col, "DF2")] = df2_col
            data[(col, "Diff")] = diff

        multi_df = pd.DataFrame(data)
        multi_df = multi_df.sort_index(axis=1, level=0)

        st.markdown("📋 Showing all rows with DF1 / DF2 / Difference per column:")
        st.dataframe(multi_df, use_container_width=True)





with tab4:
    st.header("📥 Export and Download Results")

    if "df1" in st.session_state:
        df1 = st.session_state.df1
        df2 = st.session_state.df2
        selected_col = st.session_state.column_filter

        st.markdown("### 🧼 Download Cleaned Files")

        df1_csv = df1.to_csv(index=False).encode("utf-8")
        df2_csv = df2.to_csv(index=False).encode("utf-8")

        st.download_button("⬇️ Download DF1 (Cleaned)", df1_csv, "df1_cleaned.csv", "text/csv")
        st.download_button("⬇️ Download DF2 (Cleaned)", df2_csv, "df2_cleaned.csv", "text/csv")

        st.markdown("### 🔍 Download Row-Level Differences")

        # Align for export
        df1_aligned, df2_aligned = df1.align(df2, join="outer", axis=1, fill_value=np.nan)
        df1_aligned, df2_aligned = df1_aligned.align(df2_aligned, join="outer", axis=0, fill_value=np.nan)

        data = {}
        columns_to_compare = [selected_col] if selected_col != "All Columns" else df1_aligned.columns

        for col in columns_to_compare:
            df1_col = df1_aligned[col]
            df2_col = df2_aligned[col]
            try:
                diff = df1_col - df2_col
            except:
                diff = np.where(df1_col != df2_col, "Changed", "")

            data[(col, "DF1")] = df1_col
            data[(col, "DF2")] = df2_col
            data[(col, "Diff")] = diff

        result_df = pd.DataFrame(data)
        result_df = result_df.sort_index(axis=1, level=0)

        # Flatten for CSV export
        result_flat = result_df.copy()
        result_flat.columns = ['_'.join(col).strip() for col in result_df.columns.values]
        result_csv = result_flat.to_csv(index=False).encode("utf-8")

        st.download_button("⬇️ Download Row-Level Differences (Filtered)", result_csv, "row_level_diff.csv", "text/csv")
