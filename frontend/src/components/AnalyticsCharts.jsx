/**
 * components/AnalyticsCharts.jsx — Recharts dashboard charts
 */
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, PieChart, Pie, Cell, Legend, Area, AreaChart,
} from "recharts";
import { motion } from "framer-motion";

const COLORS = ["#3355ff","#06d6d6","#7c3aed","#f59e0b","#10b981","#f43f5e","#8b5cf6","#06b6d4"];

const chartTheme = {
  cartesianGrid:  { strokeDasharray: "3 3", stroke: "rgba(255,255,255,0.05)" },
  xAxis:          { tick: { fill: "#64748b", fontSize: 11, fontFamily: "'DM Sans'" }, axisLine: false, tickLine: false },
  yAxis:          { tick: { fill: "#64748b", fontSize: 11, fontFamily: "'DM Sans'" }, axisLine: false, tickLine: false },
  tooltip: {
    contentStyle: { background: "#111d35", border: "1px solid rgba(51,85,255,0.2)", borderRadius: "12px", fontFamily: "'DM Sans'" },
    labelStyle:   { color: "#94a3b8", fontSize: 11 },
    itemStyle:    { color: "#e2e8f0", fontSize: 12 },
    cursor:       { fill: "rgba(51,85,255,0.08)" },
  },
};

function ChartCard({ title, subtitle, children, delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className="card p-5"
    >
      <div className="mb-4">
        <h3 className="font-display font-semibold text-white text-sm">{title}</h3>
        {subtitle && <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>}
      </div>
      {children}
    </motion.div>
  );
}

export function TopSkillsChart({ data = [] }) {
  return (
    <ChartCard title="Top Skills in Demand" subtitle="Most common alumni skills" delay={0.1}>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data} layout="vertical" margin={{ left: 8, right: 16 }}>
          <CartesianGrid {...chartTheme.cartesianGrid} horizontal={false} />
          <XAxis type="number" {...chartTheme.xAxis} />
          <YAxis type="category" dataKey="label" width={90} {...chartTheme.xAxis} />
          <Tooltip {...chartTheme.tooltip} />
          <Bar dataKey="count" radius={[0, 6, 6, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} opacity={0.85} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

export function TopCompaniesChart({ data = [] }) {
  return (
    <ChartCard title="Top Hiring Companies" subtitle="Alumni employer distribution" delay={0.15}>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data} margin={{ left: 0, right: 8, bottom: 20 }}>
          <CartesianGrid {...chartTheme.cartesianGrid} vertical={false} />
          <XAxis dataKey="label" {...chartTheme.xAxis} angle={-30} textAnchor="end" interval={0} />
          <YAxis {...chartTheme.yAxis} />
          <Tooltip {...chartTheme.tooltip} />
          <Bar dataKey="count" radius={[6, 6, 0, 0]}>
            {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} opacity={0.85} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

export function PlacementTrendChart({ data = [] }) {
  const formatted = data.map(d => ({ ...d, name: d.year }));
  return (
    <ChartCard title="Placement Trend" subtitle="Alumni placements by graduation year" delay={0.2}>
      <ResponsiveContainer width="100%" height={220}>
        <AreaChart data={formatted}>
          <defs>
            <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%"  stopColor="#3355ff" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#3355ff" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid {...chartTheme.cartesianGrid} />
          <XAxis dataKey="name" {...chartTheme.xAxis} />
          <YAxis {...chartTheme.yAxis} />
          <Tooltip {...chartTheme.tooltip} />
          <Area type="monotone" dataKey="count" stroke="#3355ff" strokeWidth={2} fill="url(#areaGrad)" dot={{ fill: "#3355ff", r: 4 }} />
        </AreaChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

export function DomainsChart({ data = [] }) {
  return (
    <ChartCard title="Industry Distribution" subtitle="Career domains of alumni" delay={0.25}>
      <div className="flex items-center gap-4">
        <ResponsiveContainer width="55%" height={200}>
          <PieChart>
            <Pie data={data} dataKey="count" nameKey="label" cx="50%" cy="50%" outerRadius={80} innerRadius={48}>
              {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
            </Pie>
            <Tooltip {...chartTheme.tooltip} />
          </PieChart>
        </ResponsiveContainer>
        <div className="flex-1 space-y-2">
          {data.slice(0, 6).map((d, i) => (
            <div key={i} className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ background: COLORS[i % COLORS.length] }} />
              <span className="text-xs text-slate-400 truncate flex-1">{d.label}</span>
              <span className="text-xs font-display text-white">{d.count}</span>
            </div>
          ))}
        </div>
      </div>
    </ChartCard>
  );
}

export function TopRolesChart({ data = [] }) {
  return (
    <ChartCard title="Top Job Roles" subtitle="Most common alumni positions" delay={0.3}>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data} layout="vertical" margin={{ left: 8, right: 16 }}>
          <CartesianGrid {...chartTheme.cartesianGrid} horizontal={false} />
          <XAxis type="number" {...chartTheme.xAxis} />
          <YAxis type="category" dataKey="label" width={120} {...chartTheme.xAxis} />
          <Tooltip {...chartTheme.tooltip} />
          <Bar dataKey="count" radius={[0, 6, 6, 0]} fill="#7c3aed" opacity={0.85} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}
