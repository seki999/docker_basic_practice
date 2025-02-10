# 使用官方 Nginx 镜像作为基础镜像
FROM nginx:latest

# 将当前目录下的 index.html 文件复制到镜像中 Nginx 默认的静态文件目录
COPY index.html /usr/share/nginx/html/index.html

# 暴露容器的 80 端口（可选：运行时通过 -p 参数映射到宿主机端口）
EXPOSE 80
