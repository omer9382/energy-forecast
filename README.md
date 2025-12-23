# ⚡ Energy Load Forecasting System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Azure Functions](https://img.shields.io/badge/Azure-Functions-0078D4.svg)](https://azure.microsoft.com/en-us/services/functions/)
[![Cosmos DB](https://img.shields.io/badge/Azure-Cosmos%20DB-0078D4.svg)](https://azure.microsoft.com/en-us/services/cosmos-db/)
[![Machine Learning](https://img.shields.io/badge/ML-Time%20Series-green.svg)](https://en.wikipedia.org/wiki/Time_series)

> A production-ready serverless machine learning system for predicting electrical energy consumption using time series analysis and custom gradient descent implementation.

## 🎯 Project Overview

This project implements an end-to-end machine learning solution for forecasting electrical energy load at both hourly and daily granularity. The system leverages serverless cloud architecture (Azure Functions) for scalable, cost-effective predictions, combined with a custom-built linear regression model optimized for time series forecasting.

### Key Achievements

- **Custom ML Implementation**: Built linear regression from scratch using NumPy with gradient descent optimization
- **Serverless Architecture**: Deployed on Azure Functions for automatic scaling and cost optimization
- **Real-time API**: RESTful endpoints for on-demand predictions (hourly & daily forecasts)
- **Feature Engineering**: Sophisticated temporal feature extraction including lag features, rolling windows, and seasonal patterns
- **Cloud-Native**: Full integration with Azure Cosmos DB for persistent storage and model state management

## 🚀 Technical Skills Demonstrated

### Machine Learning & Data Science
- **Time Series Forecasting**: Advanced techniques for temporal data prediction
- **Feature Engineering**: Lag features (1hr, 24hr, 168hr), rolling averages, seasonality detection
- **Custom Algorithm Implementation**: Gradient descent optimization with normalization
- **Model Persistence**: Serialization and deserialization of trained models
- **Predictive Analytics**: Multi-horizon forecasting (hourly and daily predictions)

### Cloud & DevOps
- **Azure Functions**: Serverless compute for scalable deployments
- **Azure Cosmos DB**: NoSQL database for high-throughput data operations
- **RESTful API Design**: HTTP triggers with JSON request/response handling
- **Timer Triggers**: Automated model retraining on schedule
- **Environment Management**: Secure credential handling with environment variables

### Software Engineering
- **Object-Oriented Design**: Clean architecture with separation of concerns
- **Python Best Practices**: Type hints, error handling, logging
- **Modular Code Structure**: Reusable components (DataLoader, FE, LinearRegression, Serializer)
- **Data Pipeline Development**: ETL processes for CSV to database ingestion
- **API Development**: Production-ready endpoints with validation and error handling

### Data Engineering
- **Data Transformation**: Pandas-based ETL pipelines
- **Database Operations**: CRUD operations with Cosmos DB SDK
- **CSV Processing**: Efficient data ingestion from external sources
- **Data Normalization**: Z-score standardization for model training

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Energy Forecast System                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────────┐         ┌───────────┐
│  CSV Data    │────────>│  Data Ingestion  │────────>│  Cosmos   │
│  Sources     │         │  (script.py)     │         │    DB     │
└──────────────┘         └──────────────────┘         └─────┬─────┘
                                                              │
                         ┌────────────────────────────────────┤
                         │                                    │
                         ▼                                    ▼
              ┌──────────────────────┐          ┌─────────────────────┐
              │  Model Training      │          │   Prediction API    │
              │  (Timer Trigger)     │          │  (HTTP Trigger)     │
              │  - train_model       │          │  - predict (hours)  │
              │  - train_model_days  │          │  - predict_days     │
              └──────────┬───────────┘          └──────────┬──────────┘
                         │                                  │
                         │    Model State (w,b,std,mean)   │
                         └──────────────┬───────────────────┘
                                        │
                                        ▼
                              ┌─────────────────┐
                              │   Cosmos DB     │
                              │  (Model State)  │
                              └─────────────────┘
```

## 📊 Features & Capabilities

### 1. **Hourly Load Forecasting**
Predict energy consumption at hourly intervals using:
- **Temporal Features**: Hour of day, day of week, month, weekend indicator
- **Lag Features**: 1-hour, 24-hour (same hour yesterday), 168-hour (same hour last week)
- **Rolling Statistics**: 24-hour moving average for trend capture

### 2. **Daily Load Forecasting**
Aggregate predictions at daily granularity with:
- **Daily Lags**: 1-day, 7-day (weekly cycle), 30-day (monthly cycle)
- **Weekly Rolling Average**: 7-day trend analysis
- **Seasonal Patterns**: Weekend vs. weekday, monthly variations

### 3. **Automated Model Training**
- Timer-triggered retraining for model freshness
- Automatic model state persistence to Cosmos DB
- Separate models for hourly and daily predictions

### 4. **RESTful API Interface**

#### Predict Hourly Load
```http
POST /api/predict
Content-Type: application/json

{
  "hours": 24
}
```

**Response**: Array of predictions with timestamps and load values

#### Predict Daily Load
```http
POST /api/predict_days
Content-Type: application/json

{
  "days": 7
}
```

**Response**: Array of daily predictions with timestamps and load values

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Programming** | Python 3.9+ |
| **ML/Data Science** | NumPy, Pandas |
| **Cloud Platform** | Microsoft Azure |
| **Compute** | Azure Functions (Serverless) |
| **Database** | Azure Cosmos DB (NoSQL) |
| **API** | Azure Functions HTTP Triggers |
| **Scheduling** | Azure Functions Timer Triggers |
| **Configuration** | python-dotenv |

## 📦 Project Structure

```
energy-forecast/
├── models/
│   ├── DataLoader.py          # Data transformation to DataFrame
│   ├── FE.py                  # Feature engineering (temporal features)
│   ├── LinearRegression.py    # Custom ML model with gradient descent
│   └── serializer.py          # Prediction serialization
├── repository/
│   └── cosmos_repo.py         # Cosmos DB operations
├── train_model/
│   └── __init__.py            # Hourly model training (Timer trigger)
├── train_model2/
│   └── train_model_days.py    # Daily model training (Timer trigger)
├── predict/
│   └── __init__.py            # Hourly prediction API (HTTP trigger)
├── predict_days/
│   └── __init__.py            # Daily prediction API (HTTP trigger)
├── script.py                  # CSV data ingestion utility
└── requirements.txt           # Python dependencies
```

## 🔧 Implementation Highlights

### Custom Linear Regression Model

The `LinearRegression` class implements gradient descent optimization from scratch:

```python
# Features used for training
- Normalization: Z-score standardization (μ=0, σ=1)
- Optimization: Batch gradient descent
- Learning rate: 0.1 (adaptive)
- Iterations: 2000 epochs
- Cost function: Mean Squared Error (MSE)
```

**Key Methods**:
- `compute_cost()`: Train model using gradient descent
- `predict()`: Single-point prediction with lag feature calculation
- `forecast()`: Multi-step ahead forecasting with recursive prediction
- `load()`: Restore trained model from persisted state

### Feature Engineering Pipeline

The `FE` (Feature Engineering) class transforms raw timestamps into predictive features:

**Temporal Features**:
- `hours`: Hour of day (0-23) - captures daily patterns
- `day_of_week`: Day index (0-6) - captures weekly cycles
- `month`: Month (1-12) - captures seasonal variations
- `is_weekend`: Binary flag - differentiates weekday/weekend consumption

**Lag Features** (captures historical patterns):
- `lag_1`: Previous hour/day value
- `lag_24` / `lag_7`: Same time yesterday/last week
- `lag_168` / `lag_30`: Weekly/monthly historical reference

**Rolling Statistics** (smooths noise, captures trends):
- `rolling_24` / `rolling_7`: Moving average over window

### Data Pipeline

1. **Ingestion** (`script.py`): CSV → Cosmos DB with UUID generation
2. **Loading** (`DataLoader`): Cosmos DB items → Pandas DataFrame
3. **Feature Engineering** (`FE`): Raw data → Feature-rich dataset
4. **Training** (`train_model`): Features → Trained model parameters
5. **Prediction** (`predict`): New timestamps → Load forecasts

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Azure subscription
- Azure Functions Core Tools
- Azure Cosmos DB account

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/omer9382/energy-forecast.git
cd energy-forecast
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file:
```env
COSMOS_URL=your_cosmos_db_url
COSMOS_KEY=your_cosmos_db_key
COSMOS_DATABASE=your_database_name
COSMOS_CONTAINER=your_data_container
COSMOS_CONTAINER2=your_model_state_container
COSMOS_CONTAINER3=your_daily_model_container
```

4. **Load initial data**
```bash
python script.py
```

### Local Development

```bash
# Start Azure Functions locally
func start

# Test prediction endpoint
curl -X POST http://localhost:7071/api/predict \
  -H "Content-Type: application/json" \
  -d '{"hours": 24}'
```

### Deployment to Azure

```bash
# Login to Azure
az login

# Create Function App
az functionapp create \
  --resource-group <resource-group> \
  --consumption-plan-location <location> \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4 \
  --name <app-name> \
  --storage-account <storage-account>

# Deploy
func azure functionapp publish <app-name>
```

## 📈 Model Performance Considerations

### Training Process
- **Data Normalization**: Prevents feature scaling issues
- **Gradient Descent**: Efficient for linear models, converges in 2000 iterations
- **Feature Selection**: Domain-driven feature engineering for time series

### Prediction Strategy
- **Recursive Forecasting**: Uses own predictions as inputs for future steps
- **Lag Feature Calculation**: Dynamically computes historical references
- **Error Handling**: Graceful fallback for missing historical data

### Scalability
- **Serverless Architecture**: Auto-scales with demand
- **Stateless Functions**: Each prediction is independent
- **Persistent Models**: Model state stored separately from compute

## 💡 Use Cases

1. **Energy Grid Management**: Optimize power generation scheduling
2. **Demand Response Planning**: Predict peak load times for load balancing
3. **Cost Optimization**: Forecast energy costs for budget planning
4. **Infrastructure Planning**: Identify capacity requirements
5. **Renewable Integration**: Plan solar/wind energy storage needs

## 🔐 Security Features

- Environment-based configuration (no hardcoded credentials)
- Azure Key Vault integration capability
- HTTPS-only API endpoints
- Cosmos DB authentication with access keys
- Input validation and error handling

## 📚 Key Learnings & Best Practices

1. **Feature Engineering is Critical**: Domain knowledge in energy patterns (daily/weekly cycles) significantly improves predictions
2. **Normalization Matters**: Z-score standardization prevents gradient descent instability
3. **Serverless for ML**: Azure Functions provides cost-effective deployment for inference workloads
4. **Model Persistence**: Separating model training from prediction enables independent scaling
5. **Recursive Forecasting**: Multi-step predictions require careful handling of lag features

## 🎓 Skills Showcase

This project demonstrates proficiency in:

✅ **Machine Learning**: Time series forecasting, gradient descent, feature engineering  
✅ **Cloud Computing**: Azure Functions, Cosmos DB, serverless architecture  
✅ **Python Development**: NumPy, Pandas, object-oriented design  
✅ **API Development**: RESTful services, HTTP triggers, JSON handling  
✅ **Data Engineering**: ETL pipelines, data transformation, database operations  
✅ **DevOps**: Cloud deployment, environment configuration, monitoring  
✅ **Software Architecture**: Modular design, separation of concerns, scalability  

## 📧 Contact & Professional Links

**Portfolio**: Demonstrate this project in your data science portfolio  
**LinkedIn**: Highlight skills in Machine Learning, Cloud Computing, Python, Azure, Time Series Analysis  
**GitHub**: Showcase clean, production-ready code with best practices  

---

**⭐ If you found this project impressive, please star the repository!**

*Built with passion for solving real-world energy challenges through machine learning and cloud technology.*
