# CAN 2023 Performance Dashboard

An interactive Streamlit dashboard for analyzing performance data from the **2023 African Cup of Nations (CAN 2023)**.

## 🚀 Features
- **All 24 Teams**: Data for every nation participating in the tournament.
- **Elite UI/UX**: Professional dark theme with custom typography.
- **Advanced Tactical Maps**: 
  - Team progression to final third.
  - Individual pass maps (Successful/Incomplete).
  - Activity heatmaps with directional watermarks.
  - Tactical pass networks (connectivity graphs).
- **Optimized Performance**: Uses local CSV storage for instant data loading.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd can23
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Extract fresh data**:
   If you want to update the data, run:
   ```bash
   python data_extractor.py
   ```

4. **Run the dashboard**:
   ```bash
   streamlit run app.py
   ```

## 📊 Data Source
All data is powered by **StatsBomb Open Data**.

## 👤 App
https://can2023-dashboard.streamlit.app
