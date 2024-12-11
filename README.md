# LLMOps Project with Langfuse

<div align="center">
  <!-- Replace with your project logo or team photo -->
  <img src="src/img/langfuse_logo.png" width="400" alt="Project Logo">
</div>

[![Langfuse Version](https://img.shields.io/badge/Langfuse-2.53.3-blue.svg)](https://langfuse.com)
[![Python Version](https://img.shields.io/badge/Python-3.10.5-green.svg?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3105/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Project Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/your-username/your-project)


## 🚀 Quick Overview

This LLMOps project leverages Langfuse 2.53.3 for comprehensive observability and evaluation of language model applications, built with Python 3.10.5.

## 📋 Prerequisites

- Python 3.10.5
- Langfuse 2.53.3
- pip package manager

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nachojeda/RagFuse.git
cd RagFuse
```

### 2. Set Up Virtual Environment

```bash
python3.10.5 -m venv venv
source venv/bin/activate  # MacOS
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Langfuse Credentials

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=<your_secret_key>
LANGFUSE_SECRET_KEY=<your_secret_key>
LANGFUSE_PUBLIC_KEY=<your_public_key>
LANGFUSE_HOST=https://localhost:3000
```

## 🔍 Project Structure

```
llmops-project/
│
├── documents/
│   ├── dracula.pdf
│
├── notebooks/
│   ├── langfuse-gemini.py
│   ├── ragfuse-langchain-tracing.py
│
├── src/
│   └── img/
│       ├── langfuse_logo.png
│   ├── main.py
│   ├── rag_utils.py
│
├── configs/
│   └── config.yaml
│
├── docker-compose.yml
│
├── langfuse_run.sh
│
├── README.md
│
└── .env
```

## 🧪 Getting Started

### Running the Application

```bash
python src/main.py
```
## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📈 Monitoring & Observability

Utilize Langfuse dashboard to:
- Track model performance
- Analyze trace details
- Monitor prompt variations
- Evaluate model outputs

## 🔒 Security

Ensure all sensitive credentials are stored in `.env` and never committed to version control.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

Project Link: [https://github.com/nachojeda/RagFuse.git](https://github.com/nachojeda/RagFuse.git)


