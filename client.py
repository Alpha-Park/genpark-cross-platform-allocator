# -*- coding: utf-8 -*-
"""
GenPark Cross-Platform Allocator Client
Zero-dependency Markowitz mean-variance ad budget optimizer, diminishing marginal ROAS
Hill saturation modeler, and cross-channel spend rebalancing engine.
"""

import math
from typing import Dict, List, Any, Optional

class GenParkCrossPlatformAllocator:
    """
    Optimizes multi-channel advertising budgets using Markowitz modern portfolio theory,
    models diminishing marginal ROAS saturation curves, and detects spend drift.
    """

    def optimize_markowitz_ad_budget(
        self,
        channels: List[Dict[str, Any]],
        total_budget_usd: float = 50000.0,
        risk_aversion_lambda: float = 0.5
    ) -> Dict[str, Any]:
        """
        Solves convex budget allocation maximizing Risk-Adjusted ROAS:
        Utility = ROAS - lambda * Variance
        Allocation weight w_i proportional to (roas_i - lambda * var_i)
        """
        if total_budget_usd <= 0 or not channels:
            raise ValueError("Budget must be positive and channels list cannot be empty.")

        # Compute raw utility weights
        raw_weights = []
        for ch in channels:
            roas = ch.get("expected_roas", 3.0)
            volatility = ch.get("roas_volatility_std", 0.5)
            variance = volatility ** 2
            
            utility = max(0.1, roas - risk_aversion_lambda * variance)
            raw_weights.append(utility)

        total_weight = sum(raw_weights)
        allocations = []
        blended_roas = 0.0

        for ch, w in zip(channels, raw_weights):
            weight_ratio = w / total_weight
            allocated_budget = round(total_budget_usd * weight_ratio, 2)
            roas = ch.get("expected_roas", 3.0)
            expected_rev = round(allocated_budget * roas, 2)
            blended_roas += roas * weight_ratio

            allocations.append({
                "channel_name": ch.get("name", "channel"),
                "allocated_budget_usd": allocated_budget,
                "budget_share_pct": round(weight_ratio * 100.0, 1),
                "expected_roas": roas,
                "expected_revenue_usd": expected_rev
            })

        total_expected_revenue = sum(a["expected_revenue_usd"] for a in allocations)

        return {
            "total_budget_usd": total_budget_usd,
            "risk_aversion_lambda": risk_aversion_lambda,
            "blended_portfolio_roas": round(blended_roas, 3),
            "total_projected_revenue_usd": round(total_expected_revenue, 2),
            "channel_allocations": allocations
        }

    def calculate_diminishing_marginal_roas_curve(
        self,
        channel_budget_usd: float,
        roas_base: float = 4.5,
        saturation_scale_k: float = 20000.0,
        gamma: float = 1.2
    ) -> Dict[str, Any]:
        """
        Models diminishing marginal ROAS using the Hill function:
        ROAS(B) = roas_base / (1 + (B / K)^gamma)
        """
        if channel_budget_usd <= 0 or saturation_scale_k <= 0:
            raise ValueError("Budget and saturation scale must be positive.")

        ratio = channel_budget_usd / saturation_scale_k
        current_roas = round(roas_base / (1.0 + math.pow(ratio, gamma)), 3)
        total_revenue = round(channel_budget_usd * current_roas, 2)

        # Marginal ROAS approximation (dRev / dB at +$1000)
        delta_b = 1000.0
        next_b = channel_budget_usd + delta_b
        next_ratio = next_b / saturation_scale_k
        next_roas = roas_base / (1.0 + math.pow(next_ratio, gamma))
        next_rev = next_b * next_roas
        marginal_roas = round((next_rev - total_revenue) / delta_b, 3)

        saturation_pct = round(min(100.0, 100.0 * (1.0 - (current_roas / roas_base))), 1)

        return {
            "channel_budget_usd": channel_budget_usd,
            "base_unconstrained_roas": roas_base,
            "current_effective_roas": current_roas,
            "marginal_roas_next_1k": marginal_roas,
            "total_projected_revenue_usd": total_revenue,
            "saturation_level_pct": saturation_pct,
            "efficiency_status": "HIGHLY_EFFICIENT" if marginal_roas >= 2.0 else ("SATURATION_WARNING" if marginal_roas >= 1.0 else "DIMINISHING_RETURNS_EXHAUSTED")
        }

    def rebalance_cross_platform_discrepancy(
        self,
        target_allocation: Dict[str, float],
        actual_spend: Dict[str, float],
        tolerance_pct: float = 5.0
    ) -> Dict[str, Any]:
        """
        Detects drift between target budget allocation and actual spend, generating corrective transfer actions.
        """
        all_channels = sorted(list(set(target_allocation.keys()).union(set(actual_spend.keys()))))
        total_target = sum(target_allocation.values())
        total_actual = sum(actual_spend.values())

        discrepancies = []
        rebalance_actions = []

        for ch in all_channels:
            t_usd = target_allocation.get(ch, 0.0)
            a_usd = actual_spend.get(ch, 0.0)

            t_share = (t_usd / max(1e-9, total_target)) * 100.0
            a_share = (a_usd / max(1e-9, total_actual)) * 100.0
            drift_pct = round(a_share - t_share, 2)
            dollar_diff = round(a_usd - t_usd, 2)

            is_out_of_bounds = abs(drift_pct) > tolerance_pct

            if drift_pct > tolerance_pct:
                action = f"DECREASE_SPEND: Trim ${abs(dollar_diff):.2f} (over by {drift_pct}%)"
            elif drift_pct < -tolerance_pct:
                action = f"INCREASE_SPEND: Allocate +${abs(dollar_diff):.2f} (under by {abs(drift_pct)}%)"
            else:
                action = "ON_TARGET: Maintain current pacing"

            discrepancies.append({
                "channel": ch,
                "target_usd": t_usd,
                "actual_usd": a_usd,
                "dollar_drift": dollar_diff,
                "share_drift_pct": drift_pct,
                "requires_rebalance": is_out_of_bounds,
                "action": action
            })

        return {
            "total_target_budget_usd": round(total_target, 2),
            "total_actual_spend_usd": round(total_actual, 2),
            "tolerance_threshold_pct": tolerance_pct,
            "channels_out_of_bounds_count": sum(1 for d in discrepancies if d["requires_rebalance"]),
            "channel_audits": discrepancies
        }
