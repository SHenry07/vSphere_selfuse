from django.urls import path

from . import views

app_name = 'clonevm'
urlpatterns =[

    path('',views.index,name='index'),

    path('idc/',views.idc,name='idc'),

    # 添加硬盘
    # ex /clonevm/9f/adddisk
    path('idc/<str:vsphere_comment>/adddisk/',views.machines,name='vmlist'),

    # ex /clonevm/9f/clonevm
    path('idc/<str:vsphere_comment>/clonevm/',views.newvm,name='newvm'),

    # ex /adddisk/9f/name
    #path('<str:vsphere_comment>/<str:vm_name>/',views.details,name='vmdetail'),
    path('<str:vsphere_comment>/details/',views.details,name='vmdetail'),
]
