# 🛡️ DealSentry BD

> **Bangladesh Marketplace Deal Scanner** — Scan, compare, and verify deals across Daraz, Pickaboo, Chaldal & more with AI-powered risk analysis.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org)
[![Tailwind](https://img.shields.io/badge/Tailwind-3.4-38B2AC.svg)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

- 🔍 **Multi-Platform Price Aggregation** — Compare prices across Daraz Bangladesh, Pickaboo, Chaldal, and AjkerDeal
- 🧠 **Smart Risk Scoring Engine (0-100%)** — Weighted analysis across 5 factors:
  - Price Reality (30%) — Flags "too good to be true" deals
  - Seller Trust (25%) — Reviews, ratings, verification
  - Return Policy (15%) — Refund protection check
  - Warranty (15%) — Official vs. shop vs. none
  - Platform Safety (15%) — Buyer protection levels
- 🎯 **Buy Recommendation Engine** — STRONG BUY → BUY → CAUTIOUS BUY → NOT RECOMMENDED → AVOID
- 📊 **Visual Price Comparison** — Color-coded bars showing price spread across platforms
- 🏠 **Bangladesh-Specific** — BDT (৳) currency, local brands (Walton, Symphony, Marcel), local pricing psychology
- 🌙 **Dark-Themed Dashboard** — Clean, responsive UI built with React + Tailwind CSS
- ⚡ **Real-Time Filtering** — Search, sort, and filter by category, platform, price, risk, and savings

---

## 🖼️ Screenshots

| Dashboard | Product Card | Risk Analysis |
|-----------|-------------|---------------|
| Stats cards, filters, deal list | Expandable cards with price bars | Risk breakdown + buy verdict |

---

## 🚀 Quick Start

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- Or: Python 3.11 + Node.js 18

### Option 1: Docker (Recommended)

```bash
git clone https://github.com/YOUR_USERNAME/dealsentry-bd.git
cd dealsentry-bd
docker-compose up --build
```

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Option 2: Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py       # Seeds 20 products + 50+ listings
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React Frontend │────▶│  FastAPI Backend │────▶│   SQLite DB     │
│  (Port 3000)     │     │  (Port 8000)     │     │  + Seed Data    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
               ┌────────┐ ┌────────┐ ┌────────┐
               │ Daraz  │ │Pickaboo│ │ Chaldal│
               │Scraper │ │Scraper │ │Scraper │
               └────────┘ └────────┘ └────────┘
```

### Risk Algorithm

```python
score = 0

# Price Reality (30%)
if price < market_avg * 0.5:  score += 30
elif price < market_avg * 0.7: score += 20
elif price < market_avg * 0.85: score += 10

# Seller Trust (25%)
if reviews < 50:     score += 15
if rating < 3.5:     score += 10
if not verified:     score += 10

# Return Policy (15%)
if not has_return:    score += 15

# Warranty (15%)
if warranty == "none": score += 15
elif warranty == "shop": score += 8

# Platform Safety (15%)
if platform == "facebook" and not verified: score += 15
if platform == "daraz" and verified:        score -= 10  # bonus
```

---

## 📁 Project Structure

```
dealsentry-bd/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI routes
│   │   ├── scrapers/      # Platform scrapers (Daraz, Pickaboo, Chaldal)
│   │   ├── config.py      # App settings
│   │   ├── database.py    # SQLAlchemy setup
│   │   ├── main.py        # FastAPI entry point
│   │   ├── models.py      # DB models
│   │   ├── risk_engine.py # Risk scoring algorithm
│   │   └── schemas.py     # Pydantic models
│   ├── Dockerfile
│   ├── requirements.txt
│   └── seed_data.py       # Demo data generator
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── App.js         # Main app
│   │   └── index.js       # Entry point
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/deals` | List all deals with risk analysis |
| GET | `/api/deals?category=Mobile+Phones&sort=lowest_risk` | Filtered deals |
| GET | `/api/stats` | Dashboard statistics |
| GET | `/api/categories` | Available categories |
| POST | `/api/scrape?query=iPhone` | Trigger live scraping |

---

## 🛡️ Scraping Ethics

- Respects `robots.txt`
- Rate-limited to 1 request per 2 seconds
- Rotating User-Agents for resilience
- Results cached for 2-4 hours
- **Facebook Marketplace** marked as experimental (requires browser automation)

---

## ⚠️ Disclaimer

> **Risk scores are algorithmic estimates. Always verify sellers independently before purchasing.**
>
> DealSentry BD is a price comparison tool only. We do not store user payment data.

---

## 📝 License

[MIT](LICENSE) — Free to use, modify, and distribute.

---

## 🙋 Support

Found a bug or have a feature request? Open an [issue](https://github.com/miraz-cd/dealsentry-bd/issues) or submit a PR!

Built with ❤️ for Bangladeshi shoppers.
