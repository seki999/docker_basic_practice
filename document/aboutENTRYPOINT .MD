该页面详细讲解了 Dockerfile 中 **ENTRYPOINT** 指令的作用、格式以及使用场景，其核心内容可以归纳为以下几点：

---

### 1. ENTRYPOINT 指令的作用

- **指定容器主进程**  
  与 CMD 类似，ENTRYPOINT 用来指定容器启动时的默认主进程及其参数。不同的是，ENTRYPOINT 更强调让镜像表现得像一个可执行命令，即使在运行时传入额外参数，这些参数也会被追加到 ENTRYPOINT 所指定的命令后面。（cite1†ENTRYPOINT 入口点）

- **与 CMD 的配合**  
  当 Dockerfile 同时定义了 ENTRYPOINT 和 CMD 时，CMD 的内容会作为参数传递给 ENTRYPOINT。这种机制使得你可以将镜像设计为既固定了主要行为，又能通过传参灵活控制运行细节。

---

### 2. ENTRYPOINT 的两种格式

ENTRYPOINT 的写法与 RUN 指令类似，分为两种格式：

- **exec 格式**  
  使用 JSON 数组的形式，例如：  
  ```dockerfile
  ENTRYPOINT ["curl", "-s", "http://myip.ipip.net"]
  ```  
  这种方式不会经过 shell 解析，参数传递更为精确，推荐在大多数场景下使用。

- **shell 格式**  
  直接写成一个命令字符串，例如：  
  ```dockerfile
  ENTRYPOINT curl -s http://myip.ipip.net
  ```  
  这种方式会通过 `/bin/sh -c` 来执行命令，允许使用 shell 的特性，但可能引入一些解析上的问题。（cite1†ENTRYPOINT 入口点）

---

### 3. 使用场景

#### 场景一：让镜像变成像命令一样使用

- **问题描述**  
  有时希望构建的镜像可以直接作为一个命令行工具使用。例如，一个镜像用于查询当前公网 IP。  
- **CMD 的局限**  
  如果仅使用 CMD，当在 `docker run` 时传入新的参数，这些参数会完全替换掉 Dockerfile 中的 CMD，而不是追加在后面，从而无法实现灵活传参。  
- **ENTRYPOINT 的优势**  
  使用 ENTRYPOINT 后，运行时附加的参数会作为参数传给 ENTRYPOINT 指定的命令。例如：  
  - Dockerfile 示例：  
    ```dockerfile
    FROM ubuntu:18.04
    RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
    ENTRYPOINT ["curl", "-s", "http://myip.ipip.net"]
    ```  
  - 运行镜像时：  
    ```bash
    docker run myip -i
    ```  
    此时 `-i` 会追加到 ENTRYPOINT 的命令后，最终执行的命令类似于：  
    ```bash
    curl -s http://myip.ipip.net -i
    ```  
    达到了既固定默认行为，又可以灵活传递额外参数的效果。（cite1†ENTRYPOINT 入口点）

#### 场景二：应用运行前的准备工作

- **问题描述**  
  某些应用在正式启动前需要执行一些初始化任务或配置工作，例如数据库的初始化、权限设置、用户切换等。  
- **解决方案**  
  可以编写一个脚本，将这些预处理工作放在脚本中，并将该脚本作为 ENTRYPOINT。脚本在执行完成后，再将传入的参数（通常是实际要启动的服务程序）传递下去执行。  
- **典型示例**  
  官方的 Redis 镜像就采用了这种方式。其 Dockerfile 中使用了类似下面的写法：  
  ```dockerfile
  ENTRYPOINT ["docker-entrypoint.sh"]
  CMD ["redis-server"]
  ```  
  在 `docker-entrypoint.sh` 脚本中，会先执行一些必要的初始化操作（比如检查权限、切换到非 root 用户等），最后再执行传入的命令（这里就是 `redis-server`）。这种方式既保证了初始化工作的一致性，又使得镜像的使用更加灵活。（cite1†ENTRYPOINT 入口点）

---

### 总结

- **ENTRYPOINT** 主要用于固定容器启动时的主进程行为，使得镜像可以表现得像一个独立的命令行工具；  
- 与 **CMD** 配合时，CMD 提供默认参数，而运行时可以通过额外参数进行补充；  
- 使用 **exec 格式** 更为推荐，因为它直接以 JSON 数组形式传递参数，不经过 shell 解析，确保命令执行更精确；  
- 在需要预处理、初始化或用户切换的场景中，通过编写启动脚本并将其作为 ENTRYPOINT，可以实现更复杂的启动逻辑。（cite1†ENTRYPOINT 入口点）