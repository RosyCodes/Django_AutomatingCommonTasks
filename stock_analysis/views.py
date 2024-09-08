from django.shortcuts import render, redirect, get_object_or_404
from dal import autocomplete
from .models import Stock, StockData
from .forms import StockForm
from .utils import scrape_stock_data
from django.contrib import messages


def stocks(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock_id = request.POST.get('stock')
            # fetch the stock and symbol
            stock = Stock.objects.get(pk=stock_id)
            symbol = stock.symbol

            exchange = stock.exchange
            stock_response = scrape_stock_data(symbol, exchange)

            if stock_response:
                try:
                    stock_data = StockData.objects.get(stock=stock)
                except StockData.DoesNotExist:
                    stock_data = StockData(stock=stock)

                # update the StockData table with the response data from stock_analysis\utils.py
                stock_data.current_price = stock_response['current_price']
                stock_data.previous_close = stock_response['previous_close']
                stock_data.price_changed = stock_response['price_changed']
                stock_data.percentage_changed = stock_response['percentage_changed']
                stock_data.market_cap = stock_response['market_cap']
                stock_data.pe_ratio = stock_response['pe_ratio']
                stock_data.week_52_low = stock_response['week_52_low']
                stock_data.week_52_high = stock_response['week_52_high']
                # stock_data.dividend_yield = stock_response['dividend_yield']

                stock_data.save()
                print('Data updated')
                return redirect('stock-detail', stock_data.id)
            else:
                messages.error(
                    request, f'Stock Data could not be fetched for {symbol}.')
                return redirect('stocks')
        else:
            print('Form is not valid')
    else:

        form = StockForm()
    context = {
        'form': form,
    }
    return render(request, 'stock_analysis/stocks.html', context)


class StockAutocomplete (autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Stock.objects.all()

        if self.q:
            print('Typed keywords ->', self.q)
            qs = qs.filter(name__istartswith=self.q)
            print('Result query ->', qs)

        return qs


def stock_detail(request, pk):
    stock_data = get_object_or_404(StockData, pk=pk)
    context = {
        'stock_data': stock_data,
    }
    return render(request, 'stock_analysis/stock-detail.html', context)
