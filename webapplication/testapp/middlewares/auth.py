from django.shortcuts import redirect

def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # returnUrl = request.META['PATH_INFO']
        # print(returnUrl)
    
        if not request.session.get('employeeid'):
            return redirect('/emp_login')
        # except KeyError:
        #     return redirect('/login')

        response = get_response(request)
        return response

    return middleware