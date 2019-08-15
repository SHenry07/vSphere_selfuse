'''
@Description: 
@Author: Henry Sun
@Date: 2019-08-07 14:11:06
@LastEditors: Henry Sun
@LastEditTime: 2019-08-14 22:13:51
'''
import xadmin
from xadmin import views
from .models import Vsphere
import taggit
import assets
# Register your models here.
class VsphereAdmin(object):

    list_display = ('vsphere_comment','vsphere_host','idc_address','idc_contact','idc_phone')
    
xadmin.site.register(Vsphere,VsphereAdmin)


class BaseSetting(object):
    '''
    主题样式多样化
    '''
    enable_themes=True
    use_bootswatch=True


class GlobalSetting(object):
    #页头
    site_title = '运维后台管理系统'
    #页脚
    site_footer = '上海钢银电子商务有限公司'
    #左侧样式
    menu_style='accordion'
    # 设置models的全局图标
    global_search_models = [Vsphere]
    global_models_icon = {
        Vsphere: "glyphicon glyphicon-th-list",
        taggit.models.Tag: "glyphicon glyphicon-tags",
        assets.models.VmDetails : "fa fa-list-alt"
    }
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)