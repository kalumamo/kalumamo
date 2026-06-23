"use client";
import { useEffect, useState, useCallback } from "react";
import { Layers, BarChart3, TrendingUp, TrendingDown, Minus, AlertTriangle } from "lucide-react";
import Header from "@/components/layout/Header";
import KPICard from "@/components/dashboard/KPICard";
import TierBadge from "@/components/dashboard/TierBadge";
import SeverityBadge from "@/components/dashboard/SeverityBadge";
import PerformanceTrendChart from "@/components/charts/PerformanceTrendChart";
import MultiLineChart from "@/components/charts/MultiLineChart";
import TierDistributionChart from "@/components/charts/TierDistributionChart";
import api from "@/lib/api";
import { formatScore, formatCategoryName, formatCurrency } from "@/lib/utils";
import { useRefresh } from "@/lib/use-refresh";
import { toast } from "sonner";

interface KPIs {
  total_products: number;
  avg_performance_score: number;
  high_tier_count: number;
  medium_tier_count: number;
  low_tier_count: number;
  total_alerts: number;
  critical_alerts: number;
}

interface Ranking {
  rank: number;
  product_id: number;
  product_name: string;
  product_category: string;
  performance_score: number;
  performance_tier: string;
  score_change: number | null;
  trend: string;
  recommendation_count: number;
}

interface Alert {
  id: number;
  product_name: string;
  alert_type: string;
  severity: string;
  title: string;
  period_date: string;
}

export default function DashboardPage() {
  const [kpis, setKpis] = useState<KPIs | null>(null);
  const [charts, setCharts] = useState<any>(null);
  const [rankings, setRankings] = useState<Ranking[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);

  const load = useCallback(async () => {
    try {
      const [kpisRes, chartsRes, rankingsRes, alertsRes] = await Promise.all([
        api.get("/scores/dashboard/kpis"),
        api.get("/scores/dashboard/charts"),
        api.get("/rankings/"),
        api.get("/alerts/?is_resolved=false&limit=5"),
      ]);
      setKpis(kpisRes.data);
      setCharts(chartsRes.data);
      setRankings(rankingsRes.data);
      setAlerts(alertsRes.data);
    } catch {
      toast.error("Failed to load dashboard data");
    }
  }, []);

  useEffect(() => { load(); }, [load]);
  useRefresh(load);  // auto-reload when data is uploaded

  return (
    <div>
      <Header title="Dashboard" subtitle="AI-Powered Digital Banking Performance Overview" />

      <div className="p-6 space-y-6">
        {/* KPI Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <KPICard
            title="Total Products"
            value={kpis?.total_products || 0}
            icon={Layers}
            subtitle="Active digital products"
          />
          <KPICard
            title="Avg Performance Score"
            value={formatScore(kpis?.avg_performance_score)}
            icon={BarChart3}
            subtitle="Across all products"
          />
          <KPICard
            title="Active Alerts"
            value={kpis?.total_alerts || 0}
            icon={AlertTriangle}
            subtitle={`${kpis?.critical_alerts || 0} critical`}
            iconBg="bg-[#FDECEA]"
          />
          <div className="bg-white rounded-xl border border-gray-100 p-5 shadow-card">
            <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">Performance Tiers</p>
            <div className="flex gap-3">
              <div className="text-center">
                <div className="text-lg font-bold text-[#2D5A27]">{kpis?.high_tier_count || 0}</div>
                <div className="text-[10px] text-gray-500">HIGH</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-[#7A5C00]">{kpis?.medium_tier_count || 0}</div>
                <div className="text-[10px] text-gray-500">MED</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-[#8B1A1A]">{kpis?.low_tier_count || 0}</div>
                <div className="text-[10px] text-gray-500">LOW</div>
              </div>
            </div>
          </div>
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2">
            <PerformanceTrendChart
              data={charts?.performance_trend || []}
              title="Average Performance Score Trend"
            />
          </div>
          <div className="bg-white rounded-xl border border-gray-100 p-5 shadow-card">
            <h3 className="text-sm font-semibold text-gray-800 mb-1">Tier Distribution</h3>
            <TierDistributionChart
              high={kpis?.high_tier_count || 0}
              medium={kpis?.medium_tier_count || 0}
              low={kpis?.low_tier_count || 0}
            />
          </div>
        </div>

        {/* Revenue & User Trends */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <MultiLineChart
            data={charts?.revenue_trend || []}
            title="Revenue Trend by Product"
          />
          <MultiLineChart
            data={charts?.user_growth_trend || []}
            title="Active User Growth"
          />
        </div>

        {/* Failure & Complaint Trends */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <MultiLineChart
            data={charts?.failure_rate_trend || []}
            title="Transaction Failure Rate (%)"
          />
          <MultiLineChart
            data={charts?.complaint_trend || []}
            title="Complaint Volume"
          />
        </div>

        {/* Rankings Table & Alerts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Rankings */}
          <div className="lg:col-span-2 bg-white rounded-xl border border-gray-100 shadow-card overflow-hidden">
            <div className="px-5 py-4 border-b border-gray-100">
              <h3 className="text-sm font-semibold text-gray-800">Product Rankings</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full data-table">
                <thead>
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Rank</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Product</th>
                    <th className="px-4 py-3 text-center text-xs font-semibold text-gray-500 uppercase tracking-wide">Score</th>
                    <th className="px-4 py-3 text-center text-xs font-semibold text-gray-500 uppercase tracking-wide">Tier</th>
                    <th className="px-4 py-3 text-center text-xs font-semibold text-gray-500 uppercase tracking-wide">Trend</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {rankings.slice(0, 6).map((r) => (
                    <tr key={r.product_id} className="hover:bg-gray-50 transition">
                      <td className="px-4 py-3">
                        <span className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold ${
                          r.rank === 1 ? "bg-[#7A0E28] text-white" :
                          r.rank === 2 ? "bg-[#9B1535] text-white" :
                          r.rank === 3 ? "bg-[#BE1B3C] text-white" : "bg-gray-100 text-gray-600"
                        }`}>
                          {r.rank}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <div className="text-sm font-medium text-gray-900">{r.product_name}</div>
                        <div className="text-xs text-gray-400">{formatCategoryName(r.product_category)}</div>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className="text-sm font-bold text-[#7A0E28]">{formatScore(r.performance_score)}</span>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <TierBadge tier={r.performance_tier} size="sm" />
                      </td>
                      <td className="px-4 py-3 text-center">
                        {r.trend === "up" ? (
                          <TrendingUp size={14} className="text-green-600 mx-auto" />
                        ) : r.trend === "down" ? (
                          <TrendingDown size={14} className="text-red-600 mx-auto" />
                        ) : (
                          <Minus size={14} className="text-gray-400 mx-auto" />
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Recent Alerts */}
          <div className="bg-white rounded-xl border border-gray-100 shadow-card">
            <div className="px-5 py-4 border-b border-gray-100">
              <h3 className="text-sm font-semibold text-gray-800">Active Alerts</h3>
            </div>
            <div className="divide-y divide-gray-50">
              {alerts.length === 0 ? (
                <div className="p-5 text-center text-sm text-gray-400">No active alerts</div>
              ) : alerts.map((a) => (
                <div key={a.id} className="px-5 py-4">
                  <div className="flex items-start justify-between gap-2 mb-1">
                    <SeverityBadge severity={a.severity} />
                    <span className="text-[10px] text-gray-400">{a.period_date}</span>
                  </div>
                  <p className="text-xs font-medium text-gray-800 mt-1">{a.title}</p>
                  <p className="text-[10px] text-gray-500">{a.product_name}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
