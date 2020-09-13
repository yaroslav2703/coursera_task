from django.http import HttpResponseNotAllowed, HttpResponseNotFound, HttpResponse, HttpResponseBadRequest


def simple_route(request):
    if request.method == 'GET':
        if not request.path == '/routing/simple_route/':
            return HttpResponseNotFound()
        else:
            response = HttpResponse()
            response.status_code = 200
            return response
    else:
        return HttpResponseNotAllowed(['GET'])


def slug_route(request, slug):
    par_ = request.path
    print(par_)
    return HttpResponse(slug, status=200)


def sum_route(request, first, second):
        try:
            sum_ = int(first) + int(second)
            return HttpResponse(sum_, status=200)
        except:
            return HttpResponseNotFound()


def sum_get_method(request):
    if request.method == 'GET':
        a = request.GET.get('a', False)
        b = request.GET.get('b', False)
        if a == False or b == False:
            return HttpResponseBadRequest()
        try:
            sum_ = int(a) + int(b)
            return HttpResponse(sum_, status=200)
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(['GET'])


def sum_post_method(request):
    if request.method == 'POST':
        a = request.POST.get('a', False)
        b = request.POST.get('b', False)
        if a == False or b == False:
            return HttpResponseBadRequest()
        try:
            sum_ = int(a) + int(b)
            return HttpResponse(sum_, status=200)
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(['POST'])
