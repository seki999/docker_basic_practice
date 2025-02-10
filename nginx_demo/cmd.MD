在 nginx_demo 文件夹下，执行以下命令构建镜像（镜像名可以自定义，如 my-nginx）：
1.运行容器
docker build -t my-nginx .
2.构建成功后，运行容器并将容器的 80 端口映射到宿主机的 8080 端口：
docker run -d -p 8080:80 --name my-nginx-container my-nginx
3.访问测试
在浏览器中访问：http://localhost:8080
或者使用 curl 命令：
curl http://localhost:8080
如果一切正常，就会看到你在 index.html 中定义的页面内容。
