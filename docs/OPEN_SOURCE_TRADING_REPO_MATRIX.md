# Open-Source Trading Repository Integration Matrix

This file records what should be used, studied, isolated or avoided when building the project.

| Repository | Role | Planned treatment | License / commercial note |
|---|---|---|---|
| nautechsystems/nautilus_trader | Execution + event architecture | Study deeply; integrate only through owned interfaces | LGPL-3.0; legal review before linking/embedding |
| QuantConnect/Lean | Backtest/live engine reference | Study architecture; selectively integrate concepts | Apache-2.0 |
| vnpy/vnpy | Full trading application architecture | Study modules and gateway patterns | MIT |
| ccxt/ccxt | Crypto exchange connectivity | Adapter/reference | MIT |
| hummingbot/hummingbot | Connector/order execution reference | Study and isolate | Apache-2.0 |
| microsoft/qlib | Quant research | Research service/reference | MIT |
| AI4Finance-Foundation/FinRL-Trading | AI trading research | Research layer/reference | Apache-2.0 |
| microsoft/RD-Agent | Automated quant R&D | Research-agent reference | Check repository license before reuse |
| optuna/optuna | Optimization | Direct dependency candidate | MIT |
| TA-Lib/ta-lib-python | Technical indicators | Direct dependency candidate | BSD-2-Clause |
| joshyattridge/smart-money-concepts | SMC calculations | Reference only until independently validated | Check repository license before reuse |
| PyPortfolio/PyPortfolioOpt | Portfolio optimization | Direct dependency candidate | MIT |
| ranaroussi/quantstats | Performance analytics | Direct dependency candidate/reference | Check exact version/license before distribution |
| tradingview/lightweight-charts | Charting | Frontend dependency | Apache-2.0 plus TradingView attribution requirements |
| freqtrade/freqtrade | Crypto bot | Study/reference; do not make proprietary core dependent without legal plan | GPL-3.0 |
| mementum/backtrader | Backtesting | Historical/reference only for this architecture | GPL-3.0 |
| kernc/backtesting.py | Backtesting | Research/reference; isolate if used | AGPL-3.0 |
| polakowo/vectorbt | Research/sweeps | Useful for research, but review commercial restrictions | Apache-2.0 + Commons Clause |

## Selection rule

Prefer permissive licenses for code that becomes part of the distributed proprietary product.

For restrictive-license repositories:
- use them as architecture/reference material;
- isolate them behind a separate service where appropriate;
- or obtain the required commercial licensing/legal approval before distribution.

Never assume that a repository being public or described as open source automatically permits incorporation into a proprietary product.

## Deep-study order

1. NautilusTrader
2. LEAN
3. VN.PY
4. Qlib
5. CCXT
6. Hummingbot
7. TA-Lib
8. PyPortfolioOpt
9. Optuna
10. Lightweight Charts
11. FinRL-Trading
12. SMC repository

## Validation checklist for every candidate repository

- Is the repository actively maintained?
- What is the exact license at the commit/version we use?
- Can the dependency be imported without infecting the proprietary application with incompatible licensing requirements?
- Does it introduce look-ahead bias or repainting?
- Does it assume crypto-only or exchange-specific semantics?
- Does it handle partial fills and cancellations?
- Does it model fees, spread and slippage?
- Can it run deterministically in backtests?
- Can its state be persisted and recovered?
- Can we replace it later without redesigning our public application APIs?
