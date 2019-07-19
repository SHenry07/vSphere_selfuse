# 业务逻辑

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
