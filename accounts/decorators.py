from django.http import HttpResponse
from django.shortcuts import redirect

def authentication_required(view_func) :
    def wrapper_func(request, *args, **kwargs) :
        if request.user.is_authenticated :
            return redirect('home')
        else :
            return view_func(request, *args, **kwargs)
    return wrapper_func

def user_allowed(allowed_users=[]) :
    # print("allowed_users : " + str(allowed_users))
    def decorator(view_func) :
        def wrapper_func(request, *args, **kwargs) :
            user_groups = None
            
            if request.user.groups.exists() :
                print("exists")
                user_groups = request.user.groups.all()
                
                for user_group in user_groups :
                    print("user_group : " + str(user_group))
                    if user_group.name in allowed_users :
                        return view_func(request, *args, **kwargs)

            return HttpResponse("unauthorized access")
        return wrapper_func
    return decorator

def admin_only(view_func) :
    def wrapper_func(request, *args, **kwargs) :
        group = None
        if request.user.groups.exists() :
            group = request.user.groups.all()[0].name
        
        if group == "admins" :
            return view_func(request, *args, **kwargs)
        else :
            print("a customer")
            return redirect('userHome')
    return wrapper_func