# 🧮 Streamlit DataFrame Comparator

Compare two data files (CSV, Excel, or Parquet) side-by-side using an interactive Streamlit app.  
This tool highlights differences in structure, datatypes, nulls, and row-level values — ideal for data engineers, analysts, and QA teams validating pipeline outputs.

---

## 🚀 Features

- 📂 **Multi-format file support**: `.csv`, `.xlsx`, `.xls`, `.parquet`
- ✅ **Data cleaning**: trims whitespace, replaces blanks with `NaN`, handles case sensitivity
- 📊 **Comparison Summary**:
  - Column Names
  - Data Types
  - Shape Equality
  - Null Counts
  - Value Equality
- 📌 **Column-by-Column Detail View**:
  - Show matching/mismatching types, nulls, values
- 🔍 **Row-Level Differences**:
  - Full record comparison for every column
  - Grouped display as: `DF1`, `DF2`, `Diff` under each column
- 🧭 **Column filter dropdown** across **every tab**
- 📥 **Export**:
  - Cleaned data (DF1, DF2)
  - Row-level diff (flattened or grouped)

---

## 🖼️ Preview

> *(Insert your screenshot here)*  
> ![screenshot](https://github.com/your-username/streamlit-df-comparator/assets/screenshot.png)

---

## 🛠️ Installation

Clone the repo and install requirements:

```bash
git clone https://github.com/your-username/streamlit-df-comparator.git
cd streamlit-df-comparator
pip install -r requirements.txt
streamlit run app.py
```

---

## 🐍 Requirements

```txt
streamlit
pandas
numpy
pyarrow
openpyxl
```

To install manually:

```bash
pip install streamlit pandas numpy pyarrow openpyxl
```

---

## 🧩 How to Use

1. Upload your two data files (any supported format)
2. Set cleaning and comparison options
3. Use dropdown to focus on any specific column
4. Check:
   - ✅ Summary tab for structure checks
   - 🔍 Row-Level tab for full side-by-side breakdown
   - 📥 Export tab to download results

---

## 📂 Supported File Types

- `.csv`
- `.xlsx` / `.xls`
- `.parquet`

---

## 💡 Why Use This?

This tool is ideal for:
- Validating **ETL/ELT pipeline outputs**
- Comparing **source vs. target** post-ingestion
- Debugging mismatches in staging vs. production
- Auditing machine learning input/output consistency
- Tracking column-level changes between two snapshots

---

## 🛠️ Roadmap Ideas

- [ ] Excel export with multi-level headers
- [ ] Heatmap for numeric deviations
- [ ] Tolerance-based comparisons
- [ ] Fuzzy matching for string values
- [ ] Change-only filtering mode

---

## 🤝 Contributions

PRs welcome!  
If you'd like to add a feature, open an issue first to discuss scope.

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Built by [Vijay Rodrigues](https://github.com/vijayrodrigues)

- 🌐 Website: [vijayrodrigues.com](https://vijayrodrigues.com)
- 💼 LinkedIn: [linkedin.com/in/vijayrodrigues](https://linkedin.com/in/vijayrodrigues)
- 🐙 GitHub: [@vijayrodrigues](https://github.com/vijayrodrigues)
- 📧 Email: rodriguesvijay92@gmail.com
