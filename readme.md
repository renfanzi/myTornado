### 删除所有.pyc文件命令
```
find 路径 -type f -name  "*.pyc"  | xargs -i -t rm -f {}
```

### 结束进程
```
lsof -i:8002 |sed '1d'| awk '{print $2}' | xargs kill -9
```


### 打包命令
zip -r zk_css.zip zk_css/


### 启动服务
nohup python run.py > /dev/null &



### 上线注意事项
更改配置文件信息
更改日志权限
更改索引权限
更改文件目录权限


### 文件路径和索引文件路径
1. 首先创建文件, 给文件相应权限
2. 搜索引擎，先执行createwhooshindex 创建索引文件， 注意指定路径()
3. filepath