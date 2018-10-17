import json
from .converter import CurrencyConverter
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

def check_errors(from_currency, to_currency, amount):
    errors = list()
    if not from_currency:
        errors.append('select first currency')
    if not to_currency:
        errors.append('select second currency')
    if not amount:
        errors.append('amount is required')
    return errors
    
def converter_json(request):
    from_currency = request.GET.get('from_currency')
    to_currency = request.GET.get('to_currency')
    amount = request.GET.get('amount')
    errors = check_errors(from_currency, to_currency, amount)
    if not errors:
        converter = CurrencyConverter()
        try:
            out = converter.convert(amount, from_currency, to_currency)
        except ValueError as e:
            errors.append(str(e))
        except TypeError as e:
            errors.append(str(e))
    if errors:
        out = {
            "error": True,
            "message": ', '.join(errors)
        }
    return HttpResponse(json.dumps(out))

@csrf_exempt
def page(request):
    if request.GET.get('type') == 'json':
        return converter_json(request)
    elif request.method == 'POST':
        from_currency = request.POST.get('from_currency_type')
        to_currency = request.POST.get('to_currency_type')
        amount = request.POST.get('amount')
        errors = check_errors(from_currency, to_currency, amount)
        if not errors:
            converter = CurrencyConverter()
            currency = converter.convert(amount, from_currency, to_currency)
            response = render(request, 'currency/answer.html', currency)
        else:
            response = render(request, 'currency/form.html', {'errors': errors})
    else:
        response = render(request, 'currency/form.html', {})
    return response


