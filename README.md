## Author Honglei Zhou (周宏雷)

## 数据转换
### how to use
1. convert csv file to json data
```
from p1 import csv2json

file_path = path
result = csv2json(file_path)
print(result)
```

2. key search
```
from p1 import find, csv2json

file_path = path
result = find(key)
print(result)
```



## 用户权限验证系统

实现简单的博客系统权限管理后台，满足以下两个简单需求：
1. 系统有两种角色：普通用户，管理员
2. 每种角色有不同的权限：
	a. 普通用户：可以查看所有人的文章，只能编辑，删除自己的文章
	b. 管理员：管理员拥有普通用户的权限，并且拥有删除其他用户文章的权限
3. 前端通过RESTful API与后台交互

### 使用说明

#### database
```
copy files posts.txt and users.txt to document specified within create_table.sql and execute all
```

### config the file
```
db_addr = '<addr>:<port>'
db_user = '<user>'
db_pwd = '<password>'
```

### run the service
The default port is 5000

```
./start.sh [port]
```

### how to use the service
You have to login first to use the service.
1. login
```
curl -F 'username=nbyis' -F 'password=hshach' -X POST http://127.0.0.1:5000/login
```

2. list all the posts
Example
```
curl -X GET http://127.0.0.1:5000/list 

```

3. search post
Example: search by username
```
curl -F 'username=nbyis' -X POST http://127.0.0.1:5000/search
```

Example: search by post_id
```
curl -F 'post_id=1' -X POST http://127.0.0.1:5000/search
```

4. update post
Permission required.
Example
```
curl -F 'post_id=1' -F 'content=abcdefghijk' -X POST http://127.0.0.1:5000/update
```

5. delete post
Permission required.
Example
```
curl -F 'post_id=1' -X POST http://127.0.0.1:5000/delete
```

