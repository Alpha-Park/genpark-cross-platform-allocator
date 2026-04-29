---
name: genpark-cross-platform-allocator
description: Dynamically reallocates ad spend across Meta, Google, and TikTok based on real-time ROAS and CPA efficiency.
---

# GenPark Cross-Platform Spend Allocator

## Overview
Inspired by GrowthGPT's cross-platform data insights, this GenPark skill intelligently routes budget to the most efficient acquisition channels. Rather than waiting for manual weekly reviews, the agent constantly analyzes cross-channel performance and shifts spend from underperforming channels to high-performing ones.

## Capabilities
- **Cross-Channel Normalization**: Standardizes CPA and ROAS metrics across Meta, Google, and TikTok to ensure apples-to-apples comparison.
- **Efficiency Detection**: Identifies channels that are "underweighted" (e.g., generating 68% of conversions on only 42% of spend) and suggests or executes budget shifts.
- **Trend Spotting**: Detects early warning signs, such as rising CPCs on Google or emerging efficiency on TikTok, enabling proactive strategy adjustments.

## Usage Instructions
1. Connect the agent to all active marketing channels and an aggregate data source (like Google Analytics or Shopify) to verify source-of-truth conversions.
2. Define total cross-platform budget caps.
3. The agent will output an updated allocation matrix and execute the budget transfers via the respective APIs.
