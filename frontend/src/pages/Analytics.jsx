/**
 * pages/Analytics.jsx — Full analytics dashboard
 */
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { RiBarChartLine, RiRefreshLine } from "react-icons/ri";
import Layout from "../components/Layout";
import StatCard from "../components/StatCard";
import {
  TopSkillsChart, TopCompaniesChart,
  PlacementTrendChart, DomainsChart, TopRolesChart,
} from "../components/AnalyticsCharts";
import api from "../api/client";
import toast from "react-hot-toast";

export default function Analytics() {
  const [data, setData]     = useState(null);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const r = await api.get("/analytics");
      setData(r.data);
    } catch {
      toast.error("Could not load analytics");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  return (
    <Layout>
      <div className="p-6 max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <motion.div initial={{ opacity:0, y:-10 }} animate={{ opacity:1, y:0 }}
          className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <div className="w-8 h-8 rounded-xl bg-accent-green/15 flex items-center justify-center">
                <RiBarChartLine className="text-emerald-300" />
              </div>
              <h1 className="font-display font-bold text-2xl text-white">Career Analytics</h1>
            </div>
            <p className="text-slate-400 text-sm ml-11">Live insights from alumni placement data</p>
          </div>
          <button onClick={load} className="btn-secondary btn-sm">
            <RiRefreshLine className={loading ? "animate-spin" : ""} />
            Refresh
          </button>
        </motion.div>

        {/* Top stats */}
        {data && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard icon={RiBarChartLine} label="Total Alumni"    value={data.total_alumni || 0}           color="brand"  delay={0} />
            <StatCard icon={RiBarChartLine} label="Top Companies"   value={data.top_companies?.length || 0}  color="violet" delay={0.05} />
            <StatCard icon={RiBarChartLine} label="Unique Roles"    value={data.top_roles?.length || 0}      color="cyan"   delay={0.1} />
            <StatCard icon={RiBarChartLine} label="Skills Tracked"  value={data.top_skills?.length || 0}     color="amber"  delay={0.15} />
          </div>
        )}

        {/* Charts grid */}
        {loading ? (
          <div className="grid md:grid-cols-2 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="card p-5">
                <div className="h-5 skeleton w-40 mb-4 rounded" />
                <div className="h-52 skeleton rounded" />
              </div>
            ))}
          </div>
        ) : data ? (
          <>
            <div className="grid md:grid-cols-2 gap-6">
              <TopSkillsChart    data={data.top_skills} />
              <TopCompaniesChart data={data.top_companies} />
            </div>
            <div className="grid md:grid-cols-2 gap-6">
              <PlacementTrendChart data={data.placement_trend} />
              <DomainsChart        data={data.hiring_domains} />
            </div>
            <TopRolesChart data={data.top_roles} />
          </>
        ) : (
          <div className="card p-12 text-center">
            <RiBarChartLine className="text-slate-600 text-4xl mx-auto mb-3" />
            <p className="text-slate-400">No analytics data available yet.</p>
          </div>
        )}
      </div>
    </Layout>
  );
}
