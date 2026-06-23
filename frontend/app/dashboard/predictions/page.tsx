"use client";
import { useEffect, useState, useCallback } from "react";
import { TrendingUp } from "lucide-react";
import Header from "@/components/layout/Header";
import TierBadge from "@/components/dashboard/TierBadge";
import api from "@/lib/api";
import { formatScore } from "@/lib/utils";
import { useRefresh } from "@/lib/use-refresh";
import { toast } from "sonner";

interface Prediction {
  id: number;
  product_id: number;
  period_date: string;
  predicted_score: number;
  predicted_tier: string;
  prediction_horizon_days: number;
  confidence: number;
  model_version: string;
  created_at: string;
}

export default function PredictionsPage() {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [products, setProducts] = useState<Record<number, string>>({});
  const [filterProduct, setFilterProduct] = useState<number | "">("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    try {
      const [predictionsRes, productsRes] = await Promise.all([
        api.get("/ml/predictions/bulk"),
        api.get("/products/"),
      ]);
      setPredictions(predictionsRes.data || []);
      const pMap: Record<number, string> = {};
      productsRes.data.forEach((p: any) => {
        pMap[p.id] = p.name;
      });
      setProducts(pMap);
    } catch (error: any) {
      const msg = error?.response?.data?.detail || "Failed to load predictions";
      toast.error(msg);
      setPredictions([]); // Show empty state instead of breaking
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);
  useRefresh(load);

  const filtered = filterProduct
    ? predictions.filter((p) => p.product_id === Number(filterProduct))
    : predictions;

  // Group by product
  const byProduct = filtered.reduce((acc: any, p) => {
    if (!acc[p.product_id]) acc[p.product_id] = [];
    acc[p.product_id].push(p);
    return acc;
  }, {});

  return (
    <div>
      <Header
        title="Predictions & Forecast"
        subtitle="3-month forward predictions for all digital banking products"
      />
      <div className="p-6">
        <div className="mb-4 flex items-center gap-3">
          <select
            value={filterProduct}
            onChange={(e) =>
              setFilterProduct(e.target.value === "" ? "" : Number(e.target.value))
            }
            className="text-xs border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-[#9B1535]"
          >
            <option value="">All Products</option>
            {Object.entries(products).map(([id, name]) => (
              <option key={id} value={id}>
                {name}
              </option>
            ))}
          </select>
          <span className="text-xs text-gray-400">{filtered.length} predictions</span>
        </div>

        {loading ? (
          <div className="space-y-3">
            {Array(4).fill(0).map((_, i) => (
              <div key={i} className="bg-white rounded-xl border p-4 animate-pulse h-24" />
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="bg-white rounded-xl border border-gray-100 p-10 text-center">
            <div className="text-4xl mb-3">📊</div>
            <p className="text-gray-500 text-sm">No predictions available yet</p>
            <p className="text-gray-400 text-xs mt-2">Upload data via Settings to generate predictions</p>
          </div>
        ) : (
          <div className="space-y-4">
            {Object.entries(byProduct).map(([productId, preds]: [string, any]) => (
              <div
                key={productId}
                className="bg-white rounded-xl border border-gray-100 shadow-card overflow-hidden"
              >
                <div className="px-5 py-4 border-b border-gray-100 bg-[#FBF0F3]">
                  <h3 className="text-sm font-semibold text-gray-900">
                    {products[Number(productId)] || `Product ${productId}`}
                  </h3>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="bg-gray-50">
                        {[
                          "Prediction Date",
                          "Horizon",
                          "Predicted Score",
                          "Tier",
                          "Confidence",
                          "Model",
                          "Generated",
                        ].map((h, idx) => (
                          <th
                            key={`header-${idx}-${h}`}
                            className="px-4 py-3 text-left text-[10px] font-semibold text-gray-500 uppercase tracking-wide"
                          >
                            {h}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-50">
                      {preds.map((p: Prediction) => (
                        <tr key={p.id} className="hover:bg-gray-50 transition">
                          <td className="px-4 py-3 text-xs text-gray-900 font-medium">
                            {p.period_date}
                          </td>
                          <td className="px-4 py-3 text-xs text-gray-500">
                            {p.prediction_horizon_days} days
                          </td>
                          <td className="px-4 py-3">
                            <span className="text-sm font-bold text-[#9B1535]">
                              {formatScore(p.predicted_score)}
                            </span>
                          </td>
                          <td className="px-4 py-3">
                            <TierBadge tier={p.predicted_tier} size="sm" />
                          </td>
                          <td className="px-4 py-3 text-xs font-medium">
                            <div className="flex items-center gap-2">
                              <div className="w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                                <div
                                  className="h-full bg-[#9B1535] rounded-full"
                                  style={{
                                    width: `${(p.confidence || 0) * 100}%`,
                                  }}
                                />
                              </div>
                              <span className="text-[10px] text-gray-500">
                                {((p.confidence || 0) * 100).toFixed(0)}%
                              </span>
                            </div>
                          </td>
                          <td className="px-4 py-3 text-[10px] text-gray-400 font-mono">
                            {p.model_version}
                          </td>
                          <td className="px-4 py-3 text-[10px] text-gray-400">
                            {p.created_at?.slice(0, 10)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
