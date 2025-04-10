# 网络相册后端

> 前置条件

运行前，请确保已经成功安装了 Python、Redis 等环境

> 重要信息

后端默认运行端口为`8000`，本说明文档中所有的命令均在 Unix 系统下测试通过，Windows 用户请自行修改命令

## 运行说明

### 1. 安装项目依赖

**强烈建议**使用`venv`创建虚拟环境，避免与其他项目的依赖冲突

命令行进入当前目录运行如下命令

```sh
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 准备工作

在当前目录下使用以下命令迁移数据库

```sh
python manage.py migrate
```

运行如下命令创建超级管理员, 用户名为`admin`，密码为`admin123`

```sh
python add_data.py
```

确保 redis 服务已经启动，redis 服务默认端口为`6379`

### 3. 启动项目

在当前目录下使用以下命令启动项目

```sh
python manage.py runserver
```
