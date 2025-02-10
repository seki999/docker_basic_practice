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
