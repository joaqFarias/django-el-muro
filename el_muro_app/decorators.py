from django.shortcuts import redirect


def login_required(function):

    def wrapper(request, *args):
        if 'user' not in request.session:
            return redirect('/login')
        resp = function(request, *args)
        return resp
    
    return wrapper