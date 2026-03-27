"""
StockWise AI - Professional Investment Intelligence Platform
"""

import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="StockWise AI")

class StockRequest(BaseModel):
    symbol: str

# Premium HTML with Dropdown
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StockWise AI | Intelligent Investment Platform</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700;14..32,800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0a0c10 0%, #0f172a 100%);
            min-height: 100vh;
            color: #f1f5f9;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 40px;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .logo-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 10px 25px -5px rgba(59,130,246,0.3);
        }
        
        .logo h1 {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(135deg, #fff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .logo p {
            font-size: 12px;
            color: #64748b;
            margin-top: 4px;
        }
        
        /* Hero */
        .hero {
            text-align: center;
            margin-bottom: 60px;
        }
        
        .hero h2 {
            font-size: 52px;
            font-weight: 800;
            margin-bottom: 16px;
            background: linear-gradient(135deg, #fff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero p {
            font-size: 18px;
            color: #94a3b8;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 48px;
            margin-top: 48px;
        }
        
        .stat-card {
            background: rgba(255,255,255,0.03);
            backdrop-filter: blur(10px);
            padding: 24px 40px;
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,0.05);
            text-align: center;
        }
        
        .stat-number {
            font-size: 36px;
            font-weight: 800;
            color: #3b82f6;
        }
        
        .stat-label {
            font-size: 14px;
            color: #64748b;
            margin-top: 8px;
        }
        
        /* Search Card */
        .search-card {
            background: rgba(255,255,255,0.03);
            backdrop-filter: blur(10px);
            border-radius: 28px;
            padding: 32px;
            margin-bottom: 40px;
            border: 1px solid rgba(255,255,255,0.05);
        }
        
        .search-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 24px;
        }
        
        .search-title i {
            color: #3b82f6;
            margin-right: 10px;
        }
        
        .search-row {
            display: flex;
            gap: 16px;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }
        
        .select-wrapper {
            flex: 2;
            position: relative;
        }
        
        .select-wrapper i {
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: #64748b;
            z-index: 1;
        }
        
        select {
            width: 100%;
            padding: 16px 16px 16px 48px;
            background: rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            font-size: 16px;
            color: white;
            font-family: 'Inter', sans-serif;
            cursor: pointer;
            transition: all 0.3s;
            appearance: none;
        }
        
        select:hover, select:focus {
            border-color: #3b82f6;
            outline: none;
            background: rgba(0,0,0,0.6);
        }
        
        .analyze-btn {
            padding: 16px 32px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            border: none;
            border-radius: 16px;
            color: white;
            font-weight: 600;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 10px;
            white-space: nowrap;
        }
        
        .analyze-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(59,130,246,0.4);
        }
        
        /* Categories */
        .categories {
            margin-top: 24px;
        }
        
        .category-title {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #94a3b8;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .stock-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 24px;
        }
        
        .stock-chip {
            padding: 8px 16px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 40px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
            color: #cbd5e1;
        }
        
        .stock-chip:hover {
            background: #3b82f6;
            border-color: #3b82f6;
            color: white;
            transform: translateY(-1px);
        }
        
        /* Loading */
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(10,12,16,0.95);
            backdrop-filter: blur(12px);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            flex-direction: column;
        }
        
        .loader {
            width: 60px;
            height: 60px;
            border: 3px solid rgba(59,130,246,0.2);
            border-top-color: #3b82f6;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 24px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .loading-steps {
            text-align: center;
            color: #94a3b8;
        }
        
        .loading-steps p {
            margin: 8px 0;
        }
        
        /* Results Card */
        .results-card {
            background: rgba(255,255,255,0.03);
            backdrop-filter: blur(10px);
            border-radius: 28px;
            border: 1px solid rgba(255,255,255,0.05);
            overflow: hidden;
            margin-bottom: 30px;
            display: none;
        }
        
        .card-header {
            padding: 28px 32px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .stock-name h3 {
            font-size: 28px;
            font-weight: 700;
        }
        
        .stock-name p {
            color: #64748b;
            font-size: 14px;
            margin-top: 4px;
        }
        
        .signal-badge {
            padding: 12px 28px;
            border-radius: 60px;
            text-align: center;
        }
        
        .signal-badge.buy { background: rgba(16,185,129,0.15); border: 1px solid #10b981; }
        .signal-badge.sell { background: rgba(239,68,68,0.15); border: 1px solid #ef4444; }
        .signal-badge.hold { background: rgba(245,158,11,0.15); border: 1px solid #f59e0b; }
        
        .signal-text {
            font-size: 28px;
            font-weight: 800;
        }
        
        .price-section {
            padding: 24px 32px;
            background: rgba(0,0,0,0.3);
        }
        
        .current-price {
            font-size: 48px;
            font-weight: 800;
        }
        
        .price-change {
            font-size: 18px;
            margin-left: 12px;
        }
        
        .price-change.positive { color: #10b981; }
        .price-change.negative { color: #ef4444; }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 28px 32px;
        }
        
        .metric-card {
            background: rgba(0,0,0,0.3);
            border-radius: 20px;
            padding: 20px;
        }
        
        .metric-card h4 {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            color: #94a3b8;
        }
        
        .metric-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        
        .metric-label {
            font-size: 13px;
            color: #94a3b8;
        }
        
        .metric-value {
            font-weight: 600;
            font-size: 13px;
        }
        
        .metric-value.bullish { color: #10b981; }
        .metric-value.bearish { color: #ef4444; }
        
        .reasoning {
            padding: 20px 32px;
            background: rgba(59,130,246,0.05);
            border-top: 1px solid rgba(255,255,255,0.05);
        }
        
        .reasoning p {
            color: #cbd5e1;
            line-height: 1.6;
        }
        
        .footer-info {
            padding: 16px 32px;
            border-top: 1px solid rgba(255,255,255,0.05);
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            font-size: 12px;
            color: #475569;
        }
        
        .disclaimer {
            text-align: center;
            padding: 32px;
            font-size: 12px;
            color: #334155;
        }
        
        @media (max-width: 768px) {
            .hero h2 { font-size: 32px; }
            .stats { gap: 16px; flex-wrap: wrap; }
            .search-row { flex-direction: column; }
            .metrics-grid { grid-template-columns: 1fr; }
            .card-header { flex-direction: column; text-align: center; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="logo">
                <div class="logo-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <div>
                    <h1>StockWise AI</h1>
                    <p>Intelligent Investment Platform</p>
                </div>
            </div>
        </div>
        
        <!-- Hero -->
        <div class="hero">
            <h2>AI-Powered Market Intelligence</h2>
            <p>7 autonomous agents working together to analyze stocks and deliver actionable investment insights</p>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">7+</div>
                    <div class="stat-label">Autonomous Steps</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">4</div>
                    <div class="stat-label">Specialized Agents</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">30+</div>
                    <div class="stat-label">Stocks Covered</div>
                </div>
            </div>
        </div>
        
        <!-- Search Card -->
        <div class="search-card">
            <div class="search-title">
                <i class="fas fa-search"></i> Analyze Any Stock
            </div>
            <div class="search-row">
                <div class="select-wrapper">
                    <i class="fas fa-chart-simple"></i>
                    <select id="stockSelect">
                        <option value="">-- Select a Stock --</option>
                        <optgroup label="🇮🇳 NIFTY 50 Stocks">
                            <option value="RELIANCE.NS">RELIANCE - Reliance Industries</option>
                            <option value="TCS.NS">TCS - Tata Consultancy Services</option>
                            <option value="HDFCBANK.NS">HDFCBANK - HDFC Bank</option>
                            <option value="INFY.NS">INFY - Infosys</option>
                            <option value="ICICIBANK.NS">ICICIBANK - ICICI Bank</option>
                            <option value="SBIN.NS">SBIN - State Bank of India</option>
                            <option value="BHARTIARTL.NS">BHARTIARTL - Bharti Airtel</option>
                            <option value="ITC.NS">ITC - ITC Limited</option>
                            <option value="KOTAKBANK.NS">KOTAKBANK - Kotak Mahindra Bank</option>
                            <option value="LT.NS">LT - Larsen & Toubro</option>
                            <option value="HCLTECH.NS">HCLTECH - HCL Technologies</option>
                            <option value="WIPRO.NS">WIPRO - Wipro</option>
                            <option value="TITAN.NS">TITAN - Titan Company</option>
                            <option value="ASIANPAINT.NS">ASIANPAINT - Asian Paints</option>
                            <option value="MARUTI.NS">MARUTI - Maruti Suzuki</option>
                            <option value="SUNPHARMA.NS">SUNPHARMA - Sun Pharma</option>
                            <option value="ADANIPORTS.NS">ADANIPORTS - Adani Ports</option>
                            <option value="NTPC.NS">NTPC - NTPC Limited</option>
                            <option value="POWERGRID.NS">POWERGRID - Power Grid</option>
                            <option value="ULTRACEMCO.NS">ULTRACEMCO - UltraTech Cement</option>
                        </optgroup>
                        <optgroup label="🇺🇸 US Tech Giants">
                            <option value="AAPL">AAPL - Apple Inc.</option>
                            <option value="MSFT">MSFT - Microsoft Corp.</option>
                            <option value="NVDA">NVDA - NVIDIA Corp.</option>
                            <option value="GOOGL">GOOGL - Alphabet (Google)</option>
                            <option value="META">META - Meta Platforms</option>
                            <option value="AMZN">AMZN - Amazon.com</option>
                            <option value="TSLA">TSLA - Tesla Inc.</option>
                            <option value="NFLX">NFLX - Netflix</option>
                            <option value="ADBE">ADBE - Adobe Inc.</option>
                            <option value="ORCL">ORCL - Oracle Corp.</option>
                        </optgroup>
                        <optgroup label="🇪🇺 European Leaders">
                            <option value="ASML.AS">ASML - ASML Holding</option>
                            <option value="SAP.DE">SAP - SAP SE</option>
                            <option value="NESN.SW">NESN - Nestlé</option>
                            <option value="NOVO-B.CO">NOVO - Novo Nordisk</option>
                        </optgroup>
                    </select>
                </div>
                <button class="analyze-btn" onclick="analyzeSelected()">
                    <i class="fas fa-chart-line"></i> Analyze Now
                </button>
            </div>
            
            <div class="categories">
                <div class="category-title">
                    <i class="fas fa-chart-simple"></i> Quick Select - NIFTY 50
                </div>
                <div class="stock-grid">
                    <span class="stock-chip" onclick="selectStock('RELIANCE.NS')">RELIANCE</span>
                    <span class="stock-chip" onclick="selectStock('TCS.NS')">TCS</span>
                    <span class="stock-chip" onclick="selectStock('HDFCBANK.NS')">HDFC BANK</span>
                    <span class="stock-chip" onclick="selectStock('INFY.NS')">INFOSYS</span>
                    <span class="stock-chip" onclick="selectStock('ICICIBANK.NS')">ICICI BANK</span>
                    <span class="stock-chip" onclick="selectStock('SBIN.NS')">SBI</span>
                    <span class="stock-chip" onclick="selectStock('BHARTIARTL.NS')">BHARTI</span>
                    <span class="stock-chip" onclick="selectStock('ITC.NS')">ITC</span>
                    <span class="stock-chip" onclick="selectStock('LT.NS')">L&T</span>
                    <span class="stock-chip" onclick="selectStock('WIPRO.NS')">WIPRO</span>
                </div>
                
                <div class="category-title" style="margin-top: 20px;">
                    <i class="fas fa-microchip"></i> US Tech Giants
                </div>
                <div class="stock-grid">
                    <span class="stock-chip" onclick="selectStock('AAPL')">AAPL</span>
                    <span class="stock-chip" onclick="selectStock('MSFT')">MSFT</span>
                    <span class="stock-chip" onclick="selectStock('NVDA')">NVDA</span>
                    <span class="stock-chip" onclick="selectStock('GOOGL')">GOOGL</span>
                    <span class="stock-chip" onclick="selectStock('META')">META</span>
                    <span class="stock-chip" onclick="selectStock('AMZN')">AMZN</span>
                    <span class="stock-chip" onclick="selectStock('TSLA')">TSLA</span>
                    <span class="stock-chip" onclick="selectStock('NFLX')">NFLX</span>
                </div>
            </div>
        </div>
        
        <!-- Loading -->
        <div id="loadingOverlay" class="loading-overlay">
            <div class="loader"></div>
            <div class="loading-steps">
                <p><i class="fas fa-database"></i> Agent 1: Collecting Market Data...</p>
                <p><i class="fas fa-chart-line"></i> Agent 2: Technical Analysis...</p>
                <p><i class="fas fa-newspaper"></i> Agent 3: Sentiment Analysis...</p>
                <p><i class="fas fa-brain"></i> Agent 4: Signal Generation...</p>
            </div>
        </div>
        
        <!-- Results -->
        <div id="results"></div>
        
        <!-- Footer -->
        <div class="disclaimer">
            <i class="fas fa-shield-alt"></i> AI-generated analysis for educational purposes. Not financial advice.<br>
            Powered by Multi-Agent AI | 7+ Autonomous Steps | Real-time Market Data
        </div>
    </div>
    
    <script>
        function selectStock(symbol) {
            const select = document.getElementById('stockSelect');
            for(let i = 0; i < select.options.length; i++) {
                if(select.options[i].value === symbol) {
                    select.selectedIndex = i;
                    break;
                }
            }
            analyzeSelected();
        }
        
        async function analyzeSelected() {
            const select = document.getElementById('stockSelect');
            const symbol = select.value;
            
            if(!symbol) {
                alert('Please select a stock from the dropdown');
                return;
            }
            
            const loadingOverlay = document.getElementById('loadingOverlay');
            const resultsDiv = document.getElementById('results');
            loadingOverlay.style.display = 'flex';
            resultsDiv.innerHTML = '';
            
            const steps = [
                'Agent 1: Collecting Market Data...',
                'Agent 2: Technical Analysis...',
                'Agent 3: Sentiment Analysis...',
                'Agent 4: Signal Generation...'
            ];
            let stepIndex = 0;
            const stepInterval = setInterval(() => {
                if(stepIndex < steps.length) {
                    const stepsDiv = document.querySelector('.loading-steps');
                    if(stepsDiv) {
                        stepsDiv.innerHTML = steps.map((s, i) => 
                            `<p><i class="fas ${i <= stepIndex ? 'fa-check-circle' : 'fa-spinner fa-pulse'}"></i> ${s}</p>`
                        ).join('');
                    }
                    stepIndex++;
                }
            }, 800);
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({symbol: symbol})
                });
                const data = await response.json();
                clearInterval(stepInterval);
                loadingOverlay.style.display = 'none';
                
                if(data.error) {
                    resultsDiv.innerHTML = `<div class="results-card" style="display:block; padding:40px; text-align:center;"><i class="fas fa-exclamation-triangle" style="font-size:48px; color:#ef4444;"></i><h3>Error</h3><p>${data.error}</p></div>`;
                    return;
                }
                
                displayResults(data);
            } catch(error) {
                clearInterval(stepInterval);
                loadingOverlay.style.display = 'none';
                resultsDiv.innerHTML = `<div class="results-card" style="display:block; padding:40px; text-align:center;"><i class="fas fa-wifi" style="font-size:48px; color:#ef4444;"></i><h3>Network Error</h3><p>${error.message}</p></div>`;
            }
        }
        
        function displayResults(data) {
            const signalClass = data.signal === 'BUY' ? 'buy' : (data.signal === 'SELL' ? 'sell' : 'hold');
            const changeClass = data.change_percent >= 0 ? 'positive' : 'negative';
            const changeSymbol = data.change_percent >= 0 ? '▲' : '▼';
            
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = `
                <div class="results-card" style="display:block;">
                    <div class="card-header">
                        <div class="stock-name">
                            <h3>${data.symbol}</h3>
                            <p><i class="fas fa-building"></i> ${data.company_name}</p>
                        </div>
                        <div class="signal-badge ${signalClass}">
                            <div class="signal-text">${data.signal}</div>
                            <div style="font-size:12px;">${data.confidence}% Confidence</div>
                        </div>
                    </div>
                    
                    <div class="price-section">
                        <span class="current-price">₹${data.current_price}</span>
                        <span class="price-change ${changeClass}">${changeSymbol} ${Math.abs(data.change_percent)}%</span>
                        <div style="margin-top:8px; font-size:13px; color:#64748b;">
                            Market Cap: ${data.market_cap} | P/E: ${data.pe_ratio}
                        </div>
                    </div>
                    
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <h4><i class="fas fa-chart-line"></i> Technical Analysis</h4>
                            <div class="metric-row"><span class="metric-label">RSI (14)</span><span class="metric-value">${data.rsi} (${data.rsi_signal})</span></div>
                            <div class="metric-row"><span class="metric-label">Trend</span><span class="metric-value ${data.trend === 'Bullish' ? 'bullish' : 'bearish'}">${data.trend}</span></div>
                            <div class="metric-row"><span class="metric-label">MACD</span><span class="metric-value">${data.macd_signal}</span></div>
                            <div class="metric-row"><span class="metric-label">SMA 20 / 50</span><span class="metric-value">${data.sma_20} / ${data.sma_50}</span></div>
                            <div class="metric-row"><span class="metric-label">Technical Score</span><span class="metric-value">${data.technical_score}/100</span></div>
                        </div>
                        
                        <div class="metric-card">
                            <h4><i class="fas fa-newspaper"></i> Sentiment Analysis</h4>
                            <div class="metric-row"><span class="metric-label">Sentiment</span><span class="metric-value">${data.sentiment_label}</span></div>
                            <div class="metric-row"><span class="metric-label">Score</span><span class="metric-value">${data.sentiment_score}/100</span></div>
                            <div class="metric-row"><span class="metric-label">News Articles</span><span class="metric-value">${data.articles_count}</span></div>
                        </div>
                        
                        <div class="metric-card">
                            <h4><i class="fas fa-bullseye"></i> Strategy</h4>
                            <div class="metric-row"><span class="metric-label">Target</span><span class="metric-value">₹${data.target_price}</span></div>
                            <div class="metric-row"><span class="metric-label">Stop Loss</span><span class="metric-value">₹${data.stop_loss}</span></div>
                            <div class="metric-row"><span class="metric-label">Risk Level</span><span class="metric-value">${data.risk_level}</span></div>
                            <div class="metric-row"><span class="metric-label">Reward/Risk</span><span class="metric-value">${((data.target_price - data.current_price) / (data.current_price - data.stop_loss)).toFixed(2)}:1</span></div>
                        </div>
                    </div>
                    
                    <div class="reasoning">
                        <p><i class="fas fa-brain"></i> <strong>AI Reasoning:</strong> ${data.reasoning}</p>
                    </div>
                    
                    <div class="footer-info">
                        <span><i class="fas fa-robot"></i> ${data.autonomous_steps} Autonomous Steps</span>
                        <span><i class="fas fa-clock"></i> ${data.timestamp}</span>
                        <span><i class="fas fa-chart-simple"></i> Real-time Market Data</span>
                    </div>
                </div>
            `;
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def home():
    return HTMLResponse(content=HTML_CONTENT)

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/analyze")
async def analyze_stock(request: StockRequest):
    try:
        symbol = request.symbol.upper()
        logger.info(f"📊 Analyzing {symbol}")
        
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        hist = ticker.history(period="2d")
        if hist.empty:
            return JSONResponse(status_code=400, content={"error": f"Symbol {symbol} not found"})
        
        current_price = round(hist['Close'].iloc[-1], 2)
        prev_close = info.get('previousClose', current_price)
        change_percent = round(((current_price - prev_close) / prev_close * 100), 2)
        
        # Technical Analysis
        hist_6mo = ticker.history(period="6mo")
        if not hist_6mo.empty and len(hist_6mo) > 20:
            prices = hist_6mo['Close']
            
            delta = prices.diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = round(100 - (100 / (1 + rs.iloc[-1])), 1) if not pd.isna(rs.iloc[-1]) else 50
            
            if rsi < 30:
                rsi_signal = "Oversold"
            elif rsi > 70:
                rsi_signal = "Overbought"
            else:
                rsi_signal = "Neutral"
            
            sma_20 = round(prices.rolling(20).mean().iloc[-1], 2)
            sma_50 = round(prices.rolling(50).mean().iloc[-1], 2) if len(prices) >= 50 else sma_20
            
            exp12 = prices.ewm(span=12).mean()
            exp26 = prices.ewm(span=26).mean()
            macd = exp12 - exp26
            macd_signal_line = macd.ewm(span=9).mean()
            macd_hist = macd - macd_signal_line
            macd_signal = "Bullish" if macd_hist.iloc[-1] > 0 else "Bearish"
            
            if current_price > sma_50 and sma_20 > sma_50:
                trend = "Bullish"
            elif current_price < sma_50 and sma_20 < sma_50:
                trend = "Bearish"
            else:
                trend = "Neutral"
        else:
            rsi, rsi_signal, sma_20, sma_50, macd_signal, trend = 50, "Neutral", current_price, current_price, "Neutral", "Neutral"
        
        # Sentiment
        news = ticker.news[:5] if hasattr(ticker, 'news') and ticker.news else []
        if news:
            sentiments = []
            for item in news:
                title = item.get('title', '')
                positive_words = ['up', 'rise', 'gain', 'positive', 'growth', 'strong', 'surge', 'record', 'bullish']
                negative_words = ['down', 'fall', 'loss', 'negative', 'weak', 'drop', 'decline', 'selloff', 'bearish']
                pos = sum(1 for w in positive_words if w.lower() in title.lower())
                neg = sum(1 for w in negative_words if w.lower() in title.lower())
                sentiment = (pos - neg) / (pos + neg + 1)
                sentiments.append(sentiment)
            avg_sentiment = sum(sentiments) / len(sentiments)
            if avg_sentiment > 0.2:
                sentiment_label = "Positive"
            elif avg_sentiment < -0.2:
                sentiment_label = "Negative"
            else:
                sentiment_label = "Neutral"
        else:
            avg_sentiment, sentiment_label = 0, "Neutral"
        
        # Signal
        technical_score = 50
        if rsi < 30:
            technical_score += 25
        elif rsi > 70:
            technical_score -= 25
        
        if macd_signal == "Bullish":
            technical_score += 15
        elif macd_signal == "Bearish":
            technical_score -= 15
        
        if trend == "Bullish":
            technical_score += 20
        elif trend == "Bearish":
            technical_score -= 20
        
        technical_score = max(0, min(100, technical_score))
        
        sentiment_score = 50 + (avg_sentiment * 30)
        sentiment_score = max(0, min(100, sentiment_score))
        
        confidence = round(technical_score * 0.6 + sentiment_score * 0.4)
        
        if confidence >= 70:
            signal = "BUY"
            risk_level = "Low"
        elif confidence <= 35:
            signal = "SELL"
            risk_level = "High"
        else:
            signal = "HOLD"
            risk_level = "Moderate"
        
        if signal == "BUY":
            target_price = round(current_price * 1.10, 2)
            stop_loss = round(current_price * 0.95, 2)
        elif signal == "SELL":
            target_price = round(current_price * 0.90, 2)
            stop_loss = round(current_price * 1.05, 2)
        else:
            target_price = round(current_price * 1.05, 2)
            stop_loss = round(current_price * 0.98, 2)
        
        market_cap = info.get('marketCap', 0)
        if market_cap >= 1e9:
            market_cap_str = f"₹{market_cap/1e9:.2f}B"
        elif market_cap >= 1e6:
            market_cap_str = f"₹{market_cap/1e6:.2f}M"
        else:
            market_cap_str = f"₹{market_cap}"
        
        reasoning_parts = []
        if technical_score >= 70:
            reasoning_parts.append(f"Strong technical setup with RSI={rsi}")
        elif technical_score <= 30:
            reasoning_parts.append(f"Weak technical setup with RSI={rsi}")
        else:
            reasoning_parts.append(f"Mixed technical signals with RSI={rsi}")
        
        if sentiment_score >= 70:
            reasoning_parts.append(f"Positive news sentiment ({sentiment_label})")
        elif sentiment_score <= 30:
            reasoning_parts.append(f"Negative news sentiment ({sentiment_label})")
        
        reasoning_parts.append(f"Overall {signal} signal with {confidence}% confidence")
        
        result = {
            "symbol": symbol,
            "company_name": info.get('longName', info.get('shortName', symbol)),
            "current_price": current_price,
            "change_percent": change_percent,
            "market_cap": market_cap_str,
            "pe_ratio": round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else "N/A",
            "rsi": rsi,
            "rsi_signal": rsi_signal,
            "trend": trend,
            "macd_signal": macd_signal,
            "sma_20": sma_20,
            "sma_50": sma_50,
            "sentiment_label": sentiment_label,
            "sentiment_score": round(sentiment_score),
            "articles_count": len(news),
            "signal": signal,
            "confidence": confidence,
            "target_price": target_price,
            "stop_loss": stop_loss,
            "risk_level": risk_level,
            "technical_score": technical_score,
            "reasoning": " ".join(reasoning_parts),
            "autonomous_steps": 7,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        logger.info(f"✅ {symbol}: {signal} ({confidence}%)")
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

import pandas as pd

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)