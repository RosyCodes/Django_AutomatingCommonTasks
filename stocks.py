from bs4 import BeautifulSoup
import requests

def scrape_stock_data(symbol, exchange):
    if exchange == 'NASDAQ' or exchange == 'OTC':
        url = f"https://finance.yahoo.com/quote/{symbol}/"
    elif exchange == 'NSE':
        symbol = symbol+'.NS'
        url = f"https://finance.yahoo.com/quote/{symbol}/"

    # for real-time stock prices, Define the headers with a User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    # Make the request with headers
    response = requests.get(url, headers=headers)
    # response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Print the status code to ensure the request was successful
    print(f"Status code for {symbol}: {response.status_code}\n=============")
    current_price = soup.find(
        "fin-streamer", {"data-field": "regularMarketPrice"})['data-value']
    print('Current price -->', current_price)

    previous_close = soup.find(
        "fin-streamer", {"data-field": "regularMarketPreviousClose"})['data-value']
    print('Previous close -->', previous_close)

    print("=============")

# Example usage
scrape_stock_data('GOOG', 'NASDAQ')
scrape_stock_data('JBFCF', 'OTC')
scrape_stock_data('TATAMOTORS', 'NSE')
# # Print the status code to ensure the request was successful
# print(f"Status code for {symbol}: {response.status_code}\n=============")

# # Find and print the current price
# current_price_tag = soup.find(
#     "fin-streamer", {"data-field": "regularMarketPrice"})
# if current_price_tag:
#     current_price = current_price_tag.get('data-value')
#     print('Current price -->', current_price)
# else:
#     print(
#         f"Current price not found for {symbol}. The HTML structure may have changed or the content is loaded dynamically.")

# # Find and print the previous close
# previous_close_tag = soup.find(
#     "fin-streamer", {"data-field": "regularMarketPreviousClose"})
# if previous_close_tag:
#     previous_close = previous_close_tag.get('data-value')
#     print('Previous close -->', previous_close)
# else:
#     print(
#         f"Previous close not found for {symbol}. The HTML structure may have changed or the content is loaded dynamically.")
