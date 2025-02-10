 **MySQL** 容器（在 MySQL 中自动创建一个数据库和一张表，并插入一条数据）。你可以根据下面的示例进行学习和实验。
构建 MySQL 容器并初始化数据库
### 1 准备工作

建立一个新的目录，例如：`mysql_demo`，并在该目录下创建以下文件：

- **init.sql**  
  用于初始化数据库，内容如下：
  ```sql
  -- 创建数据库 web，如果不存在的话
  CREATE DATABASE IF NOT EXISTS web;
  
  -- 切换到 web 数据库
  USE web;
  
  -- 创建 user 表（包含 id, name, password 三个字段）
  CREATE TABLE IF NOT EXISTS user (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(50) NOT NULL,
      password VARCHAR(50) NOT NULL
  );
  
  -- 插入一条数据：name 为 'admin', password 为 '123456'
  INSERT INTO user (name, password) VALUES ('admin', '123456');
  ```

- **Dockerfile**  
  使用官方 MySQL 镜像，并复制 `init.sql` 到镜像中预定义的初始化目录：
  ```dockerfile
  # 使用官方 MySQL 镜像作为基础镜像
  FROM mysql:latest
  
  # 设置环境变量（注意：MYSQL_ROOT_PASSWORD 是必须设置的）
  ENV MYSQL_ROOT_PASSWORD=my-secret-pw
  ENV MYSQL_DATABASE=web
  
  # 将初始化 SQL 文件复制到镜像的初始化目录中
  COPY init.sql /docker-entrypoint-initdb.d/
  
  # 如果需要可以暴露3306端口
  EXPOSE 3306
  ```

> **注意：**  
> - `MYSQL_ROOT_PASSWORD` 用于设置 root 用户的密码，这里设置为 `my-secret-pw`（你可以自行修改）。  
> - 由于在环境变量中指定了 `MYSQL_DATABASE=web`，官方镜像在启动时会自动创建该数据库；但为了确保在数据库中创建 user 表和插入数据，我们依然在 `init.sql` 中操作。

### 2 构建镜像

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

---

## 其他学习提示

- **docker-compose：**  
  如果你想同时管理多个容器，可以尝试使用 [docker-compose](https://docs.docker.com/compose/)。例如，将上面两个服务写到一个 `docker-compose.yml` 文件中，方便同时启动和管理。

- **扩展阅读：**  
  学习如何使用 Docker 卷（volumes）来持久化数据；如何编写多阶段构建的 Dockerfile；以及如何优化镜像体积。
