import { useMemo } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts'

// ── Theme colors matching the app's CSS variables ──
const COLORS = {
  cyan: '#22d3ee',
  purple: '#a78bfa',
  green: '#34d399',
  amber: '#fbbf24',
  red: '#f87171',
  blue: '#60a5fa',
  orange: '#fb923c',
  pink: '#f472b6',
}
const PIE_COLORS = [COLORS.cyan, COLORS.purple, COLORS.green, COLORS.amber, COLORS.blue, COLORS.orange, COLORS.pink, COLORS.red]

// ── Parse currency strings like "₹2,345.67" or "$1,234.56" into numbers ──
function parseCurrency(str) {
  if (!str || str === 'N/A') return null
  const cleaned = String(str).replace(/[₹$,\s]/g, '')
  const num = parseFloat(cleaned)
  return isNaN(num) ? null : num
}

// ── Parse market cap strings like "₹18.52 Trillion" into display-friendly format ──
function parseMarketCap(str) {
  if (!str || str === 'N/A') return null
  const match = String(str).match(/([\d.]+)\s*(Trillion|Billion|Million|Crore|Lakh)?/i)
  if (!match) return parseCurrency(str)
  return parseFloat(match[1])
}

// ── Detect & extract stock data from bot response text ──
function extractStockData(text) {
  if (!text) return null

  // Match the stock tool output pattern
  const stockPattern = /LIVE STOCK DATA FOR:\s*(.+?)\s*\((.+?)\)/i
  const headerMatch = text.match(stockPattern)
  if (!headerMatch) {
    // Also try markdown bold format from generator
    const mdPattern = /\*\*(.+?)\s*\(([A-Z0-9^.]+)\)\*\*/
    const mdMatch = text.match(mdPattern)
    if (!mdMatch) return null
  }

  const lines = text.split('\n')
  const data = {}

  for (const line of lines) {
    const cleaned = line.replace(/\*\*/g, '').replace(/\|/g, '').trim()

    if (/current\s*price/i.test(cleaned)) {
      const val = cleaned.split(/[:—–-]\s*/).pop().trim()
      data.currentPrice = parseCurrency(val)
      data.currentPriceDisplay = val
    }
    if (/today.?s?\s*range/i.test(cleaned)) {
      const parts = cleaned.split(/[:—–]\s*/).pop().trim().split(/\s*[-–]\s*/)
      data.dayLow = parseCurrency(parts[0])
      data.dayHigh = parseCurrency(parts[1])
    }
    if (/52.?week\s*range/i.test(cleaned)) {
      const parts = cleaned.split(/[:—–]\s*/).pop().trim().split(/\s*[-–]\s*/)
      data.wk52Low = parseCurrency(parts[0])
      data.wk52High = parseCurrency(parts[1])
    }
    if (/market\s*cap/i.test(cleaned)) {
      const val = cleaned.split(/[:—–]\s*/).pop().trim()
      data.marketCap = val
      data.marketCapNum = parseMarketCap(val)
    }
    if (/p\/?e\s*ratio/i.test(cleaned)) {
      const val = cleaned.split(/[:—–]\s*/).pop().trim()
      data.peRatio = parseFloat(val) || null
    }
    if (/volume/i.test(cleaned) && !/52/i.test(cleaned)) {
      const val = cleaned.split(/[:—–]\s*/).pop().trim()
      data.volume = val
    }
    if (/exchange/i.test(cleaned)) {
      data.exchange = cleaned.split(/[:—–]\s*/).pop().trim()
    }
  }

  // Extract name from header
  const nameMatch = text.match(/LIVE STOCK DATA FOR:\s*(.+?)\s*\(/i) ||
                    text.match(/\*\*(.+?)\s*\([A-Z0-9^.]+\)\*\*/i)
  if (nameMatch) data.name = nameMatch[1].trim()

  const tickerMatch = text.match(/\(([A-Z0-9^.]+(?:\.NS|\.BO)?)\)/i)
  if (tickerMatch) data.ticker = tickerMatch[1]

  // Only return if we have meaningful price data
  if (data.currentPrice || data.dayHigh || data.wk52High) {
    return data
  }
  return null
}

// ── Detect comparison tables (e.g., old vs new tax regime) ──
function extractComparisonData(text) {
  if (!text) return null

  // Look for markdown table patterns with numeric data
  const tableRegex = /\|(.+)\|\r?\n\|[-:\s|]+\|\r?\n((?:\|.+\|\r?\n?)+)/g
  const match = tableRegex.exec(text)
  if (!match) return null

  const headers = match[1].split('|').map(h => h.trim()).filter(Boolean)
  const rows = match[2].trim().split(/\r?\n/).flatMap(row => {
    const r = row.trim()
    if (!r) return []
    return [r.split('|').map(c => c.trim()).filter(Boolean)]
  })

  // Need at least 2 columns and 3 rows for a meaningful comparison
  if (headers.length < 2 || rows.length < 3) return null

  // Check if there are numeric values (percentages, amounts)
  const hasNumbers = rows.some(row =>
    row.some(cell => /[\d.]+%|₹[\d,.]+|[\d,]+/.test(cell))
  )
  if (!hasNumbers) return null

  return { headers, rows }
}

// ── Detect Budget/Allocation Pie Chart data ──
function extractPieChartData(text) {
  if (!text) return null

  const tableRegex = /\|(.+)\|\r?\n\|[-:\s|]+\|\r?\n((?:\|.+\|\r?\n?)+)/g
  const match = tableRegex.exec(text)
  if (!match) return null

  const headers = match[1].split('|').map(h => h.trim()).filter(Boolean)
  const rows = match[2].trim().split(/\r?\n/).flatMap(row => {
    const r = row.trim()
    if (!r) return []
    return [r.split('|').map(c => c.trim()).filter(Boolean)]
  })

  // Need exactly 2 columns for a clean Pie Chart (e.g., Sector | Percentage)
  if (headers.length !== 2) return null

  const data = []
  for (const row of rows) {
    if (row.length !== 2) continue
    const [name, valStr] = row
    
    // Look for percentage or raw numbers in the second column
    const numMatch = valStr.match(/([\d.]+)\s*%?/)
    if (numMatch) {
      data.push({ name: name.replace(/\*\*/g, '').trim(), value: parseFloat(numMatch[1]) })
    }
  }

  // If we have at least 2 data points, it's a valid pie chart
  if (data.length >= 2) {
    // Check if values look like percentages (sum close to 100) or just random numbers
    // Actually, recharts handles relative values fine, but let's just return it.
    return data
  }
  return null
}

// ── Custom Tooltip ──
function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  return (
    <div style={{
      background: 'rgba(15, 15, 20, 0.95)',
      border: '1px solid rgba(255,255,255,0.12)',
      borderRadius: '8px',
      padding: '10px 14px',
      fontSize: '0.8rem',
      color: '#e4e4e7',
      backdropFilter: 'blur(10px)',
      boxShadow: '0 8px 32px rgba(0,0,0,0.4)'
    }}>
      <p style={{ fontWeight: 600, marginBottom: 4, color: '#fff' }}>{label}</p>
      {payload.map((entry, i) => (
        <p key={i} style={{ color: entry.color, margin: '2px 0' }}>
          {entry.name}: {typeof entry.value === 'number'
            ? entry.value.toLocaleString('en-IN', { maximumFractionDigits: 2 })
            : entry.value}
        </p>
      ))}
    </div>
  )
}

// ── Stock Price Range Chart ──
function StockRangeChart({ data }) {
  const chartData = []

  if (data.dayLow && data.dayHigh) {
    chartData.push({
      name: "Today's Range",
      Low: data.dayLow,
      High: data.dayHigh,
      Current: data.currentPrice || 0,
    })
  }
  if (data.wk52Low && data.wk52High) {
    chartData.push({
      name: '52-Week Range',
      Low: data.wk52Low,
      High: data.wk52High,
      Current: data.currentPrice || 0,
    })
  }

  if (chartData.length === 0) return null

  return (
    <div className="chart-container">
      <div className="chart-header">
        <span className="chart-badge">📊 Price Range Visualization</span>
        <span className="chart-badge-source">Live Data · RapidAPI</span>
      </div>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={chartData} margin={{ top: 10, right: 20, left: 10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
          <XAxis dataKey="name" tick={{ fill: '#a1a1aa', fontSize: 12 }} axisLine={{ stroke: 'rgba(255,255,255,0.1)' }} />
          <YAxis tick={{ fill: '#a1a1aa', fontSize: 11 }} axisLine={{ stroke: 'rgba(255,255,255,0.1)' }} tickFormatter={v => `₹${v.toLocaleString('en-IN')}`} />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="Low" fill={COLORS.red} radius={[4, 4, 0, 0]} name="Low" />
          <Bar dataKey="Current" fill={COLORS.cyan} radius={[4, 4, 0, 0]} name="Current Price" />
          <Bar dataKey="High" fill={COLORS.green} radius={[4, 4, 0, 0]} name="High" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

// ── Stock Metrics Cards ──
function StockMetricsCards({ data }) {
  const metrics = []
  if (data.currentPriceDisplay) metrics.push({ label: 'Current Price', value: data.currentPriceDisplay, color: COLORS.cyan, icon: '💰' })
  if (data.marketCap) metrics.push({ label: 'Market Cap', value: data.marketCap, color: COLORS.purple, icon: '🏢' })
  if (data.peRatio) metrics.push({ label: 'P/E Ratio', value: data.peRatio.toFixed(2), color: COLORS.amber, icon: '📈' })
  if (data.volume) metrics.push({ label: 'Volume', value: data.volume, color: COLORS.green, icon: '📊' })

  if (metrics.length === 0) return null

  return (
    <div className="chart-metrics-grid">
      {metrics.map((m, i) => (
        <div key={i} className="chart-metric-card" style={{ borderColor: `${m.color}33` }}>
          <span className="chart-metric-icon">{m.icon}</span>
          <div>
            <div className="chart-metric-label">{m.label}</div>
            <div className="chart-metric-value" style={{ color: m.color }}>{m.value}</div>
          </div>
        </div>
      ))}
    </div>
  )
}

// ── Budget / Allocation Pie Chart (future-ready) ──
function AllocationPieChart({ data }) {
  if (!data || data.length === 0) return null

  return (
    <div className="chart-container">
      <div className="chart-header">
        <span className="chart-badge">🥧 Allocation Breakdown</span>
      </div>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={50}
            outerRadius={90}
            paddingAngle={3}
            dataKey="value"
            nameKey="name"
            label={false} /* Removed overlapping labels, relying on Legend */
          >
            {data.map((_, i) => (
              <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ fontSize: '0.75rem', color: '#a1a1aa' }}
            iconType="circle"
            iconSize={8}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

// ── Main ChartRenderer Component ──
export default function ChartRenderer({ content }) {
  const analysis = useMemo(() => {
    if (!content || typeof content !== 'string') return null

    const stockData = extractStockData(content)
    const pieData = extractPieChartData(content)
    // Only show comparison table if it's NOT a pie chart table (to avoid duplicates)
    const comparisonData = !pieData ? extractComparisonData(content) : null

    if (!stockData && !comparisonData && !pieData) return null

    return { stockData, comparisonData, pieData }
  }, [content])

  if (!analysis) return null

  const { stockData, comparisonData, pieData } = analysis

  return (
    <div className="chart-renderer">
      {/* Stock Data Visualizations */}
      {stockData && (
        <>
          <StockMetricsCards data={stockData} />
          <StockRangeChart data={stockData} />
        </>
      )}

      {/* Pie Chart (Budget/Allocation) */}
      {pieData && <AllocationPieChart data={pieData} />}

      {/* Comparison Table Charts (future: tax slabs, etc.) */}
      {comparisonData && comparisonData.rows.length > 0 && (
        <div className="chart-container">
          <div className="chart-header">
            <span className="chart-badge">📋 Data Comparison</span>
          </div>
          <div className="chart-table-wrapper">
            <table className="chart-styled-table">
              <thead>
                <tr>
                  {comparisonData.headers.map((h, i) => (
                    <th key={i}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {comparisonData.rows.map((row, i) => (
                  <tr key={i}>
                    {row.map((cell, j) => {
                      const cleanCell = cell.replace(/\*\*/g, '').replace(/\*/g, '')
                      return (
                        <td key={j} style={{
                          color: /[\d.]+%/.test(cleanCell) ? COLORS.cyan : 'inherit',
                          fontWeight: /[\d.]+%|₹/.test(cleanCell) ? 600 : 400
                        }}>{cleanCell}</td>
                      )
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
