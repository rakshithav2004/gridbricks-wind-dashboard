# UK Wind Forecast Analysis Dashboard

A full-stack dashboard for analysing wind power generation forecasts against actual generation in Great Britain. Built to help energy analysts explore forecast errors and understand potential implications for electricity purchasing decisions.

## Overview

Wind generation forecasts can differ from actual generation. Understanding these differences can help energy analysts evaluate forecast performance and identify periods that may require further investigation.

This project retrieves wind generation data from the **Elexon BMRS API**, processes actual and forecast records, calculates forecast accuracy metrics, and presents the results through an interactive dashboard.

### Key Features

- Retrieve actual wind generation data from Elexon BMRS.
- Retrieve wind generation forecast data.
- Compare actual generation with forecast generation by hour.
- Calculate Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and forecast bias.
- Visualise actual and forecast generation using interactive charts.
- Filter results by start and end dates.
- View hourly matched records in a data table.
- Validate date ranges and handle upstream API errors.
- Test forecast analysis logic using pytest.

## Technology Stack

### Frontend
- React
- Vite
- Recharts
- JavaScript
- CSS

### Backend
- Python 3.11
- FastAPI
- HTTPX
- Uvicorn
- Pytest

### Data Source
- Elexon BMRS API

## Architecture

The application uses a frontend-backend architecture.

1. The React frontend allows users to select dates and explore the results.
2. The FastAPI backend requests data from the Elexon BMRS API.
3. The backend filters actual wind generation records and matches actual and forecast values by hour.
4. The analysis module calculates forecast accuracy metrics.
5. The frontend displays the metrics, comparison chart, and hourly records.

```text
                 Elexon BMRS API
                        |
                        v
               FastAPI Backend
                        |
             +----------+----------+
             |                     |
      Actual Generation      Wind Forecasts
             |                     |
             +----------+----------+
                        |
                        v
              Hourly Data Matching
                        |
                        v
               Accuracy Metrics
                        |
                        v
                React Dashboard
           +------------+------------+
           |            |            |
       KPI Cards    Line Chart   Hourly Table
```

## Forecast Accuracy Metrics

The dashboard calculates three metrics using matched actual and forecast values.

### Mean Absolute Error (MAE)

MAE measures the average absolute difference between actual and forecast generation.

A lower MAE indicates smaller average forecast errors.

### Root Mean Squared Error (RMSE)

RMSE gives greater weight to larger errors by squaring the differences before averaging them and taking the square root.

A lower RMSE generally indicates better forecast accuracy.

### Forecast Bias

Bias is calculated as the average of forecast generation minus actual generation.

- **Positive bias:** Forecast generation is higher than actual generation on average.
- **Negative bias:** Forecast generation is lower than actual generation on average.
- **Bias near zero:** Forecasts have little average directional error, although individual errors may still be large.

All three metrics are expressed in the same generation units as the underlying data.

## Project Structure

```text
gridbricks-wind-dashboard/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── elexon.py
│   │   └── analysis.py
│   ├── tests/
│   │   └── test_analysis.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── App.jsx
│   ├── package.json
│   └── .env
└── README.md
```

## Prerequisites

Install the following before running the application:

- Python 3.11 or a compatible Python version
- Node.js and npm
- Git

An internet connection is required to retrieve data from Elexon BMRS.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/rakshithav2004/gridbricks-wind-dashboard.git
cd gridbricks-wind-dashboard
```

### 2. Set up the backend

Open a terminal in the project root.

Create a Python virtual environment:

```bash
cd backend
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

The backend should be available at:

- API root: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Interactive API documentation: http://127.0.0.1:8000/docs

Keep this terminal running.

### 3. Set up the frontend

Open a second terminal and navigate to the frontend directory from the project root:

```bash
cd frontend
npm install
```

Create or check the frontend `.env` file. For local development, it should contain:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the development server:

```bash
npm run dev
```

Open the local address printed by Vite, normally:

http://localhost:5173/

Both the backend and frontend must be running for the dashboard to retrieve live API data.

## API Endpoints

The backend exposes the following endpoints.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns API status information |
| GET | `/health` | Health check |
| GET | `/api/wind/actual` | Retrieves actual wind generation records |
| GET | `/api/wind/forecast` | Retrieves wind generation forecast records |
| GET | `/api/wind/analysis` | Returns matched records and forecast accuracy metrics |

The wind endpoints accept `start` and `end` query parameters in `YYYY-MM-DD` format. If omitted, the backend defaults to 1 January 2026 through 2 January 2026 as the date boundaries.

Example requests:

```text
http://127.0.0.1:8000/api/wind/actual?start=2026-01-01&end=2026-01-02
```

```text
http://127.0.0.1:8000/api/wind/forecast?start=2026-01-01&end=2026-01-02
```

```text
http://127.0.0.1:8000/api/wind/analysis?start=2026-01-01&end=2026-01-02
```

## Testing

The backend analysis module includes tests for metric calculations, empty input, mismatched input lengths, hourly matching, and filtering out non-wind generation records.

From the `backend` directory, activate the virtual environment and run:

```bash
python -m pytest -v
```

The current analysis test suite contains five tests.

## Data Source and Important Limitations

**Data source:** Elexon BMRS, which provides electricity market and generation data for Great Britain.

The application uses the `FUELHH` dataset for actual generation and the wind forecast endpoint for forecast records.

Important considerations:

- Actual and forecast records must be matched correctly before interpreting the metrics.
- The current implementation only compares hours for which exactly two half-hourly actual records are available.
- The forecast endpoint provides a latest historical view. It may not represent the forecast that was available to a buyer at the time an electricity purchasing decision was made.
- Forecast publication times and data availability should be checked before using historical comparisons for trading or purchasing decisions.
- The metrics are analytical indicators, not guarantees of financial outcomes.
- API availability and response formats may affect data retrieval.

For decision-grade backtesting, the analysis should use forecast versions that were available at the relevant decision time, rather than relying solely on the latest forecast view.

## Potential Future Improvements

- Add forecast-vintage selection and publication-time-aware backtesting.
- Expand the analysis to longer date ranges.
- Add daily and weekly performance summaries.
- Compare forecast errors across different periods.
- Add more robust data-quality checks and API retry handling.
- Improve deployment configuration and production monitoring.
- Add automated frontend tests and API integration tests.

## Author

**Rakshitha Bai V**

GitHub: https://github.com/rakshithav2004

---

*Developed as a full-stack wind generation forecast analysis project using React, FastAPI, Python, and Elexon BMRS data.*
