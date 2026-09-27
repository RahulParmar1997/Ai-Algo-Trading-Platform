# AI Algo Trading Platform — Reference Architecture

## Purpose

This document converts the open-source trading-system research into the target architecture for this project.

The platform is intended to support:

- Multi-asset market data
- Portfolio and positions
- Paper trading and live trading
- Deterministic risk controls
- Rule-based and quantitative strategies
- Technical analysis
- SMC/ICT-style market-structure analytics
- Backtesting and walk-forward validation
- ML/AI research and model inference
- Broker/exchange adapters
- TradingView-like charting, watchlists, scanners and alerts
- Separate user and admin applications

## Architecture principle

Do not turn the product into a fork of one trading-bot repository.

Own the application/domain layer and integrate specialized open-source capabilities behind stable internal interfaces.

Target flow:

market data
  -> normalized data model
  -> feature/indicator engine
  -> SMC/market-structure engine
  -> strategy engine
  -> ML/AI signal engine
  -> decision/ensemble engine
  -> risk engine
  -> order planner
  -> execution engine
  -> broker/exchange adapter
  -> broker/exchange

The live and backtest paths should share the same strategy, portfolio, risk and order semantics wherever practical.

## Recommended reference projects

### Core execution / event architecture

1. NautilusTrader
   - Study: event-driven architecture, execution, order state, venues, portfolio/account semantics, adapters, backtest/live parity.
   - Repository: https://github.com/nautechsystems/nautilus_trader

2. QuantConnect LEAN
   - Study: modular engine, brokerage abstraction, data feeds, indicators, optimization and research workflows.
   - Repository: https://github.com/QuantConnect/Lean

3. VN.PY / VeighNa
   - Study: modular trading application architecture, gateways, CTA strategy engine, portfolio, algo execution, risk and market-data applications.
   - Repository: https://github.com/vnpy/vnpy

### Connectivity

4. CCXT
   - Use/reference for crypto exchange normalization.
   - Repository: https://github.com/ccxt/ccxt

5. Hummingbot
   - Study: connector and execution architecture, order lifecycle and exchange/DEX integration patterns.
   - Repository: https://github.com/hummingbot/hummingbot

### Research / AI

6. Microsoft Qlib
   - Study: point-in-time data, factors, models, research workflows and quantitative experimentation.
   - Repository: https://github.com/microsoft/qlib

7. FinRL-Trading
   - Study: AI/quant strategy interface and deployment-oriented research.
   - Repository: https://github.com/AI4Finance-Foundation/FinRL-Trading

8. RD-Agent
   - Study: automated quantitative R&D and factor discovery workflows.
   - Repository: https://github.com/microsoft/RD-Agent

9. Optuna
   - Use/reference for hyperparameter and strategy optimization.
   - Repository: https://github.com/optuna/optuna

### Technical analysis

10. TA-Lib Python
    - Use for standard technical indicators and candlestick pattern functions.
    - Repository: https://github.com/TA-Lib/ta-lib-python

11. smart-money-concepts
    - Study/reference for BOS/CHoCH, order blocks, FVG, liquidity and related SMC calculations.
    - Repository: https://github.com/joshyattridge/smart-money-concepts
    - Requirement: independently validate all calculations for causality and no-lookahead behavior before using them in live signals.

### Portfolio / analytics

12. PyPortfolioOpt
    - Study/reference for allocation, covariance, Black-Litterman, HRP and portfolio constraints.
    - Repository: https://github.com/robertmartin8/PyPortfolioOpt

13. QuantStats
    - Study/reference for portfolio statistics and reporting.
    - Repository: https://github.com/ranaroussi/quantstats

### UI

14. TradingView Lightweight Charts
    - Use as the chart rendering foundation.
    - Repository: https://github.com/tradingview/lightweight-charts

## Internal modules to own

backend/app/
  api/
    auth.py
    dashboard.py
    market.py
    portfolio.py
    trading.py
    watchlists.py
    strategies.py
    backtest.py
    ai.py
    risk.py
    alerts.py
    admin/

  core/
    config.py
    security.py
    events.py
    errors.py
    logging.py

  models/
    user.py
    portfolio.py
    position.py
    order.py
    trade.py
    market_data.py
    strategy.py
    signal.py
    backtest.py
    broker.py
    risk.py
    alert.py

  schemas/
    ...

  services/
    market/
    portfolio/
    orders/
    execution/
    brokers/
    strategies/
    signals/
    indicators/
    smc/
    backtest/
    risk/
    ai/
    alerts/
    reporting/

  engine/
    event_bus/
    market/
    strategy/
    decision/
    risk/
    execution/
    portfolio/

  adapters/
    brokers/
      zerodha/
      upstox/
      dhan/
      angelone/
      fyers/
    exchanges/
      ccxt/

  research/
    datasets/
    features/
    factors/
    experiments/
    models/

## Execution contract

Every strategy must produce an internal signal/order-intent object, not a raw broker API request.

Example conceptual contract:

StrategySignal
  symbol
  timestamp
  side
  signal_type
  confidence
  expected_edge
  timeframe
  strategy_id
  feature_snapshot
  stop_reference
  target_reference
  expiry

The decision engine combines signals.

The risk engine is authoritative for:
- maximum position size
- maximum notional
- portfolio exposure
- per-symbol exposure
- daily loss limit
- drawdown limit
- leverage
- margin
- stop/target constraints
- trading session constraints
- kill switch

Only an approved OrderPlan reaches a broker adapter.

## AI safety boundary

AI/LLM components may:
- summarize market state
- propose strategies
- discover candidate features
- classify regimes
- rank candidate signals
- generate research code
- explain backtest results

AI/LLM components must not bypass:
- risk checks
- broker validation
- position limits
- order validation
- audit logging

Live order path:

AI/ML
  -> Signal
  -> Decision Engine
  -> Risk Engine
  -> Order Planner
  -> Broker Adapter
  -> Broker

## Backtest requirements

Backtest and live execution must share:

- symbol definitions
- strategy signal contracts
- portfolio accounting
- position accounting
- fees/slippage model
- order states
- risk limits
- time handling

The backtester must support:

- commissions
- slippage
- bid/ask or spread assumptions
- partial fills
- latency assumptions
- market/limit/stop orders
- session/calendar rules
- corporate-action handling where applicable
- survivorship-bias controls
- point-in-time data
- walk-forward testing
- out-of-sample validation
- Monte Carlo analysis

A high historical return alone must never be treated as evidence that a strategy is production ready.

## SMC/ICT implementation requirements

Treat SMC/ICT as a family of measurable market-structure features rather than as an opaque strategy.

Suggested feature families:

- swing highs/lows
- BOS
- CHoCH
- market structure
- internal/external structure
- liquidity pools
- equal highs/lows
- liquidity sweeps
- displacement
- fair value gaps
- order blocks
- breaker blocks
- mitigation
- premium/discount zones
- dealing ranges
- session behavior
- multi-timeframe structure

Every feature must declare:
- calculation timestamp
- confirmation timestamp
- lookback window
- whether confirmation requires future bars
- whether it can repaint
- raw inputs used

For live trading, only information known at decision time may be used.

## Data architecture

Normalize all sources into a canonical model:

Instrument
Market
Venue
TradingSession
Tick
Quote
Trade
Candle
OrderBookSnapshot
CorporateAction
NewsEvent
EconomicEvent

Keep source-specific raw data separately from normalized data.

Recommended storage tiers:

1. Raw immutable source data
2. Normalized market data
3. Derived features
4. Strategy signals
5. Orders/trades
6. Research datasets
7. Model artifacts

## Target runtime

FastAPI remains the application/API layer.

Use asynchronous messaging/event processing for live market and order events.

SQLite can remain the local development database, but production should be designed around a proper transactional database plus time-series/analytical storage where scale requires it.

## Development order

### Phase 1 — Portfolio foundation
- users/authentication
- portfolios
- positions
- transactions
- P&L
- holdings
- exposure
- portfolio APIs

### Phase 2 — Trading
- order models
- order validation
- paper broker
- order state machine
- execution service
- broker abstraction
- first live broker adapter

### Phase 3 — Market
- normalized instruments
- OHLCV
- quotes
- WebSocket updates
- watchlists
- screener
- chart data
- market depth

### Phase 4 — Analysis
- TA-Lib integration
- custom indicator engine
- SMC/ICT engine
- multi-timeframe analysis
- signals
- alerts

### Phase 5 — Backtesting
- shared strategy interface
- historical simulator
- commission/slippage
- metrics
- optimization
- walk-forward
- Monte Carlo

### Phase 6 — AI Advisor
- feature store
- model registry
- regime detection
- signal ranking
- research agent
- strategy generator
- model validation
- explainability

### Phase 7 — News / admin / operations
- news ingestion
- economic calendar
- admin controls
- broker health
- audit logs
- monitoring
- risk controls
- operational dashboards

## Non-negotiable engineering rules

1. No look-ahead bias.
2. No broker call from strategy code.
3. No AI component can bypass the risk engine.
4. Every live order gets an audit trail.
5. Backtest results are immutable once published.
6. Strategies are versioned.
7. Models are versioned.
8. Features have deterministic definitions.
9. Broker adapters implement one internal interface.
10. Paper/live execution share order semantics.
11. Secrets never live in source control.
12. Every important decision has a reproducible input snapshot.

## Initial integration priority

For this project, the first reference stack should be:

- NautilusTrader -> execution/event architecture reference
- LEAN -> engine and brokerage architecture reference
- VN.PY -> modular feature reference
- CCXT -> crypto adapter
- TA-Lib -> standard indicators
- custom SMC engine -> production market-structure logic
- Qlib -> quantitative research architecture
- Optuna -> optimization
- PyPortfolioOpt -> allocation
- Lightweight Charts -> frontend chart rendering

These are references/components, not a mandate to copy their code into the project.
