from django.urls import path

from . import views

app_name = 'adddisk'
urlpatterns =[

    path('',views.index,name='index'),

    # 添加硬盘
    # ex /adddisk/9f
    path('<str:vsphere_comment>/',views.machines,name='vmlist'),

    # ex /adddisk/9f/name
    path('<str:vsphere_comment>/<str:vm_name>/',views.details,name='vmdetail'),
]
