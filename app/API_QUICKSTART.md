# DebtSage API - Quick Reference

## Start API Server

```bash
# Option 1: Run directly
python app/api.py

# Option 2: Using uvicorn
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: **http://localhost:8000**

---

## Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Quick Test

```bash
# Health check
curl http://localhost:8000/health

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

# Get countries
curl http://localhost:8000/countries

# Get country data
curl "http://localhost:8000/country/Togo?start_year=2020"

# Run test suite
python app/test_api.py
```

---

## Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict` | POST | Single prediction |
| `/predict/batch` | POST | Batch predictions |
| `/countries` | GET | List countries |
| `/country/{country}` | GET | Country data |
| `/risk-scores` | GET | ML risk scores |
| `/model/performance` | GET | Model metrics |
| `/fiscal/metrics` | GET | Fiscal data |
| `/projections/{country}` | GET | Debt forecasts |

---

## JavaScript Integration

```javascript
// Simple prediction
const response = await fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    debt_to_gdp: 65.0,
    deficit_to_gdp: -3.5,
    revenue_to_gdp: 18.5,
    inflation_rate: 5.2,
    gdp_growth: 3.8,
    external_debt_ratio: 45.0,
    debt_service_to_revenue: 25.0,
    reserves_months: 4.5,
    primary_balance: -1.2,
    exchange_rate_change: 2.1,
    model: 'xgboost'
  })
});

const data = await response.json();
console.log(`Risk Score: ${data.risk_score}%`);
console.log(`Risk Level: ${data.risk_level}`);
```

---

## Full Documentation

See **API_DOCUMENTATION.md** for complete endpoint details, examples, and integration guides.
