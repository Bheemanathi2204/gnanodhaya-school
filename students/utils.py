from django.shortcuts import redirect

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.groups.filter(name="Teacher").exists():
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper


def parent_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.groups.filter(name="Parent").exists():
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper


def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.groups.filter(name="Student").exists():
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper
