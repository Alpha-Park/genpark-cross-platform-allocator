# genpark-cross-platform-allocator

![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![MCP Dependency](https://img.shields.io/badge/MCP-mcp%20SDK-blue)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

GenPark Cross-Platform Allocator is a quantitative paid media and performance marketing optimization engine implementing Markowitz Modern Portfolio Theory for ad budget distribution, Hill function diminishing marginal ROAS curves, and automated cross-channel spend drift rebalancing.

```mermaid
flowchart LR
    A[Channel ROAS & Volatilities] --> B[Markowitz Mean-Variance Portfolio Engine]
    B --> C[Risk-Adjusted Optimal Budget Share]
    D[Incremental Channel Spend] --> E[Hill Function Saturation Model]
    E --> F[Marginal ROAS & Diminishing Return Warning]
    G[Target Allocation vs Actual Spend] --> H[Cross-Platform Rebalancing Engine]
    H --> I[Pacing Correction & Capital Reallocation]
```

## Features
- **Markowitz Mean-Variance Ad Portfolio**: Optimizes multi-channel spend based on expected ROAS and channel volatility trade-offs.
- **Hill Function Saturation Modeling**: Detects marginal efficiency decay ($dRev / dB$) to prevent ad spend waste above saturation thresholds.
- **Cross-Platform Rebalancing**: Identifies pacing drift across Google, Meta, TikTok, and Amazon to issue corrective capital adjustments.

## MCP Runtime Requirements

Use Python 3.10+ for the MCP server. The core `client.py` has no external dependencies; MCP transport requires `mcp>=1.0.0,<2`. From this checkout, install it into the Python environment used by your MCP client:

```bash
python -m pip install -r requirements.txt
```

Use the same Python interpreter to launch `mcp_server.py`. In desktop client configuration, set `command` to that interpreter's absolute path.

## Quickstart

```python
from client import GenParkCrossPlatformAllocator

allocator = GenParkCrossPlatformAllocator()
res = allocator.optimize_markowitz_ad_budget(
    [{"name": "Google", "expected_roas": 4.5, "roas_volatility_std": 0.3},
     {"name": "Meta", "expected_roas": 3.8, "roas_volatility_std": 0.5}],
    total_budget_usd=10000.0
)
print("Blended ROAS:", res["blended_portfolio_roas"])
```

## Local MCP Server

After installing the MCP requirements, launch the local STDIO server:

```bash
python mcp_server.py
```

Point your MCP client at the absolute path to `mcp_server.py` using the same Python interpreter. This repository does not provide a hosted MCP endpoint.

## License
MIT
