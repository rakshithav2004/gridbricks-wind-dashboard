# UK Wind Forecast Analysis Dashboard

A full-stack analytics dashboard for comparing wind generation forecasts with actual generation in Great Britain. Built using React, FastAPI, Python, and the Elexon BMRS API.

## Live Demo

- **Live Dashboard:** https://gridbricks-wind-dashboard.vercel.app
- **Backend API:** https://gridbricks-wind-api-gzap.onrender.com
- **Interactive API Documentation:** https://gridbricks-wind-api-gzap.onrender.com/docs
- **Health Check:** https://gridbricks-wind-api-gzap.onrender.com/health

> **Note:** The backend runs on Render's free instance, which may take some time to wake up after inactivity.

## Overview

Wind generation forecasts can differ from actual generation. Analysing these differences helps energy analysts evaluate forecast performance and identify periods that may require further investigation.

This application retrieves actual wind generation and forecast records from Elexon BMRS, matches the data by hour, calculates forecast accuracy metrics, and presents the results in an interactive dashboard.

Users can select a date range, compare actual and forecast generation, review summary metrics, and inspect individual hourly records.

## Key Features

- Retrieve actual wind generation data from Elexon BMRS.
- Retrieve wind generation forecast data.
- Match actual and forecast values by hour.
- Calculate Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and forecast bias.
- Visualise actual and forecast generation using interactive charts.
- Filter results by start and end dates.
- Inspect matched hourly records and forecast publication timestamps.
- Validate date ranges and handle upstream API errors.
- Test the backend analysis logic using pytest.
- Deploy the frontend and backend independently.

## Technology Stack

### Frontend
- React
- Vite
- JavaScript
- Recharts
- CSS

### Backend
- Python 3.11
- FastAPI
- HTTPX
- Uvicorn
- Pytest

### Data Source
- Elexon BMRS API

### Deployment
- Vercel — frontend
- Render — backend
- GitHub — source code and version control

## Architecture

The application follows a frontend-backend architecture.

1. The React frontend lets users select dates and explore the analysis.
2. The FastAPI backend retrieves actual and forecast records from Elexon BMRS.
3. The backend filters wind generation data and matches actual and forecast values by hour.
4. The analysis module calculates forecast accuracy metrics.
5. The frontend displays summary cards, a generation comparison chart, and hourly records.

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
                 React Frontend
           +------------+------------+
           |            |            |
       KPI Cards    Line Chart   Hourly Table
```

## Forecast Accuracy Metrics

The dashboard calculates three metrics using matched actual and forecast values.

### Mean Absolute Error (MAE)

MAE is the average absolute difference between actual and forecast generation.

A lower MAE indicates a smaller average forecast error.

### Root Mean Squared Error (RMSE)

RMSE is the square root of the average squared difference between actual and forecast generation.

Because errors are squared, larger errors have a greater influence on RMSE.

### Forecast Bias

Forecast bias is calculated as:

`Average forecast generation - Average actual generation`

Equivalently, it is the mean of the forecast-minus-actual errors over the matched records.

- **Positive bias:** Forecast generation is higher than actual generation on average.
- **Negative bias:** Forecast generation is lower than actual generation on average.
- **Bias near zero:** Average directional error is small, although individual errors may still be large.

All three metrics use the same generation units as the underlying data, reported in MW.

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
│   ├── package-lock.json
│   └── .env.example
└── README.md
```

The structure above shows the main application files. Other frontend components, stylesheets, configuration files, and tests may also be present.

**Environment files:** Keep local `.env` files out of version control when appropriate. Commit an `.env.example` containing placeholder configuration rather than machine-specific or secret values.

## Prerequisites

Install the following:

- Python 3.11 or a compatible Python version
- Node.js and npm
- Git
- An internet connection to retrieve Elexon BMRS data

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/rakshithav2004/gridbricks-wind-dashboard.git
cd gridbricks-wind-dashboard
```

### 2. Set up the backend

From the project root:

```bash
cd backend
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

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

Open a second terminal from the project root:

```bash
cd frontend
npm install
```

Create a local `.env` file in the `frontend` directory with:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the frontend:

```bash
npm run dev
```

Open the address printed by Vite, normally:

http://localhost:5173/

Both the backend and frontend must be running for the dashboard to retrieve data locally.

**Configuration note:** Vite reads `VITE_` environment variables during the build. If the API URL changes, restart the development server or rebuild and redeploy the frontend as appropriate.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns API status information |
| GET | `/health` | Health check |
| GET | `/api/wind/actual` | Retrieves actual wind generation records |
| GET | `/api/wind/forecast` | Retrieves wind forecast records |
| GET | `/api/wind/analysis` | Returns matched records and forecast accuracy metrics |

The wind endpoints accept `start` and `end` query parameters in `YYYY-MM-DD` format. The default date boundaries are 1 January 2026 and 2 January 2026, respectively.

Example local requests:

```text
http://127.0.0.1:8000/api/wind/actual?start=2026-01-01&end=2026-01-02
```

```text
http://127.0.0.1:8000/api/wind/forecast?start=2026-01-01&end=2026-01-02
```

```text
http://127.0.0.1:8000/api/wind/analysis?start=2026-01-01&end=2026-01-02
```

The same endpoints are available through the deployed backend:

https://gridbricks-wind-api-gzap.onrender.com/docs

## Testing

The backend analysis tests cover metric calculations, empty input, mismatched input lengths, hourly matching, and filtering out non-wind generation records.

From the `backend` directory, activate the virtual environment and run:

```bash
python -m pytest -v
```

The current analysis test suite contains five tests.

The frontend production build was also verified during development.

## Deployment

### Frontend — Vercel

The frontend is deployed on Vercel.

Production URL:

https://gridbricks-wind-dashboard.vercel.app

Configure the following environment variable in the Vercel project settings:

```env
VITE_API_BASE_URL=https://gridbricks-wind-api-gzap.onrender.com
```

Ensure the variable is enabled for the required deployment environments and trigger a fresh deployment after changing it.

### Backend — Render

The FastAPI backend is deployed on Render.

Production URL:

https://gridbricks-wind-api-gzap.onrender.com

The backend service uses the `backend` directory as its root directory.

Typical deployment commands:

**Build command**

```bash
pip install -r requirements.txt
```

**Start command**

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The backend's CORS configuration permits the local development frontend and the deployed Vercel frontend.

## Data Source and Important Limitations

**Data source:** Elexon BMRS, which provides electricity market and generation data for Great Britain.

The application uses the `FUELHH` dataset for actual generation and a wind forecast endpoint for forecast records.

Important considerations:

- Actual and forecast records must be matched correctly before interpreting the metrics.
- The current implementation compares hours for which exactly two half-hourly actual records are available.
- The forecast endpoint provides a latest historical view and may not represent the forecast available to a buyer at the time an electricity purchasing decision was made.
- Forecast publication timestamps should be reviewed before interpreting historical comparisons as evidence of forecast performance at a particular decision time.
- The metrics are analytical indicators, not guarantees of financial outcomes.
- Upstream API availability and response formats may affect data retrieval.

For decision-grade backtesting, use forecast versions that were available at the relevant decision time rather than relying solely on the latest forecast view.

## Potential Future Improvements

- Add forecast-vintage selection and publication-time-aware backtesting.
- Expand the analysis to longer date ranges.
- Add daily and weekly performance summaries.
- Compare forecast errors across different periods.
- Improve data-quality checks, retry handling, and error reporting.
- Add automated frontend tests and API integration tests.
- Improve monitoring and operational observability.

## Author

**Rakshitha Bai V**

GitHub: https://github.com/rakshithav2004

---

Developed as a full-stack wind generation forecast analysis project using React, FastAPI, Python, and Elexon BMRS data.
