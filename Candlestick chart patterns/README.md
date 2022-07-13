### About Candles

Chart analysis can give a trader insight into the current market environment - what is happening right here and right now. Each candle carries useful information for santiment understanding: the market's open, high, low, and close price for the time period.

The size and shape of a candle can tell a lot about the strength, momentum, and trend of the market at the moment. For example, when candles get bigger, it is a signal for a stronger trend. Small candles after a long rally may precede a reversal or the end of a trend. Long shadows at key support or resistance levels are often a good sign of a potential market reversal. Shadows usually indicate a price bounce or failed attempts to push the price above or below an important price level.

Context is important in candlestick analysis, as a result of which the current candle is always considered in the context of the overall market movement. That is why a trader should not rely only on candlestick patterns for making trading decisions, but their appearance deserves attention.

### Pattern Recognition

![alt text](https://www.tradingview.com/x/UF4uIhLq/)

You can find a huge number of candlestick patterns in books, most of which are useless in real life. I used the TA-Lib library for pattern discovery and out of an initial 60+ patterns, 40 were initially selected. Of these, 11 appeared only once during the entire study period, so it is not yet possible to evaluate them to the proper extent.

Research confirmed the widespread idea that each asset has its own manner of movement and their charts should be analyzed taking into account their features. Patterns that worked well on bitcoin could show worse results on ETH and other coins, which is why I decided to define its own list of setups for each asset. For example, its 12 patterns for BTC and 17 for BNB. Some of the patterns looked useful, but their implementation in the library was fundamentally different from the generally accepted ones, which is why they were removed. The idea was to leave only the most reliable patterns, since one candle could become a source of several triggers at once, both for buying and for selling.

Since the goal was to look for turning points on the chart, the patterns were evaluated based on the dynamics on each of the four nearest candles. After that, the average return was calculated. In order to avoid too many signals, it was decided to use 4h candles from Binance exchange. This approach also allows to focus on more significant price movements and ignore short-term noise. Signals will be received for 15 coins with the largest trading volumes at the moment: BTC, ETH, SOL, DOGE, NEAR, ONE, BNB, XRP, ADA, DOT, ATOM, FTT, LTC, AVAX and MATIC. After the pattern is detected notification will be sent to the Telegram channel.
