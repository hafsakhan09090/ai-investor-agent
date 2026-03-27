# MCP-Integrated Multi-Agent Stock Analysis System for Indian Investors

## 🎯 Google Cloud Gen AI Academy - Track 2 (MCP)

This project demonstrates a production-ready AI agent system that uses **Model Context Protocol (MCP)** to connect to real-world financial data tools and provide investment insights.

## 🏆 Key Features

### MCP Integration (Track 2 Requirement)
- ✅ **6+ MCP Tools**: Stock info, historical data, technical indicators, sentiment analysis, investment signals
- ✅ **External Data Connection**: Uses yfinance API via MCP for real-time market data
- ✅ **Structured Data Retrieval**: Fetches and processes financial data
- ✅ **Response Generation**: Gemini-powered analysis with investment recommendations

### Multi-Agent Architecture
- **Coordinator Agent**: Orchestrates 7+ autonomous steps
- **Data Collector Agent**: Fetches data via MCP tools
- **Analysis Agent**: Technical & sentiment analysis
- **Report Agent**: Generates human-readable insights

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))
- Google Cloud Account (for deployment)

### Local Development

1. **Clone and Setup**
```bash
git clone https://github.com/YOUR_USERNAME/mcp-stock-advisor.git
cd mcp-stock-advisor
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
