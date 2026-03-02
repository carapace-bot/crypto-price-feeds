#!/usr/bin/env python3
"""
Bitcoin price aggregator - fetches BTC prices from multiple free APIs
and consolidates them into a single data point.
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Tuple

def fetch_coingecko_btc() -> Tuple[float, Dict]:
    """Fetch BTC price from CoinGecko API"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        btc_data = data.get("bitcoin", {})
        price = btc_data.get("usd")
        
        return price, {
            "source": "coingecko",
            "price": price,
            "market_cap": btc_data.get("usd_market_cap"),
            "volume_24h": btc_data.get("usd_24h_vol"),
            "change_24h": btc_data.get("usd_24h_change")
        }
    except Exception as e:
        print(f"Error fetching from CoinGecko: {e}")
        return None, {"source": "coingecko", "error": str(e)}

def fetch_coindesk_btc() -> Tuple[float, Dict]:
    """Fetch BTC price from CoinDesk API"""
    try:
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        price = data.get("bpi", {}).get("USD", {}).get("rate_float")
        
        return price, {
            "source": "coindesk",
            "price": price
        }
    except Exception as e:
        print(f"Error fetching from CoinDesk: {e}")
        return None, {"source": "coindesk", "error": str(e)}

def aggregate_prices(sources: List[Tuple[float, Dict]]) -> Dict:
    """Aggregate prices from multiple sources"""
    prices = [p for p, _ in sources if p is not None]
    
    if not prices:
        return {"error": "No valid price data retrieved"}
    
    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)
    spread = max_price - min_price
    spread_pct = (spread / avg_price * 100) if avg_price > 0 else 0
    
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "btc_price_usd": round(avg_price, 2),
        "min_price": round(min_price, 2),
        "max_price": round(max_price, 2),
        "spread": round(spread, 2),
        "spread_percent": round(spread_pct, 4),
        "sources_used": len(prices),
        "source_details": [s for _, s in sources]
    }

def main():
    """Fetch prices and save aggregated data"""
    print("Fetching Bitcoin prices from multiple sources...")
    
    sources = [
        fetch_coingecko_btc(),
        fetch_coindesk_btc()
    ]
    
    aggregated = aggregate_prices(sources)
    
    # Save to JSON
    with open("btc_price_data.json", "w") as f:
        json.dump(aggregated, f, indent=2)
    
    print(f"BTC Price: ${aggregated.get('btc_price_usd', 'N/A')}")
    print(f"Spread: ${aggregated.get('spread', 'N/A')} ({aggregated.get('spread_percent', 'N/A')}%)")
    print(f"Saved to btc_price_data.json")

if __name__ == "__main__":
    main()
