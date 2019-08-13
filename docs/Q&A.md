1. xadmin出现如下错误ModuleNotFoundError: No module named 'django.core.urlresolvers'

解: 将`core.urlresolvers`替换为`urls`

2. File "D:\cmdb\extra_apps\xadmin\views\dashboard.py", line 285, in __init__
    *args, **kwargs)   TypeError: __init__() takes 1 positional argument but 6 were given

解: 将改行替换为`forms.Field.__init__(self, required=required, widget=widget, label=label, initial=initial, help_text=help_text, **kwargs)`

3.  `xadmin\plugins\language.py", line 24, in <module>`
    `if settings.LANGUAGES and 'django.middleware.locale.LocaleMiddleware' in settings.MIDDLEWARE_CLASSES:`
    AttributeError: 'Settings' object has no attribute 'MIDDLEWARE_CLASSES'

解: 替换为`if settings.LANGUAGES and 'django.middleware.locale.LocaleMiddleware' in settings.MIDDLEWARE:`

4. `ModuleNotFoundError: No module named 'django.contrib.formtools'`

解: 重装`django-formtools`

5. `extra_apps\xadmin\util.py", line 94, in vendor`
`AttributeError: 'Media' object has no attribute 'add_css'`

解: 替换为

```python
def vendor(*tags):
    css = {'screen': []}
    js = []
    for tag in tags:
        file_type = tag.split('.')[-1]
        files = xstatic(tag)
        if file_type == 'js':
            js.extend(files)
        elif file_type == 'css':
            css['screen'] += files
    return Media(css=css, js=js)
```
6. Xadmin添加用户小组件出错:
> render() got an unexpected keyword argument 'renderer'

原因是render函数在django2.1上有变化，解决方法是修改xadmin源码，编辑xadmin/views/dashboard.py
```python
# render() got an unexpected keyword argument 'renderer'
# 修改bug, 添加renderer
def render(self, name, value, attrs=None, renderer=None):
```

7. 报异常 ‘DateTimeField‘ object has no attribute ‘rel‘

修改 xadmin\views/list.py 中228行
```python
if isinstance(field.rel, models.ManyToOneRel):

related_fields.append(field_name)
```
修改为
```python
if isinstance(field.remote_field, models.ManyToOneRel):

related_fields.append(field_name)
```
>> PS：凡是报异常rel的地方都可以尝试将报错方法中的.rel 修改为.remote_field

# Reference
[django2.0下Xadmin错误参考](https://www.cnblogs.com/xingfuggz/p/10142388.html)
[参考2](https://blog.csdn.net/jehon/article/details/84851611)