# -*- coding: utf-8 -*-
import json
from client import GenParkCrossPlatformAllocator

allocator = GenParkCrossPlatformAllocator()

# 1. Markowitz Ad Budget Portfolio Optimization
channels = [
    {"name": "Google Search Ads", "expected_roas": 4.5, "roas_volatility_std": 0.3},
    {"name": "Meta Advantage+ Feed", "expected_roas": 3.8, "roas_volatility_std": 0.5},
    {"name": "TikTok Spark Ads", "expected_roas": 3.2, "roas_volatility_std": 0.8},
    {"name": "Amazon Sponsored Products", "expected_roas": 4.8, "roas_volatility_std": 0.4}
]
portfolio = allocator.optimize_markowitz_ad_budget(channels, total_budget_usd=60000.0, risk_aversion_lambda=0.5)
print(f"Ad Portfolio: Budget=${portfolio['total_budget_usd']} | Blended ROAS={portfolio['blended_portfolio_roas']} | Total Revenue=${portfolio['total_projected_revenue_usd']}")
for c in portfolio["channel_allocations"]:
    print(f"  {c['channel_name']}: ${c['allocated_budget_usd']} ({c['budget_share_pct']}%) -> Exp Rev: ${c['expected_revenue_usd']}")

# 2. Diminishing Marginal ROAS Saturation Curve
curve = allocator.calculate_diminishing_marginal_roas_curve(channel_budget_usd=25000.0, roas_base=4.8, saturation_scale_k=20000.0)
print()
print(f"Hill Saturation: Current ROAS={curve['current_effective_roas']} (Marginal Next 1K: {curve['marginal_roas_next_1k']}) | Saturation: {curve['saturation_level_pct']}% ({curve['efficiency_status']})")

# 3. Spend Drift & Rebalance Detection
target = {"Google": 25000.0, "Meta": 20000.0, "TikTok": 15000.0}
actual = {"Google": 28000.0, "Meta": 16000.0, "TikTok": 16000.0}
rebalance = allocator.rebalance_cross_platform_discrepancy(target, actual, tolerance_pct=4.0)
print()
print(f"Rebalance Drift Audit: {rebalance['channels_out_of_bounds_count']} channels out of bounds:")
for ch in rebalance["channel_audits"]:
    print(f"  {ch['channel']}: Drift={ch['dollar_drift']} ({ch['share_drift_pct']}%) -> {ch['action']}")
