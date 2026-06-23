"""
Recommendation Engine - Rule-based with AI-style explanations.
"""
from typing import List
from datetime import date
from sqlalchemy.orm import Session

from app.models.data import ProcessedFeatures, RawData
from app.models.ml_models import Score
from app.models.recommendations import Recommendation
from app.models.alerts import Alert
import logging

logger = logging.getLogger(__name__)

# Rule definitions: (condition_fn, category, priority, title, description_template)
RULES = [
    {
        "id": "high_failure_rate",
        "metric": "transaction_success_rate",
        "condition": lambda v: v is not None and v < 0.90,
        "category": "transaction_reliability",
        "priority": "critical",
        "title": "Reduce Transaction Failure Rate",
        "description": (
            "Transaction success rate is {value:.1%}, below the 90% threshold. "
            "Investigate payment gateway errors, timeout configurations, and "
            "network reliability. Target: >95% success rate within 30 days."
        ),
    },
    {
        "id": "high_downtime",
        "metric": "downtime_impact_score",
        "condition": lambda v: v is not None and v > 0.05,
        "category": "infrastructure",
        "priority": "high",
        "title": "Improve Infrastructure Reliability",
        "description": (
            "Downtime impact score is {value:.1%}. System availability is below acceptable levels. "
            "Review server health, implement redundancy, and establish SLA-based monitoring. "
            "Target: 99.9% uptime."
        ),
    },
    {
        "id": "low_engagement",
        "metric": "active_user_rate",
        "condition": lambda v: v is not None and v < 0.40,
        "category": "user_adoption",
        "priority": "high",
        "title": "Improve User Adoption and Engagement",
        "description": (
            "Active user rate is {value:.1%}, significantly below the 40% target. "
            "Launch targeted user adoption campaigns, improve onboarding flows, "
            "and introduce loyalty incentives to drive engagement."
        ),
    },
    {
        "id": "complaint_surge",
        "metric": "complaint_growth_rate",
        "condition": lambda v: v is not None and v > 0.20,
        "category": "customer_satisfaction",
        "priority": "high",
        "title": "Address Rising Customer Complaint Volume",
        "description": (
            "Complaint growth rate is {value:.1%}. Unresolved complaints are accumulating. "
            "Prioritize complaint resolution, identify root causes, and implement "
            "proactive communication with affected customers."
        ),
    },
    {
        "id": "low_revenue_per_user",
        "metric": "revenue_per_active_user",
        "condition": lambda v: v is not None and v < 10.0,
        "category": "revenue_optimization",
        "priority": "medium",
        "title": "Optimize Revenue Per Active User",
        "description": (
            "Revenue per active user is ETB {value:.2f}, below the ETB 10 benchmark. "
            "Consider premium feature offerings, transaction fee optimization, "
            "and cross-selling digital banking products."
        ),
    },
    {
        "id": "low_operational_efficiency",
        "metric": "operational_efficiency_score",
        "condition": lambda v: v is not None and v < 0.70,
        "category": "operational_excellence",
        "priority": "medium",
        "title": "Enhance Operational Efficiency",
        "description": (
            "Operational efficiency score is {value:.1%}. Review transaction processing "
            "pipeline, response time optimization, and system resource allocation. "
            "Target: >85% operational efficiency."
        ),
    },
    {
        "id": "low_user_engagement_index",
        "metric": "user_engagement_index",
        "condition": lambda v: v is not None and v < 0.30,
        "category": "user_adoption",
        "priority": "medium",
        "title": "Boost User Engagement Index",
        "description": (
            "User engagement index is {value:.2f} (scale 0-1). Combined effect of low "
            "active user rate and transaction success. Focus on improving both UX and "
            "transaction reliability simultaneously."
        ),
    },
]

ALERT_RULES = [
    {
        "id": "score_drop",
        "condition": lambda score, prev: prev is not None and (prev - score) >= 10,
        "alert_type": "score_drop",
        "severity": "critical",
        "title": "Significant Performance Score Drop",
        "message": "Performance score dropped by {change:.1f} points from {prev:.1f} to {current:.1f}.",
    },
    {
        "id": "critical_downtime",
        "metric": "downtime_impact_score",
        "condition": lambda v: v is not None and v > 0.15,
        "alert_type": "downtime_spike",
        "severity": "critical",
        "title": "Critical Downtime Spike Detected",
        "message": "Downtime impact has reached {value:.1%}, exceeding the 15% critical threshold.",
    },
    {
        "id": "high_failure_alert",
        "metric": "transaction_success_rate",
        "condition": lambda v: v is not None and v < 0.85,
        "alert_type": "failure_rate_increase",
        "severity": "high",
        "title": "Transaction Failure Rate Critical",
        "message": "Transaction success rate fell to {value:.1%}. Immediate action required.",
    },
    {
        "id": "complaint_alert",
        "metric": "complaint_growth_rate",
        "condition": lambda v: v is not None and v > 0.30,
        "alert_type": "complaint_surge",
        "severity": "high",
        "title": "Complaint Volume Surge",
        "message": "Complaint growth rate reached {value:.1%}, indicating a customer satisfaction crisis.",
    },
]


class RecommendationService:

    def generate_for_product(
        self,
        db: Session,
        product_id: int,
        period_date: date,
        score_obj: Score,
        features: dict,
    ) -> List[Recommendation]:
        # ── Delete existing recommendations for this product+period first ──
        # This prevents duplicates when data is re-uploaded or re-processed.
        db.query(Recommendation).filter(
            Recommendation.product_id == product_id,
            Recommendation.period_date == period_date,
        ).delete()
        db.commit()

        recommendations = []

        for rule in RULES:
            metric = rule["metric"]
            value = features.get(metric)

            if rule["condition"](value):
                description = rule["description"].format(value=value or 0)
                rec = Recommendation(
                    product_id=product_id,
                    score_id=score_obj.id if score_obj else None,
                    period_date=period_date,
                    category=rule["category"],
                    priority=rule["priority"],
                    title=rule["title"],
                    description=description,
                    trigger_metric=metric,
                    trigger_value=value,
                    ai_explanation=self._generate_ai_explanation(
                        score_obj, features, rule
                    ),
                )
                recommendations.append(rec)
                db.add(rec)

        db.commit()
        return recommendations

    def generate_alerts(
        self,
        db: Session,
        product_id: int,
        period_date: date,
        score_obj: Score,
        features: dict,
    ) -> List[Alert]:
        # Delete existing alerts for this product+period to prevent duplicates on re-run
        db.query(Alert).filter(
            Alert.product_id == product_id,
            Alert.period_date == period_date,
        ).delete()
        db.commit()

        alerts = []

        # Score drop alert
        if score_obj.previous_score is not None and (score_obj.previous_score - score_obj.performance_score) >= 10:
            change = score_obj.previous_score - score_obj.performance_score
            alert = Alert(
                product_id=product_id,
                alert_type="score_drop",
                severity="critical",
                title="Significant Performance Score Drop",
                message=f"Performance score dropped by {change:.1f} points from {score_obj.previous_score:.1f} to {score_obj.performance_score:.1f}.",
                metric_name="performance_score",
                metric_value=score_obj.performance_score,
                previous_value=score_obj.previous_score,
                period_date=period_date,
            )
            alerts.append(alert)
            db.add(alert)

        # Feature-based alerts
        for rule in ALERT_RULES[1:]:  # Skip score_drop rule (already handled)
            metric = rule.get("metric")
            if not metric:
                continue
            value = features.get(metric)
            if rule["condition"](value):
                alert = Alert(
                    product_id=product_id,
                    alert_type=rule["alert_type"],
                    severity=rule["severity"],
                    title=rule["title"],
                    message=rule["message"].format(value=value or 0),
                    metric_name=metric,
                    metric_value=value,
                    threshold_value=0,
                    period_date=period_date,
                )
                alerts.append(alert)
                db.add(alert)

        db.commit()
        return alerts

    def _generate_ai_explanation(self, score_obj: Score, features: dict, rule: dict) -> str:
        score = score_obj.performance_score if score_obj else 0
        change = score_obj.score_change if score_obj else None

        parts = [f"Performance score: {score:.1f}/100"]
        if change:
            direction = "decreased" if change < 0 else "increased"
            parts.append(f"Score {direction} by {abs(change):.1f} points in the latest period.")

        # Identify top contributors
        contributors = []
        if (features.get("downtime_impact_score") or 0) > 0.05:
            contributors.append("increased system downtime")
        if (features.get("transaction_success_rate") or 1) < 0.90:
            contributors.append("elevated transaction failure rate")
        if (features.get("complaint_growth_rate") or 0) > 0.15:
            contributors.append("rising complaint volume")
        if (features.get("active_user_rate") or 1) < 0.40:
            contributors.append("declining active user base")

        if contributors:
            parts.append("Key contributing factors:")
            for i, c in enumerate(contributors, 1):
                parts.append(f"  {i}. {c.capitalize()}")

        parts.append(f"\nAction: {rule['title']}")
        return "\n".join(parts)


recommendation_service = RecommendationService()
