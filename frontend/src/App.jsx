import { useEffect, useState } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import "./App.css";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function formatNumber(value) {
  if (value === null || value === undefined || !Number.isFinite(Number(value))) {
    return "—";
  }

  return Number(value).toLocaleString("en-GB", {
    maximumFractionDigits: 2,
  });
}

function formatMetric(value) {
  return value === null || value === undefined ? "—" : formatNumber(value);
}

function formatHour(value) {
  if (!value) return "—";

  return new Date(value).toLocaleTimeString("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
    timeZone: "UTC",
  });
}

function MetricCard({ label, value, subtitle }) {
  return (
    <article className="metric-card">
      <p className="metric-label">{label}</p>
      <h2>{value}</h2>
      <p className="metric-subtitle">{subtitle}</p>
    </article>
  );
}

export default function App() {
  const [start, setStart] = useState("2026-01-01");
  const [end, setEnd] = useState("2026-01-02");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadAnalysis(event) {
    event?.preventDefault();

    if (start >= end) {
      setError("The end date must be later than the start date.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const query = new URLSearchParams({ start, end });
      const response = await fetch(
        `${API_BASE_URL}/api/wind/analysis?${query.toString()}`,
      );

      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(body.detail || `Request failed (${response.status})`);
      }

      const result = await response.json();
      setAnalysis(result);
    } catch (err) {
      setAnalysis(null);
      setError(
        `${err.message}. Check that the FastAPI backend is running and reachable.`,
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAnalysis();
    // Load the default date range on initial render.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const rows = analysis?.data ?? [];

  const averageActual =
    rows.length > 0
      ? rows.reduce((sum, row) => sum + Number(row.actual), 0) / rows.length
      : null;

  const averageForecast =
    rows.length > 0
      ? rows.reduce((sum, row) => sum + Number(row.forecast), 0) / rows.length
      : null;

  return (
    <main className="dashboard">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">W</div>
          <div>
            <p className="eyebrow">ENERGY INTELLIGENCE</p>
            <h1>Wind Forecast Monitor</h1>
          </div>
        </div>

        <div className="live-status">
          <span className="status-dot" />
          Elexon data source
        </div>
      </header>

      <section className="intro">
        <div>
          <p className="eyebrow">UK POWER MARKET · ANALYTICS</p>
          <h2>Wind generation overview</h2>
          <p className="intro-text">
            Compare observed wind generation with published forecasts to
            understand forecast error over a selected period.
          </p>
        </div>

        <form className="date-filter" onSubmit={loadAnalysis}>
          <label>
            Start date
            <input
              type="date"
              value={start}
              max={end}
              onChange={(event) => setStart(event.target.value)}
              required
            />
          </label>

          <label>
            End date
            <input
              type="date"
              value={end}
              min={start}
              onChange={(event) => setEnd(event.target.value)}
              required
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Loading..." : "Analyse"}
          </button>
        </form>
      </section>

      {error && (
        <div className="error-banner" role="alert">
          <strong>Unable to load analysis</strong>
          <span>{error}</span>
          <button type="button" onClick={() => loadAnalysis()}>
            Retry
          </button>
        </div>
      )}

      {loading && !analysis && (
        <div className="message-card">Loading wind generation data…</div>
      )}

      {!error && analysis && (
        <>
          <section className="metric-grid" aria-label="Generation metrics">
            <MetricCard
              label="Average actual generation"
              value={
                averageActual === null
                  ? "—"
                  : `${formatNumber(averageActual)} MW`
              }
              subtitle={`${formatNumber(analysis.matched_count)} matched hours`}
            />

            <MetricCard
              label="Average forecast generation"
              value={
                averageForecast === null
                  ? "—"
                  : `${formatNumber(averageForecast)} MW`
              }
              subtitle={`${formatNumber(analysis.forecast_count)} forecast records`}
            />

            <MetricCard
              label="Mean absolute error"
              value={
                analysis.metrics.mae === null
                  ? "—"
                  : `${formatNumber(analysis.metrics.mae)} MW`
              }
              subtitle="Average absolute forecast error"
            />

            <MetricCard
              label="Forecast bias"
              value={
                analysis.metrics.bias === null
                  ? "—"
                  : `${formatNumber(analysis.metrics.bias)} MW`
              }
              subtitle="Forecast minus actual generation"
            />
          </section>

          <section className="panel chart-panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">GENERATION PROFILE</p>
                <h3>Actual vs forecast</h3>
              </div>
              <span className="record-count">
                {rows.length} hourly comparisons
              </span>
            </div>

            {rows.length > 0 ? (
              <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={rows}
                    margin={{ top: 12, right: 20, left: 8, bottom: 8 }}
                  >
                    <CartesianGrid
                      strokeDasharray="3 3"
                      vertical={false}
                      stroke="#e5eaf0"
                    />
                    <XAxis
                      dataKey="startTime"
                      tickFormatter={formatHour}
                      minTickGap={28}
                      tick={{ fill: "#718096", fontSize: 12 }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <YAxis
                      tickFormatter={(value) => formatNumber(value)}
                      tick={{ fill: "#718096", fontSize: 12 }}
                      axisLine={false}
                      tickLine={false}
                      width={76}
                    />
                    <Tooltip
                      labelFormatter={(value) =>
                        `${new Date(value).toISOString().slice(0, 16).replace("T", " ")} UTC`
                      }
                      formatter={(value, name) => [
                        `${formatNumber(value)} MW`,
                        name,
                      ]}
                    />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="actual"
                      name="Actual generation"
                      stroke="#0f766e"
                      strokeWidth={2.5}
                      dot={false}
                      activeDot={{ r: 5 }}
                    />
                    <Line
                      type="monotone"
                      dataKey="forecast"
                      name="Forecast generation"
                      stroke="#6478e8"
                      strokeWidth={2.5}
                      dot={false}
                      activeDot={{ r: 5 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <div className="empty-state">
                No matching hourly records are available for this period.
              </div>
            )}

            <p className="chart-note">
              Values are shown in MW. Forecast publication time should be
              checked before using these comparisons for historical trading
              decisions.
            </p>
          </section>

          <section className="panel table-panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">PERIOD DETAILS</p>
                <h3>Hourly generation data</h3>
              </div>
              <span className="record-count">
                {rows.length} records
              </span>
            </div>

            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>Hour (UTC)</th>
                    <th>Actual (MW)</th>
                    <th>Forecast (MW)</th>
                    <th>Error (MW)</th>
                    <th>Published (UTC)</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row) => (
                    <tr
                      key={`${row.startTime}-${row.settlementPeriod}`}
                    >
                      <td>{formatHour(row.startTime)}</td>
                      <td>{formatNumber(row.actual)}</td>
                      <td>{formatNumber(row.forecast)}</td>
                      <td
                        className={
                          Number(row.forecast) - Number(row.actual) >= 0
                            ? "positive"
                            : "negative"
                        }
                      >
                        {formatNumber(
                          Number(row.forecast) - Number(row.actual),
                        )}
                      </td>
                      <td>
                        {row.publishTime
                          ? `${row.publishTime.replace("T", " ").slice(0, 16)}`
                          : "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <footer className="dashboard-footer">
            <span>Source: Elexon BMRS API</span>
            <span>
              Period: {analysis.start} to {analysis.end}
            </span>
            <span>
              RMSE: {formatMetric(analysis.metrics.rmse)} MW
            </span>
          </footer>
        </>
      )}
    </main>
  );
}