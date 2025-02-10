在 `mysql_demo` 文件夹下，执行以下命令构建镜像（例如命名为 `my-mysql`）：
```bash
docker build -t my-mysql .
```

### 3 运行容器

运行容器并映射 MySQL 默认端口（3306）到宿主机上：
```bash
docker run -d -p 3306:3306 --name my-mysql-container my-mysql
```

> **提示：** 如果你本机已有 MySQL 服务在 3306 端口上运行，建议修改映射端口，例如使用 `-p 3307:3306`。

### 4 验证数据库

你可以通过多种方式验证数据库是否正确初始化：

#### 方式1：使用 MySQL 客户端连接
例如在命令行中使用 `mysql` 客户端连接（需要先安装 mysql 客户端）：
```bash
mysql -h 127.0.0.1 -P 3306 -u root -p
```
输入上面设置的密码 `my-secret-pw` 后，执行以下 SQL 语句检查：
```sql
USE web;
SELECT * FROM user;
```
应该能看到一条记录，内容为 `admin` 和 `123456`。

#### 方式2：通过容器内部验证

你也可以进入容器内部进行验证：
```bash
docker exec -it my-mysql-container bash
# 在容器内使用 mysql 客户端（注意可能需要先安装，或者直接使用镜像中自带的 mysql 命令）
mysql -u root -p
```
同样使用 `my-secret-pw` 密码，然后执行 SQL 命令进行验证。
