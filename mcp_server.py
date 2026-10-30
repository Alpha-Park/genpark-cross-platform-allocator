# -*- coding: utf-8 -*-
"""
GenPark Cross-Platform Allocator FastMCP Server
"""

import json
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP
from client import GenParkCrossPlatformAllocator

mcp = FastMCP("genpark-cross-platform-allocator")
allocator = GenParkCrossPlatformAllocator()

@mcp.tool()
def optimize_markowitz_ad_budget(
    channels_json: str,
    total_budget_usd: float = 50000.0,
    risk_aversion_lambda: float = 0.5
) -> str:
    """
    Solves convex budget allocation maximizing Risk-Adjusted ROAS.
    """
    channels = json.loads(channels_json)
    res = allocator.optimize_markowitz_ad_budget(channels, total_budget_usd, risk_aversion_lambda)
    return json.dumps(res, indent=2)

@mcp.tool()
def calculate_diminishing_marginal_roas_curve(
    channel_budget_usd: float,
    roas_base: float = 4.5,
    saturation_scale_k: float = 20000.0,
    gamma: float = 1.2
) -> str:
    """
    Models diminishing marginal ROAS using the Hill saturation function.
    """
    res = allocator.calculate_diminishing_marginal_roas_curve(channel_budget_usd, roas_base, saturation_scale_k, gamma)
    return json.dumps(res, indent=2)

@mcp.tool()
def rebalance_cross_platform_discrepancy(
    target_allocation_json: str,
    actual_spend_json: str,
    tolerance_pct: float = 5.0
) -> str:
    """
    Detects drift between target budget allocation and actual spend.
    """
    target = json.loads(target_allocation_json)
    actual = json.loads(actual_spend_json)
    res = allocator.rebalance_cross_platform_discrepancy(target, actual, tolerance_pct)
    return json.dumps(res, indent=2)

def main():
    print("Testing Cross-Platform Allocator:")
    ch = [{"name": "Meta Ads", "expected_roas": 3.8, "roas_volatility_std": 0.4}, {"name": "Google Ads", "expected_roas": 4.2, "roas_volatility_std": 0.6}]
    print(optimize_markowitz_ad_budget(json.dumps(ch), 10000.0))

if __name__ == "__main__":
    main()
