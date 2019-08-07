from django.urls import path
from . import views 

app_name = 'assets'

urlpatterns = [
    # path('',views.dashboard),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('all/',views.VMDeatilsAll,name='vmall'),
    path('<str:vsphere_comment>/',views.VMDeatilsEachIDC,name='vmeachIDC'),
    path('detail/<uuid:UUID>/',views.vmdetailsOne,name='detail')
]