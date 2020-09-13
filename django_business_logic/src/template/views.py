from django.shortcuts import render


def echo(request):
    params = {
        'method': request.method.lower(),
        'par_name': '',
        'statement': ''
    }
    if params['method'] == 'get':
        par = dict(request.GET)
        for p in par:
            params['par_name'] = params['par_name'] + p + ': ' + par[p][0]
    elif params['method'] == 'post':
        par = dict(request.POST)
        for p in par:
            params['par_name'] = params['par_name'] + p + ': ' + par[p][0]
    try:
        params['statement'] = request.META['HTTP_X_PRINT_STATEMENT']
    except:
        params['statement'] = 'empty'
    return render(request, 'echo.html', params)


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
