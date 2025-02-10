下面给出两个简单的示例，分别展示如何构建和运行一个 **Nginx** 容器以及一个 **MySQL** 容器（在 MySQL 中自动创建一个数据库和一张表，并插入一条数据）。你可以根据下面的示例进行学习和实验。
---
## 示例 1：构建 Nginx 容器

### 1.1 准备工作

在你的工作目录下建立一个文件夹，例如：`nginx_demo`，并进入该文件夹。然后创建以下两个文件：

- **index.html**  
  这是网页的静态页面，可以随意修改内容，例如：
  ```html
  <!DOCTYPE html>
  <html>
  <head>
      <meta charset="UTF-8">
      <title>Docker Nginx Demo</title>
  </head>
  <body>
      <h1>Hello, Docker Nginx!</h1>
      <p>这是一个通过 Docker 构建的 Nginx 容器示例。</p>
  </body>
  </html>
  ```

- **Dockerfile**  
  内容如下：
  ```dockerfile
  # 使用官方 Nginx 镜像作为基础镜像
  FROM nginx:latest
  
  # 将当前目录下的 index.html 文件复制到镜像中 Nginx 默认的静态文件目录
  COPY index.html /usr/share/nginx/html/index.html
  
  # 暴露容器的 80 端口（可选：运行时通过 -p 参数映射到宿主机端口）
  EXPOSE 80
  ```

### 1.2 构建镜像

在 `nginx_demo` 文件夹下，执行以下命令构建镜像（镜像名可以自定义，如 `my-nginx`）：
```bash
docker build -t my-nginx .
```

### 1.3 运行容器

构建成功后，运行容器并将容器的 80 端口映射到宿主机的 8080 端口：
```bash
docker run -d -p 8080:80 --name my-nginx-container my-nginx
```

### 1.4 访问测试

- 在浏览器中访问：[http://localhost:8080](http://localhost:8080)  
- 或者使用 curl 命令：
  ```bash
  curl http://localhost:8080
  ```

如果一切正常，就会看到你在 `index.html` 中定义的页面内容。

---

## 其他学习提示

- **docker-compose：**  
  如果你想同时管理多个容器，可以尝试使用 [docker-compose](https://docs.docker.com/compose/)。例如，将上面两个服务写到一个 `docker-compose.yml` 文件中，方便同时启动和管理。

- **扩展阅读：**  
  学习如何使用 Docker 卷（volumes）来持久化数据；如何编写多阶段构建的 Dockerfile；以及如何优化镜像体积。

---

以上示例提供了一个基本的入门案例，你可以在此基础上进行扩展和深入学习 Docker 的使用。Happy Learning!