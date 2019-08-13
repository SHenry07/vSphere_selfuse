from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request,'index.html',locals())

def login(request):
    name = request.POST.get('username')
    password = request.POST.get('userpassword')
    user = User.login(name, password)
    if user:
      ...
      return redirect('user:users')
    else:
      context = {
          'name' : name,
          'error' : '用户名或密码错误'
      }
      return render(request, 'user/login.html', context)
  
