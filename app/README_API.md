# DebtSage REST API

**AI-Powered African Sovereign Debt Crisis Prediction API**

---

## Overview

The DebtSage API provides REST endpoints for integrating the ML-powered debt crisis prediction system into any application. Your frontend developers can use these endpoints to build custom dashboards, mobile apps, or integrate into existing systems.

**Base URL:** `http://localhost:8000`  
**Interactive Docs:** http://localhost:8000/docs  
**API Version:** 1.0.0

---

## Quick Start

### 1. Start the API Server

```bash
# From project root
python app/api.py
```

The server will start at http://localhost:8000 with:
- ✅ 3 ML models loaded (XGBoost, Random Forest, Logistic Regression)
- ✅ 8 data files loaded (panel data, risk scores, metrics, etc.)
- ✅ CORS enabled for cross-origin requests
- ✅ Interactive documentation at /docs

### 2. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Get countries
curl http://localhost:8000/countries

# Make a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "debt_to_gdp": 65.0,
    "deficit_to_gdp": -3.5,
    "revenue_to_gdp": 18.5,
    "inflation_rate": 5.2,
    "gdp_growth": 3.8,
    "external_debt_ratio": 45.0,
    "debt_service_to_revenue": 25.0,
    "reserves_months": 4.5,
    "primary_balance": -1.2,
    "exchange_rate_change": 2.1,
    "model": "xgboost"
  }'
```

### 3. Run Test Suite

```bash
# Run automated tests
python app/test_api.py
```

---

## API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info & available endpoints |
| `/health` | GET | Health check (models & data loaded) |
| `/predict` | POST | **Single debt crisis prediction** |
| `/predict/batch` | POST | Batch predictions (multiple at once) |
| `/countries` | GET | List all available countries |
| `/country/{country}` | GET | Historical data for specific country |
| `/risk-scores` | GET | ML risk scores for all countries |
| `/model/performance` | GET | Model evaluation metrics |
| `/model/feature-importance` | GET | Top risk predictors ranking |
| `/fiscal/metrics` | GET | Fiscal sustainability metrics |
| `/fiscal/scorecard` | GET | Fiscal health scorecard & rankings |
| `/projections/{country}` | GET | 5-year debt projections (3 scenarios) |
| `/stats/summary` | GET | Dataset summary statistics |

---

## Key Features

### 🤖 ML Predictions
- **3 Models Available:** XGBoost (93.4% accuracy), Random Forest, Logistic Regression
- **Real-time Inference:** <100ms response time
- **Batch Processing:** Multiple predictions in one request
- **Risk Levels:** Low, Medium, High (with confidence scores)

### 📊 Data Access
- **14 African Countries:** Comprehensive coverage
- **623 Observations:** Historical data (1960-2025)
- **26 Indicators:** Debt, deficit, revenue, inflation, GDP growth, etc.
- **Time Series:** Filter by year range

### 📈 Analytics
- **Risk Scores:** ML-generated crisis probabilities
- **Fiscal Metrics:** Debt sustainability, revenue efficiency
- **Projections:** 5-year forecasts (baseline, optimistic, stress)
- **Rankings:** Country comparisons and fiscal health scores

---

## Integration Examples

### JavaScript/TypeScript (React/Next.js)

```javascript
// Make a prediction
async function predictDebtRisk(indicators) {
  const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      debt_to_gdp: indicators.debt,
      deficit_to_gdp: indicators.deficit,
      revenue_to_gdp: indicators.revenue,
      inflation_rate: indicators.inflation,
      gdp_growth: indicators.growth,
      external_debt_ratio: indicators.externalDebt,
      debt_service_to_revenue: indicators.debtService,
      reserves_months: indicators.reserves,
      primary_balance: indicators.primaryBalance,
      exchange_rate_change: indicators.exchangeRate,
      model: 'xgboost'
    })
  });
  
  return await response.json();
}

// Get country data
async function getCountryData(country, startYear) {
  const url = `http://localhost:8000/country/${country}?start_year=${startYear}`;
  const response = await fetch(url);
  return await response.json();
}

// Usage in component
const result = await predictDebtRisk({
  debt: 65.0,
  deficit: -3.5,
  revenue: 18.5,
  inflation: 5.2,
  growth: 3.8,
  externalDebt: 45.0,
  debtService: 25.0,
  reserves: 4.5,
  primaryBalance: -1.2,
  exchangeRate: 2.1
});

console.log(`Risk Score: ${result.risk_score}%`);
console.log(`Risk Level: ${result.risk_level}`);
```

### Python

```python
import requests

# Make a prediction
response = requests.post('http://localhost:8000/predict', json={
    'debt_to_gdp': 65.0,
    'deficit_to_gdp': -3.5,
    'revenue_to_gdp': 18.5,
    'inflation_rate': 5.2,
    'gdp_growth': 3.8,
    'external_debt_ratio': 45.0,
    'debt_service_to_revenue': 25.0,
    'reserves_months': 4.5,
    'primary_balance': -1.2,
    'exchange_rate_change': 2.1,
    'model': 'xgboost'
})

result = response.json()
print(f"Risk Score: {result['risk_score']}%")
print(f"Risk Level: {result['risk_level']}")
```

---

## Response Formats

### Prediction Response
```json
{
  "risk_score": 42.35,
  "risk_level": "Medium",
  "risk_prediction": 0,
  "confidence": 84.70,
  "model_used": "xgboost"
}
```

### Country Data Response
```json
{
  "country": "Togo",
  "records": [
    {
      "country": "Togo",
      "year": 2020,
      "debt_to_gdp": 62.3,
      "deficit_to_gdp": -2.1,
      ...
    }
  ],
  "count": 10,
  "year_range": {"min": 2020, "max": 2023}
}
```

### Risk Scores Response
```json
{
  "risk_scores": [
    {
      "country": "Nigeria",
      "year": 2023,
      "risk_score": 98.5,
      "risk_prediction": 1
    }
  ],
  "count": 14
}
```

---

## Error Handling

All endpoints return standard HTTP status codes:

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 404 | Not Found (country/resource not found) |
| 500 | Internal Server Error |

**Error Response Format:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

**Example Error Handling (JavaScript):**
```javascript
try {
  const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  
  return await response.json();
  
} catch (error) {
  console.error('API Error:', error.message);
}
```

---

## Documentation Files

| File | Description |
|------|-------------|
| `API_DOCUMENTATION.md` | **Complete API reference** with all endpoints, examples, and integration guides |
| `API_QUICKSTART.md` | Quick reference guide with essential commands |
| `README_API.md` | This file - Overview and getting started |
| `test_api.py` | Automated test suite for all endpoints |

---

## CORS Configuration

The API is configured to accept requests from any origin during development:

```python
allow_origins=["*"]  # Accept all origins
```

**For production**, update the CORS settings in `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://dashboard.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Performance

- **Startup Time:** 2-3 seconds (models loaded once)
- **Prediction Latency:** <100ms per prediction
- **Batch Processing:** <500ms for 10 predictions
- **Concurrent Requests:** Supports multiple simultaneous users
- **Memory Usage:** ~500MB (models + data cached)

---

## Production Deployment

### Using Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t debtsage-api .
docker run -p 8000:8000 debtsage-api
```

### Using Gunicorn

```bash
pip install gunicorn
gunicorn app.api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## Support

- **Interactive Docs:** http://localhost:8000/docs (when server is running)
- **GitHub:** github.com/Techdee1/10Analytics
- **Complete Documentation:** See `API_DOCUMENTATION.md`

---

## What Your Engineer Needs

Share these items with your software engineer:

1. ✅ **API Base URL:** http://localhost:8000
2. ✅ **Interactive Docs:** http://localhost:8000/docs
3. ✅ **Documentation:** `app/API_DOCUMENTATION.md`
4. ✅ **Quick Reference:** `app/API_QUICKSTART.md`
5. ✅ **Test Suite:** `app/test_api.py`

They can start building immediately by:
1. Starting the API server (`python app/api.py`)
2. Exploring endpoints in the interactive docs
3. Making test requests to understand responses
4. Integrating endpoints into their frontend

---

**Last Updated:** November 29, 2025  
**Version:** 1.0.0  
**Status:** ✅ Production Ready
