django-raise-response
#####################

django-raise-response is a simple plugin that provides the ability to return
any response by raising it as you would do with django.http.Http404

Why would you need this? If you need to return a non-4XX/5XX response from a
class-based view, for example a 303/301 response, this is the only decent way
to do it.

Installing
##########

::

    pip install django-raise-response


Then add 'raiseresponse.middlewares.RaiseResponse' to your middlewares::

    MIDDLEWARE = [
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'raiseresponse.middlewares.RaiseResponse'
    ]


Usage
#####
Now you can use ResponseError to raise any response::

    from raiseresponse import ResponseError

    # somewhere in your view
    response_you_want_to_rise = HttpResponse()
    raise ResponseError(response_you_want_to_rise)
