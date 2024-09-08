from bs4 import BeautifulSoup
import requests


def scrape_stock_data(symbol, exchange):

    if exchange == 'NSE':
        symbol = symbol+'.NS'
    url = f"https://finance.yahoo.com/quote/{symbol}/"

    # for real-time stock prices, Define the headers with a User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    try:
        # Make the request with headers
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            current_price = soup.find(
                "fin-streamer", {"data-field": "regularMarketPrice"})['data-value']
            previous_close = soup.find(
                "fin-streamer", {"data-field": "regularMarketPreviousClose"})['data-value']
            price_changed = soup.find(
                "fin-streamer", {"data-testid": "qsp-price-change"}).span.text
            percentage_changed = soup.find(
                "fin-streamer", {"data-testid": "qsp-price-change-percent"}).span.text
            week_52_range = soup.find(
                "fin-streamer", {"data-field": "fiftyTwoWeekRange"}).text
            week_52_low, week_52_high = week_52_range.split(' - ')
            market_cap = soup.find(
                "fin-streamer", {"data-field": "marketCap"}).text
            pe_ratio = soup.find(
                "fin-streamer", {"data-field": "trailingPE"}).text
            # dividend_yield has no attribute name yet

            stock_response = {
                'current_price': current_price,
                'previous_close': previous_close,
                'price_changed': price_changed,
                'percentage_changed': percentage_changed,
                'market_cap': market_cap,
                'pe_ratio': pe_ratio,
                'week_52_low': week_52_low,
                'week_52_high': week_52_high,
                # 'dividend_yield': dividend_yield,
            }
            return stock_response

    except Exception as e:
        print(f'Error scraping the data: {e}')
        return None
