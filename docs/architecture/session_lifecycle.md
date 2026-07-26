Session Lifecycle & State Machine

This document outlines the daily lifecycle of the trading engine, detailing how the Engine Manager orchestrates time, data ingestion, and portfolio liquidation from pre-market to market close.

1. Pre-Market & Synchronization
The Engine Manager boots up and queries the Broker API via the Data Manager to fetch the current market clock.

If the market is closed, the Engine calculates the time difference until the next open and enters an asynchronous sleep state.

The system wakes up automatically just before the official market open to prepare for the session.

2. Warmup Phase (REST)
At market open, the system must build its initial state before listening to real-time events. The Data Manager executes a REST API call to fetch the required historical candles (e.g., a 50-period lookback).

Extended hours (pre-market data) are intentionally ignored. The warmup fetches the closing candles from the previous trading day and the very first candles of the current session.

This prevents low-volume, inefficient pre-market data from distorting moving averages and volatility indicators.

The fetched data is injected into the isolated Data Store.

3. Real-Time Trading Phase (Websocket)
Once the Data Store is populated with the warmup data, the Data Manager opens the broker websocket connection. The Engine Manager now orchestrates the active trading state.

Opening Offset: To avoid the extreme volatility and wide spreads of the opening bell, the Engine Manager enforces a delay (e.g., next_open + 15 minutes). The Strategy Manager is blocked from emitting buy signals until this window passes.

Incoming websocket ticks are seamlessly appended to the Data Store, pushing out the oldest data, while the Engine Manager triggers the Strategy Manager to evaluate new signals.

4. Close-Only Phase
As the session approaches the closing bell, the Engine Manager initiates a shutdown sequence to eliminate overnight risk.

Closing Offset: At a specific threshold (e.g., next_close - 15 minutes), the Engine Manager shifts the system to a "Close-Only" state.

The Strategy Manager is strictly prohibited from opening new positions. It may only process sell signals for existing open positions based on its natural exit logic.

5. Hard Liquidation Phase
If the algorithm operates on a short micro-timeframe (e.g., 1-minute candles), carrying overnight positions introduces unacceptable gap risk and statistical misalignment.

At a final threshold (e.g., next_close - 5 minutes), the Engine Manager overrides the Strategy Manager entirely.

It sends a blind liquidation command to the Execution Manager (e.g., triggering a DELETE /v2/positions request via Alpaca), issuing market orders to close all remaining open positions instantly.

This guarantees the portfolio returns to 100% cash before the market closes.

6. Shutdown
At next_close, the Engine Manager terminates the websocket connection.

The Data Store is cleared, flushing all historical data from local memory.

The system powers down and resets, relying entirely on the broker's servers to maintain the permanent historical record for the next day's warmup.