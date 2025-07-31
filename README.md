# 🤖 Natural Language Cross-Platform Data Query RAG Agent

> An AI-powered system that enables business users to query complex financial data from multiple databases using plain English and receive responses in text, table, or graph format.

## 📑 Table of Contents
- [About the Project](#about-the-project)
- [Demo](#demo)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Limitations and Future Work](#limitations-and-future-work)
- [License](#license)
- [Contact](#contact)



## 📖 About the Project

This AI-powered application enables users to query financial data using natural language and get instant responses in text, table, or graph format.
It combines structured data from MongoDB and MySQL, processes it with a LangChain RAG agent, and delivers insights via a user-friendly React dashboard.
The system supports cross-platform data querying for wealth management scenarios involving high-net-worth individuals.

The system allows wealth management advisors to ask natural language questions like:

> "What are the top five portfolios of our wealth members?"  
> "Give me the breakup of portfolio values per relationship manager."  
> "Which clients are the highest holders of [specific stock]?"

It seamlessly merges data from:
- **MongoDB** (client profiles)
- **MySQL** (transaction data)

And uses a **LangChain-powered Pandas DataFrame agent** to process cross-platform queries intelligently. Responses are visualized in multiple formats: **Text**, **Table**, and **Graph**.



## 🎥 Demo

> **📽️ Video Presentation:** [Google Drive Link](https://drive.google.com/file/d/1mwHSAzueq4rLWVRdBLbgedShtLgter-2/view?usp=drivesdk)
> **Deployement Link:** [https://query-portfolio.vercel.app/]

## ✨ Features

- ✅ Natural language query input (e.g., “Show me all high-risk investors”)
- 📊 Supports 3 output formats: **text**, **table**, and **graph**
- 🔌 Integrated MongoDB + MySQL into a single DataFrame for unified querying
- 🧠 LangChain + LLaMA-3 RAG agent with error handling and parsing robustness
- 🕵️ Recent query history with timestamps and persistent storage
- 📤 Export results as TXT, CSV, or PDF
- 🎛️ Modern dashboard with ReactJS, Tailwind CSS, and Chart.js
- 🧩 Modular backend powered by FastAPI
- 🔒 Extensible for future authentication, caching, and role-based access


## 🛠️ Tech Stack

### 🧠 AI & Backend
- **Python**, **FastAPI**
- **LangChain**, **Pandas DataFrame Agent**
- **MongoDB**, **MySQL**
- **Groq LLaMA 3 8B**

### 💻 Frontend
- **ReactJS**
- **Vite**
- **Tailwind CSS**
- **Chart.js** (Line, Bar, Polar Area)


## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/vishnuvardhanreddythornala/Natural-Language-Cross-Platform-Data-Query-RAG-Agent.git
cd Natural-Language-Cross-Platform-Data-Query-RAG-Agent

#.env file
  Groq API key
  mongodb & Mysql credentials

# Backend Setup
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend Setup
cd frontend
npm install
npm run dev

```

## 🚀 Usage
- Enter your query in plain English (e.g., "Top portfolios by AUM").

- Select response format: Text, Table, or Graph.

- View live output with visual insights.

- Export results or explore past queries.


## 📁 Project Structure
```
Natural-Language-Cross-Platform-Data-Query-RAG-Agent/
├── backend/
│   ├── main.py
│   ├── langchain_agent.py
│   ├── mongo_connector.py
│   ├── mysql_connector.py
│   └── requirements.txt
    └── .env
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── ...
│   └── tailwind.config.js
├── dist/  # React build folder served via FastAPI
└── README.md
```

## 🔮 Limitations

- No user authentication or access roles.

- Some long queries may time out or need formatting adjustments.

- Data is loaded fresh per query — lacks caching layer.

## Future Enhancements:

✅ Add role-based authentication (Advisors vs Clients)

🔁 Integrate Redis caching for frequently asked queries

📧 Replace CSV export with Email/PDF export

🧠 Integrate LangChain MCP for better memory & multi-turn querying

🧾 Query suggestion using past history & semantic retrieval

☁️ Cloud deployment via Render / Azure App Services

🔍 Switch to MongoDB Atlas Vector Search for future RAG expansion

## 📜 License
This project is licensed under the **MIT License**.

## 📞 Contact
- **Name**: Thornala Vishnu Vardhan Reddy
- **GitHub**: [@vishnuvardhanreddythornala](https://github.com/vishnuvardhanreddythornala)
- **Email**: [vishnuvardhanreddythornala@gmail.com]
