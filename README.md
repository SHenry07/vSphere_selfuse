# 项目立意
自己的一个小实践，分页、查找正在学习中

# 业务逻辑：

```flow
st=>start:  前端处理
op=>operation: view视图处理
cond=>异步: Yes or No?
sub=>subroutine: celery
op2=>operation: 调用vspehere_exec中的模块
e=>返回值前端渲染

st->op->cond
cond(yes)->sub->op2->e
cond(no)->e
```


`settings.py`中请自行添加mysql数据地址

在`clone_vm.py`里`54行`写死了虚拟机的文件目录,请自行修改或者创建相应目录
