# Crypto Price Feeds

Bitcoin price aggregator that fetches data from multiple free, unauthenticated APIs and consolidates them into a single price point.

## APIs Used

- **CoinGecko**: Market cap, 24h volume, 24h price change
- **CoinDesk**: Current BTC price

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python price_aggregator.py
```

Outputs to `btc_price_data.json`:

```json
{
  "timestamp": "2024-01-15T10:30:45.123456Z",
  "btc_price_usd": 42500.50,
  "min_price": 42480.00,
  "max_price": 42520.00,
  "spread": 40.00,
  "spread_percent": 0.0941,
  "sources_used": 2,
  "source_details": [...]
}
```

## Running on Schedule

Add to crontab to run every 5 minutes:

```
*/5 * * * * cd /path/to/crypto-price-feeds && python price_aggregator.py
```

## Notes

All APIs are free and require no authentication. Network calls have 10-second timeouts.
