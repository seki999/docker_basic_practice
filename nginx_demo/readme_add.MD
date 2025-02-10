在 Docker 中，你可以使用以下命令来查看镜像和容器：
1. 查看镜像
    docker images
该命令会列出你本地所有的 Docker 镜像，包括仓库名、标签、镜像 ID、创建时间以及镜像大小。

2. 查看正在运行的容器
    docker ps
这个命令会显示当前正在运行的容器列表，包括容器 ID、镜像名称、创建时间、状态、端口映射以及容器名称。

3. 查看所有容器（包括已停止的容器）
    docker ps -a
加上 `-a` 参数可以显示所有容器，无论它们是否正在运行。

### 补充说明
- 查看容器详细信息
如果你想查看某个容器的详细信息，可以使用：
    docker inspect <容器ID或容器名称>
- 查看镜像的详细信息
同样，可以使用 `docker inspect` 来查看某个镜像的详细信息：
    docker inspect <镜像ID或镜像名称>
这些命令可以帮助你更好地管理和调试 Docker 环境。Happy Docker!
要进入正在运行的 Nginx 容器内部，可以使用 `docker exec` 命令。下面提供具体步骤：
1. 确定容器名称或ID
如果你还不知道容器名称，可以先查看正在运行的容器：
    docker ps
找到你 Nginx 容器的名称或容器 ID（例如之前启动时使用了 `--name my-nginx-container`）。
2. 进入容器内部
使用 `docker exec` 命令进入容器内部。如果容器内安装了 `bash`（大多数官方 Nginx 镜像默认只有 `sh`），可以尝试：
    docker exec -it my-nginx-container bash
如果提示找不到 `bash`，请改用 `sh`：
    docker exec -it my-nginx-container sh
3. 查看 Nginx 的配置
进入容器后，可以到 Nginx 默认的配置目录查看相关配置文件。通常主要配置文件位于 `/etc/nginx/nginx.conf`，其它的配置文件可能在 `/etc/nginx/conf.d/` 目录下。可以使用下面的命令查看配置：
    cat /etc/nginx/nginx.conf
    ls /etc/nginx/conf.d/
或者使用 `vi`、`nano` 等编辑器打开文件（如果镜像中有安装的话）。
这样，你就可以进入容器内部并查看或修改 Nginx 的配置状况了。

如果你是在容器内的交互式终端中（例如通过 `docker exec -it <容器名> bash` 或 `sh` 进入的），只需输入 `exit` 并回车即可退出容器的终端会话。  

另外，如果你使用 `docker attach` 附加到容器并希望不停止容器的运行而脱离，可以使用默认的分离键序列：按下 **Ctrl + p** 然后 **Ctrl + q**，这样容器依然在后台运行，而你退出了当前的附加会话。
