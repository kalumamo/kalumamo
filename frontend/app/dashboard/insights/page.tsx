"use client";
import { useEffect, useState, useCallback } from "react";
import { AlertTriangle, Lightbulb, TrendingDown, TrendingUp } from "lucide-react";
import Header from "@/components/layout/Header";
import SeverityBadge from "@/components/dashboard/SeverityBadge";
import api from "@/lib/api";
import { useRefresh } from "@/lib/use-refresh";
import { toast } from "sonner";

interface Alert {
  id: number;
  product_name: string;
  alert_type: string;
  severity: string;
  title: string;
  message: string;
  is_resolved: boolean;
  period_date: string;
}

interface Recommendation {
  id: number;
  product_name: string;
  category: string;
  priority: string;
  title: string;
  description: string;
  is_acknowledged: boolean;
  period_date: string;
}

export default function ExecutiveInsightsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<"alerts" | "recommendations" | "summary">("summary");

  const load = useCallback(async () => {
    try {
      const [alertsRes, recsRes] = await Promise.all([
        api.get("/alerts/?limit=100"),
        api.get("/recommendations/?limit=100"),
      ]);
      setAlerts(alertsRes.data || []);
      setRecommendations(recsRes.data || []);
    } catch {
      toast.error("Failed to load insights data");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);
  useRefresh(load);

  const unresolvedAlerts = alerts.filter((a) => !a.is_resolved);
  const unacknowledgedRecs = recommendations.filter((r) => !r.is_acknowledged);
  const criticalAlerts = alerts.filter((a) => a.severity === "critical" && !a.is_resolved);
  const highPriorityRecs = recommendations.filter(
    (r) => r.priority === "critical" && !r.is_acknowledged
  );

  // Group alerts by product
  const alertsByProduct = alerts.reduce((acc: any, a) => {
    if (!acc[a.product_name]) acc[a.product_name] = [];
    acc[a.product_name].push(a);
    return acc;
  }, {});

  // Group recommendations by product
  const recsByProduct = recommendations.reduce((acc: any, r) => {
    if (!acc[r.product_name]) acc[r.product_name] = [];
    acc[r.product_name].push(r);
    return acc;
  }, {});

  const StatCard = ({
    label,
    value,
    icon: Icon,
    color,
    subtitle,
  }: {
    label: string;
    value: number;
    icon: React.ElementType;
    color: string;
    subtitle?: string;
  }) => (
    <div className="bg-white rounded-xl border border-gray-100 p-5 shadow-card">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wide font-semibold mb-1">
            {label}
          </p>
          <div className="text-3xl font-bold" style={{ color }}>
            {value}
          </div>
          {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
        </div>
        <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ background: `${color}20` }}>
          <Icon size={20} style={{ color }} />
        </div>
      </div>
    </div>
  );

  return (
    <div>
      <Header
        title="Executive Insights"
        subtitle="Compiled alerts and recommendations for executive review and decision-making"
      />
      <div className="p-6 space-y-6">
        {/* Summary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            label="Unresolved Alerts"
            value={unresolvedAlerts.length}
            icon={AlertTriangle}
            color="#8B1A1A"
            subtitle={`${criticalAlerts.length} critical`}
          />
          <StatCard
            label="Pending Recommendations"
            value={unacknowledgedRecs.length}
            icon={Lightbulb}
            color="#9B1535"
            subtitle={`${highPriorityRecs.length} critical`}
          />
          <StatCard
            label="Products with Issues"
            value={Object.keys(alertsByProduct).length}
            icon={TrendingDown}
            color="#E67E22"
          />
          <StatCard
            label="Products with Actions"
            value={Object.keys(recsByProduct).length}
            icon={TrendingUp}
            color="#27AE60"
          />
        </div>

        {/* Tabs */}
        <div className="flex gap-2 border-b border-gray-100">
          {(
            [
              { id: "summary", label: "Executive Summary" },
              { id: "alerts", label: "Critical Alerts" },
              { id: "recommendations", label: "Key Recommendations" },
            ] as const
          ).map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`px-4 py-3 text-sm font-medium border-b-2 transition ${
                tab === t.id
                  ? "border-[#9B1535] text-[#9B1535]"
                  : "border-transparent text-gray-600 hover:text-gray-900"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="space-y-4">
            {Array(3).fill(0).map((_, i) => (
              <div key={i} className="bg-white rounded-xl border p-5 animate-pulse h-20" />
            ))}
          </div>
        ) : tab === "summary" ? (
          <div className="space-y-4">
            <div className="bg-gradient-to-br from-[#7A0E28] to-[#9B1535] rounded-xl p-6 text-white shadow-lg">
              <h3 className="text-lg font-bold mb-3">Current Status Overview</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-3xl font-bold">{unresolvedAlerts.length}</div>
                  <div className="text-sm text-white/80">Unresolved Issues</div>
                </div>
                <div>
                  <div className="text-3xl font-bold">{unacknowledgedRecs.length}</div>
                  <div className="text-sm text-white/80">Pending Actions</div>
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-white/20">
                <p className="text-sm">
                  {criticalAlerts.length > 0
                    ? `⚠️ URGENT: ${criticalAlerts.length} critical alert(s) require immediate attention`
                    : "✓ No critical alerts at this time"}
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {/* Top Issues */}
              <div className="bg-white rounded-xl border border-gray-100 shadow-card p-5">
                <h3 className="text-sm font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <AlertTriangle size={16} className="text-[#8B1A1A]" />
                  Top Issues by Product
                </h3>
                <div className="space-y-3">
                  {Object.entries(alertsByProduct)
                    .sort((a: any, b: any) => b[1].length - a[1].length)
                    .slice(0, 5)
                    .map(([product, prods]: any) => (
                      <div
                        key={product}
                        className="flex items-center justify-between p-3 bg-red-50 rounded-lg border border-red-100"
                      >
                        <div>
                          <div className="text-xs font-semibold text-gray-900">{product}</div>
                          <div className="text-[10px] text-gray-500">
                            {prods.length} alert{prods.length !== 1 ? "s" : ""}
                          </div>
                        </div>
                        <div className="text-lg font-bold text-[#8B1A1A]">{prods.length}</div>
                      </div>
                    ))}
                </div>
              </div>

              {/* Top Recommendations */}
              <div className="bg-white rounded-xl border border-gray-100 shadow-card p-5">
                <h3 className="text-sm font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <Lightbulb size={16} className="text-[#9B1535]" />
                  Recommended Actions by Product
                </h3>
                <div className="space-y-3">
                  {Object.entries(recsByProduct)
                    .sort((a: any, b: any) => b[1].length - a[1].length)
                    .slice(0, 5)
                    .map(([product, prods]: any) => (
                      <div
                        key={product}
                        className="flex items-center justify-between p-3 bg-blue-50 rounded-lg border border-blue-100"
                      >
                        <div>
                          <div className="text-xs font-semibold text-gray-900">{product}</div>
                          <div className="text-[10px] text-gray-500">
                            {prods.length} recommendation{prods.length !== 1 ? "s" : ""}
                          </div>
                        </div>
                        <div className="text-lg font-bold text-[#9B1535]">{prods.length}</div>
                      </div>
                    ))}
                </div>
              </div>
            </div>
          </div>
        ) : tab === "alerts" ? (
          <div className="space-y-3">
            {criticalAlerts.length === 0 ? (
              <div className="bg-white rounded-xl border p-10 text-center text-gray-400">
                No critical unresolved alerts
              </div>
            ) : (
              criticalAlerts.map((a) => (
                <div key={a.id} className="bg-white rounded-xl border border-gray-100 p-5 shadow-card">
                  <div className="flex items-start gap-4">
                    <div className="flex-shrink-0">
                      <SeverityBadge severity={a.severity} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-xs font-bold text-gray-700">{a.product_name}</span>
                        <span className="text-gray-300">·</span>
                        <span className="text-[10px] text-gray-400">{a.period_date}</span>
                      </div>
                      <h4 className="text-sm font-semibold text-gray-900">{a.title}</h4>
                      <p className="text-xs text-gray-600 mt-1">{a.message}</p>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        ) : (
          <div className="space-y-3">
            {highPriorityRecs.length === 0 ? (
              <div className="bg-white rounded-xl border p-10 text-center text-gray-400">
                No high priority pending recommendations
              </div>
            ) : (
              highPriorityRecs.map((r) => (
                <div key={r.id} className="bg-white rounded-xl border border-gray-100 p-5 shadow-card">
                  <div className="flex items-start gap-4">
                    <div className="flex-shrink-0 w-2 h-2 rounded-full bg-[#9B1535] mt-1.5" />
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-[#FDECEA] text-[#8B1A1A]">
                          {r.priority}
                        </span>
                        <span className="text-xs font-bold text-gray-700">{r.product_name}</span>
                        <span className="text-gray-300">·</span>
                        <span className="text-[10px] text-gray-400">{r.period_date}</span>
                      </div>
                      <h4 className="text-sm font-semibold text-gray-900">{r.title}</h4>
                      <p className="text-xs text-gray-600 mt-1">{r.description}</p>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}
