# Ai-Algo-Trading-Platform
this is for trading life easy


src/
│
├── App.jsx
├── main.jsx
│
├── api/
│   └── api.js
│
├── assets/
│   ├── images/
│   ├── icons/
│   └── logo/
│
├── components/
│
│   ├── common/
│   │   ├── Header.jsx
│   │   ├── Sidebar.jsx
│   │   ├── Topbar.jsx
│   │   ├── Layout.jsx
│   │   ├── Loader.jsx
│   │   ├── StatCard.jsx
│   │   ├── SearchBar.jsx
│   │   ├── NotificationBell.jsx
│   │   └── EmptyState.jsx
│   │
│   ├── dashboard/
│   │   ├── DashboardChart.jsx
│   │   ├── DashboardStats.jsx
│   │   ├── MarketOverview.jsx
│   │   ├── AIRecommendationCard.jsx
│   │   ├── RecommendationCard.jsx
│   │   └── Indices.jsx
│   │
│   ├── portfolio/
│   │   ├── PortfolioSummary.jsx
│   │   ├── SummaryCard.jsx
│   │   ├── HoldingsTable.jsx
│   │   ├── HoldingRow.jsx
│   │   ├── PortfolioChart.jsx
│   │   ├── AllocationChart.jsx
│   │   ├── PerformanceStats.jsx
│   │   ├── RecentTransactions.jsx
│   │   └── PortfolioAnalytics.jsx
│   │
│   ├── market/
│   │   ├── MarketTable.jsx
│   │   ├── StockChart.jsx
│   │   ├── CandlestickChart.jsx
│   │   ├── LiveScanner.jsx
│   │   ├── MarketHeatmap.jsx
│   │   ├── SectorPerformance.jsx
│   │   └── TopMovers.jsx
│   │
│   ├── watchlist/
│   │   ├── WatchlistTable.jsx
│   │   ├── WatchlistCard.jsx
│   │   └── WatchlistToolbar.jsx
│   │
│   ├── trading/
│   │   ├── TradingView.jsx
│   │   ├── OrderPanel.jsx
│   │   ├── WatchlistPanel.jsx
│   │   ├── PositionsTable.jsx
│   │   ├── OrdersTable.jsx
│   │   ├── TradeHistory.jsx
│   │   ├── RecentTrades.jsx
│   │   ├── MarketDepth.jsx
│   │   ├── OpenOrders.jsx
│   │   ├── OptionChain.jsx
│   │   ├── OrderBook.jsx
│   │   └── ChartToolbar.jsx
│   │
│   ├── ai/
│   │   ├── AISignalCard.jsx
│   │   ├── AIScanner.jsx
│   │   ├── PredictionCard.jsx
│   │   ├── ConfidenceMeter.jsx
│   │   ├── StrategyCard.jsx
│   │   ├── TechnicalSummary.jsx
│   │   └── RiskScore.jsx
│   │
│   └── news/
│       ├── NewsCard.jsx
│       ├── NewsList.jsx
│       └── EconomicCalendar.jsx
│
├── pages/
│   ├── Login.jsx
│   ├── Dashboard.jsx
│   ├── Portfolio.jsx
│   ├── Market.jsx
│   ├── Trading.jsx
│   ├── Watchlist.jsx
│   ├── AI.jsx
│   ├── News.jsx
│   └── Settings.jsx
│
├── services/
│   ├── websocket.js
│   ├── auth.js
│   ├── portfolio.js
│   ├── market.js
│   ├── trading.js
│   ├── ai.js
│   └── watchlist.js
│
├── hooks/
│   ├── usePortfolio.js
│   ├── useMarket.js
│   ├── useTrading.js
│   ├── useWatchlist.js
│   └── useAI.js
│
├── utils/
│   ├── formatters.js
│   ├── constants.js
│   ├── indicators.js
│   └── helpers.js
│
├── styles/
│
│   ├── common/
│   │   ├── layout.css
│   │   ├── sidebar.css
│   │   ├── topbar.css
│   │   ├── cards.css
│   │   └── globals.css
│   │
│   ├── dashboard/
│   │   ├── dashboard.css
│   │   └── dashboardStats.css
│   │
│   ├── portfolio/
│   │   ├── portfolio-summary.css
│   │   ├── portfolio-chart.css
│   │   ├── holdings-table.css
│   │   ├── allocation-chart.css
│   │   └── analytics.css
│   │
│   ├── market/
│   │   ├── market.css
│   │   ├── stock-chart.css
│   │   └── scanner.css
│   │
│   ├── trading/
│   │   ├── trading.css
│   │   ├── order-panel.css
│   │   ├── tables.css
│   │   └── watchlist-panel.css
│   │
│   ├── ai/
│   │   └── ai.css
│   │
│   ├── news/
│   │   └── news.css
│   │
│   └── watchlist/
│       └── watchlist.css
│
└── admin/
    │
    ├── components/
    │   ├── AdminLayout.jsx
    │   ├── AdminSidebar.jsx
    │   ├── AdminTopbar.jsx
    │   └── AdminStatCard.jsx
    │
    ├── pages/
    │   ├── Dashboard.jsx
    │   ├── Users.jsx
    │   ├── Portfolios.jsx
    │   ├── Orders.jsx
    │   ├── Trades.jsx
    │   ├── Watchlist.jsx
    │   ├── Market.jsx
    │   ├── AI.jsx
    │   ├── Risk.jsx
    │   └── Settings.jsx
    │
    ├── services/
    │   ├── users.js
    │   ├── portfolios.js
    │   ├── orders.js
    │   └── trades.js
    │
    └── styles/
        ├── admin.css
        ├── sidebar.css
        ├── topbar.css
        ├── users.css
        ├── portfolios.css
        ├── trades.css
        ├── orders.css
        └── watchlist.css
