<div align="center">
  <img src="imagescan2023.png" alt="CAN 2023 Dashboard" width="750">

  <h1>🌍 CAN 2023 Performance Dashboard</h1>
  <p><b>Advanced Tactical Intelligence Platform | 2023 African Cup of Nations</b></p>

  [![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
  [![StatsBomb](https://img.shields.io/badge/StatsBomb-Open_Data-red?style=for-the-badge)](https://github.com/statsbomb/open-data)
  [![mplsoccer](https://img.shields.io/badge/mplsoccer-Pitch_Viz-3F4F75?style=for-the-badge)](https://mplsoccer.readthedocs.io)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
  [![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-can2023--dashboard.streamlit.app-success?style=for-the-badge)](https://can2023-dashboard.streamlit.app)

  > **A professional-grade AFCON analytics dashboard** covering all 24 nations —  
  > with tactical pass networks, spatial heatmaps, individual player geometry,  
  > and a premium dark-themed UI inspired by modern football broadcasting.

  [🚀 Live Demo](#-live-demo) • [✨ Features](#-key-features) • [📊 Data](#-data-source) • [📦 Installation](#️-installation--setup)

</div>

---

## 🚀 Live Demo

Experience the full tactical dashboard live on Streamlit Cloud:

🔗 **[can2023-dashboard.streamlit.app](https://can2023-dashboard.streamlit.app)**

> No installation required — explore CAN 2023 performance data directly in your browser.

---

## ✨ Key Features

### 🌍 Full Tournament Coverage
Complete data for all **24 nations** participating in the 2023 African Cup of Nations — from group stages through to the final.

### 🎨 Elite UI/UX
Professional dark-themed interface with custom typography, built to match the aesthetics of modern football broadcasting command centers.

### 🗺️ Advanced Tactical Maps

| Feature | Description |
|---|---|
| 📈 **Team Progression** | Visualize how teams advance into the final third |
| 🗺️ **Individual Pass Maps** | Successful vs incomplete passes with directional vectors per player |
| 🔥 **Activity Heatmaps** | High-resolution spatial density maps with directional watermarks |
| 🕸️ **Tactical Pass Networks** | Team passing structure and connectivity graphs before substitutions |

### ⚡ Optimized Performance
- Local **CSV storage** for instant data loading — no API calls at runtime
- Memory-efficient processing pipeline for smooth cloud deployment

---

## 🛠️ Technology Stack

| Category | Technology | Purpose |
|---|---|---|
| **Framework** | [Streamlit](https://streamlit.io/) | Web application engine |
| **Data Source** | [StatsBomb Open Data](https://github.com/statsbomb/open-data) | Match & event data |
| **Pitch Viz** | [mplsoccer](https://mplsoccer.readthedocs.io/) | Pitch rendering & pass networks |
| **Visualization** | [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/) | Charts & heatmaps |
| **Data Processing** | [Pandas](https://pandas.pydata.org/) | Data manipulation & CSV I/O |

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Step-by-step

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd can23
```

**2. Create a virtual environment** *(recommended)*
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. (Optional) Extract fresh data**

> Only needed if the `data/` folder is empty or requires updating:
```bash
python data_extractor.py
```

**5. Launch the dashboard**
```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501` 🎉

---

## 📁 Project Structure
```
can23/
├── app.py                  # Main Streamlit entry point
├── data_extractor.py       # StatsBomb data fetcher & CSV builder
├── requirements.txt        # Python dependencies
├── imagescan2023.png       # Dashboard preview image
├── data/                   # Preprocessed CSV data files
└── README.md               # Project documentation
```

---

## 📊 Data Source

All match and event data is powered by **[StatsBomb Open Data](https://github.com/statsbomb/open-data)** — freely available for research and educational use.

> 📌 Data covers all CAN 2023 matches across every round of the tournament, from group stages to the final.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your branch: `git checkout -b feature/NewAnalysis`
3. Commit your changes: `git commit -m 'Add new tactical module'`
4. Push and open a Pull Request

---

<div align="center">

**Built with ❤️ for African football fans and data analysts**

⭐ If you find this project useful, please consider giving it a star!

🔗 **[can2023-dashboard.streamlit.app](https://can2023-dashboard.streamlit.app)**

</div>
