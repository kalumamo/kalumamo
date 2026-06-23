"use client";
import { useEffect, useState, useCallback } from "react";
import { CheckCircle, X } from "lucide-react";
import Header from "@/components/layout/Header";
import api from "@/lib/api";
import { useRefresh } from "@/lib/use-refresh";
import { toast } from "sonner";

interface Recommendation {
  id: number;
  product_name: string;
  category: string;
  priority: string;
  title: string;
  description: string;
  trigger_metric: string;
  trigger_value: number;
  ai_explanation: string;
  is_acknowledged: boolean;
  period_date: string;
}

const PRIORITY_STYLES: Record<string, string> = {
  critical: "border-l-4 border-[#8B1A1A]",
  high: "border-l-4 border-[#7A3A00]",
  medium: "border-l-4 border-[#7A5C00]",
  low: "border-l-4 border-[#1A4A2A]",
};

const PRIORITY_BADGE: Record<string, string> = {
  critical: "text-[#8B1A1A] bg-[#FDECEA]",
  high: "text-[#7A3A00] bg-[#FFF0E6]",
  medium: "text-[#7A5C00] bg-[#FFF8E1]",
  low: "text-[#1A4A2A] bg-[#E8F5ED]",
};

export default function RecommendationsPage() {
  const [recs, setRecs] = useState<Recommendation[]>([]);
  const [filterPriority, setFilterPriority] = useState("");
  const [filterProduct, setFilterProduct] = useState("");
  const [showAck, setShowAck] = useState(false);
  const [loading, setLoading] = useState(true);
  const [selectedRec, setSelectedRec] = useState<Recommendation | null>(null);

  const load = useCallback(async () => {
    try {
      let url = `/recommendations/?limit=100`;
      if (filterPriority) url += `&priority=${filterPriority}`;
      if (!showAck) url += `&is_acknowledged=false`;
      const res = await api.get(url);
      setRecs(res.data);
    } catch {
      toast.error("Failed to load recommendations");
    } finally {
      setLoading(false);
    }
  }, [filterPriority, showAck]);

  useEffect(() => { load(); }, [load]);
  useRefresh(load);

  const acknowledge = async (id: number) => {
    try {
      await api.post(`/recommendations/${id}/acknowledge`);
      toast.success("Recommendation acknowledged");
      load();
    } catch {
      toast.error("Failed to acknowledge");
    }
  };

  const filtered = recs.filter((r) =>
    !filterProduct || r.product_name.toLowerCase().includes(filterProduct.toLowerCase())
  );

  return (
    <div>
      <Header title="AI Recommendations" subtitle="Data-driven improvement recommendations for each product" />
      <div className="p-6 space-y-5">
        {/* Filters */}
        <div className="bg-white rounded-xl border border-gray-100 p-4 flex flex-wrap gap-3 items-center">
          <select value={filterPriority} onChange={(e) => setFilterPriority(e.target.value)}
            className="text-xs border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-[#9B1535]">
            <option value="">All Priorities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
          <input value={filterProduct} onChange={(e) => setFilterProduct(e.target.value)}
            placeholder="Filter by product..."
            className="text-xs border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-[#9B1535] w-44" />
          <label className="flex items-center gap-2 text-xs text-gray-600 cursor-pointer">
            <input type="checkbox" checked={showAck} onChange={(e) => setShowAck(e.target.checked)} className="accent-[#9B1535]" />
            Show Acknowledged
          </label>
          <span className="text-xs text-gray-400 ml-auto">{filtered.length} recommendations</span>
        </div>

        {loading ? (
          <div className="space-y-3">
            {Array(4).fill(0).map((_, i) => <div key={i} className="bg-white rounded-xl border p-5 animate-pulse h-28" />)}
          </div>
        ) : filtered.length === 0 ? (
          <div className="bg-white rounded-xl border p-10 text-center text-gray-400 text-sm">
            No recommendations found
          </div>
        ) : (
          <div className="space-y-3">
            {filtered.map((r) => (
              <div
                key={r.id}
                onClick={() => setSelectedRec(r)}
                className={`bg-white rounded-xl border border-gray-100 shadow-card overflow-hidden ${PRIORITY_STYLES[r.priority] || ""} ${
                  r.is_acknowledged ? "opacity-60" : ""
                } cursor-pointer transition-all hover:shadow-lg hover:border-[#9B1535]`}
              >
                <div className="p-5">
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${PRIORITY_BADGE[r.priority] || "bg-gray-100 text-gray-600"}`}>
                          {r.priority}
                        </span>
                        <span className="text-xs text-gray-400">{r.product_name}</span>
                        <span className="text-gray-200">·</span>
                        <span className="text-[10px] text-gray-400">{r.category.replace(/_/g, " ")}</span>
                      </div>
                      <h3 className="text-sm font-semibold text-gray-900 mb-1">{r.title}</h3>
                      <p className="text-xs text-gray-600">{r.description}</p>

                      {r.ai_explanation && (
                        <details className="mt-3">
                          <summary className="text-xs text-[#9B1535] cursor-pointer font-medium">AI Explanation ↓</summary>
                          <pre className="text-[10px] text-gray-500 mt-2 whitespace-pre-wrap font-sans leading-relaxed bg-[#FBF0F3] p-3 rounded-lg">
                            {r.ai_explanation}
                          </pre>
                        </details>
                      )}
                    </div>
                    {!r.is_acknowledged && (
                      <button onClick={() => acknowledge(r.id)}
                        className="flex-shrink-0 flex items-center gap-1.5 text-xs text-[#9B1535] hover:text-[#7A0E28] font-medium px-3 py-1.5 border border-[#BE1B3C] rounded-lg hover:bg-[#FBF0F3] transition">
                        <CheckCircle size={13} /> Acknowledge
                      </button>
                    )}
                    {r.is_acknowledged && (
                      <span className="text-[10px] text-green-700 bg-green-50 px-2 py-1 rounded-full font-medium flex-shrink-0">Acknowledged</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recommendation Details Modal */}
      {selectedRec && (
      <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
          {/* Header */}
          <div className="sticky top-0 bg-gradient-to-r from-[#7A0E28] to-[#9B1535] px-6 py-5 flex items-start justify-between border-b border-white/10">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <span
                  className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${
                    PRIORITY_BADGE[selectedRec.priority] || "bg-gray-100 text-gray-600"
                  }`}
                >
                  {selectedRec.priority}
                </span>
                <span className="text-xs font-semibold text-white/70">
                  {selectedRec.category.replace(/_/g, " ")}
                </span>
              </div>
              <h2 className="text-lg font-bold text-white">{selectedRec.title}</h2>
            </div>
            <button
              onClick={() => setSelectedRec(null)}
              className="flex-shrink-0 text-white/60 hover:text-white transition"
            >
              <X size={24} />
            </button>
          </div>

          {/* Content */}
          <div className="p-6 space-y-6">
            {/* Product & Date */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide font-semibold mb-1">
                  Product
                </p>
                <p className="text-sm font-semibold text-gray-900">{selectedRec.product_name}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide font-semibold mb-1">
                  Period
                </p>
                <p className="text-sm font-semibold text-gray-900">{selectedRec.period_date}</p>
              </div>
            </div>

            {/* Description */}
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wide font-semibold mb-2">
                Description
              </p>
              <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <p className="text-sm text-gray-700 leading-relaxed">{selectedRec.description}</p>
              </div>
            </div>

            {/* Trigger Information */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide font-semibold mb-2">
                  Trigger Metric
                </p>
                <p className="text-sm font-semibold text-gray-900">
                  {selectedRec.trigger_metric.replace(/_/g, " ")}
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide font-semibold mb-2">
                  Trigger Value
                </p>
                <p className="text-lg font-bold text-[#9B1535]">{selectedRec.trigger_value}</p>
              </div>
            </div>

            {/* AI Explanation */}
            {selectedRec.ai_explanation && (
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wide font-semibold mb-2">
                  AI Analysis
                </p>
                <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                  <p className="text-sm text-blue-900 leading-relaxed">{selectedRec.ai_explanation}</p>
                </div>
              </div>
            )}

            {/* Status */}
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wide font-semibold mb-2">
                Status
              </p>
              <div>
                {selectedRec.is_acknowledged ? (
                  <span className="inline-flex items-center gap-2 px-3 py-1.5 bg-green-50 text-green-700 rounded-full text-xs font-semibold border border-green-200">
                    <CheckCircle size={14} /> Acknowledged
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-2 px-3 py-1.5 bg-yellow-50 text-yellow-700 rounded-full text-xs font-semibold border border-yellow-200">
                    <div className="w-2 h-2 rounded-full bg-yellow-700 animate-pulse" />
                    Pending
                  </span>
                )}
              </div>
            </div>

            {/* Actions */}
            {!selectedRec.is_acknowledged && (
              <div className="flex gap-3 pt-4 border-t border-gray-200">
                <button
                  onClick={async () => {
                    try {
                      await api.post(`/recommendations/${selectedRec.id}/acknowledge`);
                      toast.success("Recommendation acknowledged");
                      setSelectedRec(null);
                      await load();
                    } catch {
                      toast.error("Failed to acknowledge");
                    }
                  }}
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-[#7A0E28] hover:bg-[#9B1535] text-white rounded-lg font-semibold text-sm transition"
                >
                  <CheckCircle size={16} /> Acknowledge
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    )}
    </div>
  );
}
