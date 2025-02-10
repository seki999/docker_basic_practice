# 使用官方 MySQL 镜像作为基础镜像
FROM mysql:latest
  
# 设置环境变量（注意：MYSQL_ROOT_PASSWORD 是必须设置的）
ENV MYSQL_ROOT_PASSWORD=my-secret-pw
ENV MYSQL_DATABASE=web

# 将初始化 SQL 文件复制到镜像的初始化目录中
COPY init.sql /docker-entrypoint-initdb.d/

# 如果需要可以暴露3306端口
EXPOSE 3306
