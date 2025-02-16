该页面详细介绍了 Dockerfile 中的 **ARG** 指令，主要用于在镜像构建阶段定义构建参数。这些参数可以让你在构建时动态传入变量，从而使 Dockerfile 更加灵活。下面是对其主要内容的详细讲解：

---

### 1. ARG 的基本作用

- **定义构建时参数**  
  使用 ARG 指令可以在 Dockerfile 中声明构建参数，这些参数的值仅在镜像构建过程中有效，而不会保留到最终的镜像中。  
- **与 ENV 的区别**  
  与 ENV 指令不同，ENV 定义的环境变量在容器运行时依然存在，而 ARG 变量只在构建阶段起作用。这意味着你可以利用 ARG 在构建时动态指定某些值，但这些值在容器启动后并不可见。

---

### 2. ARG 的语法格式

- **基本格式**  
  ```dockerfile
  ARG <变量名>[=<默认值>]
  ```  
  例如：
  ```dockerfile
  ARG APP_VERSION=1.0
  ```
  如果在构建时没有传递其他值，则 `APP_VERSION` 默认取值为 `1.0`。

- **引用构建参数**  
  在 Dockerfile 后续的指令中，可以使用 `${变量名}` 或 `$变量名` 的方式引用这些参数，例如：
  ```dockerfile
  RUN echo "Building application version ${APP_VERSION}"
  ```

---

### 3. 如何使用 ARG 传递参数

- **构建时覆盖默认值**  
  在构建镜像时，可以使用 `--build-arg` 选项为 ARG 变量传递新的值，从而覆盖 Dockerfile 中定义的默认值。例如：
  ```bash
  docker build --build-arg APP_VERSION=2.0 -t myapp .
  ```
  这样，在构建过程中，`${APP_VERSION}` 的值将为 `2.0`。

- **在 FROM 指令之前使用 ARG**  
  从 Docker 17.05 版本开始，ARG 指令还可以在 FROM 指令之前使用，以便在选择基础镜像时也能利用构建参数。例如：
  ```dockerfile
  ARG BASE_IMAGE=ubuntu:18.04
  FROM ${BASE_IMAGE}
  ```
  这样可以根据构建时传入的参数动态选择不同的基础镜像。

---

### 4. 注意事项

- **作用范围**  
  ARG 定义的变量只在构建阶段有效，构建完成后它们不会存在于最终生成的镜像中。如果需要在容器运行时使用变量，应使用 ENV 指令。
- **默认值与空值**  
  如果未为 ARG 指令提供默认值，并且在构建时也未传递相应参数，那么引用该变量时将为空字符串。
- **构建灵活性**  
  通过 ARG，可以让同一个 Dockerfile 构建出多种变体镜像，只需在构建时传入不同的参数即可，从而大大提高了 Dockerfile 的复用性和灵活性。

---

### 5. 示例说明

下面是一个实际示例，展示了如何利用 ARG 指令动态指定基础镜像和应用版本：

```dockerfile
# 定义基础镜像参数，可在构建时通过 --build-arg 覆盖默认值
ARG BASE_IMAGE=ubuntu:18.04
FROM ${BASE_IMAGE}

# 定义应用版本参数
ARG APP_VERSION=1.0
RUN echo "Building application version ${APP_VERSION}"
```

在构建时，如果需要使用其他版本或不同的基础镜像，只需执行类似以下命令：
```bash
docker build --build-arg BASE_IMAGE=debian:10 --build-arg APP_VERSION=2.0 -t myapp .
```
这样，构建过程中会使用 `debian:10` 作为基础镜像，并将应用版本设置为 `2.0`。

---

综上所述，**ARG** 指令为 Dockerfile 提供了参数化支持，使得构建过程能够根据不同需求动态调整变量值，但这些变量仅在构建阶段生效，不会出现在最终镜像中。（cite1†ARG 构建参数）
下面举几个例子，展示如何在 Dockerfile 中通过 ARG 取得不同值，从而导致构建结果出现分歧：

---

### 示例 1：动态选择基础镜像

在下面的 Dockerfile 中，通过 ARG 定义了基础镜像参数，可以在构建时传入不同的值来选择不同的基础镜像：

```dockerfile
# 定义基础镜像参数，默认值为 ubuntu:20.04
ARG BASE_IMAGE=ubuntu:20.04
FROM ${BASE_IMAGE}

RUN apt-get update && apt-get install -y curl
```

- **构建默认镜像：**  
  ```
  docker build -t myapp .
  ```  
  使用默认的 `ubuntu:20.04` 作为基础镜像。

- **传入不同的基础镜像：**  
  ```
  docker build --build-arg BASE_IMAGE=debian:10 -t myapp .
  ```  
  此时基础镜像变为 `debian:10`，构建出的镜像在系统环境和包管理工具等方面会有所不同。

---

### 示例 2：改变应用版本

通过 ARG 设置应用版本，在构建过程中用这个版本号来决定安装或配置哪个版本的应用：

```dockerfile
FROM alpine:3.12

# 定义应用版本参数，默认版本为 1.0
ARG APP_VERSION=1.0
# 将版本信息写入文件中，作为后续验证的依据
RUN echo "App Version: ${APP_VERSION}" > /app/version.txt
```

- **构建默认版本镜像：**  
  ```
  docker build -t myapp .
  ```  
  此时生成的 `/app/version.txt` 文件内容为 `App Version: 1.0`。

- **构建新版镜像：**  
  ```
  docker build --build-arg APP_VERSION=2.0 -t myapp:v2 .
  ```  
  此时生成的文件内容为 `App Version: 2.0`，应用的版本信息就不同了。

---

### 示例 3：切换安装不同的软件版本

比如你需要安装不同版本的 Node.js，通过 ARG 传入不同版本号，Dockerfile 根据这个值拉取相应版本的 Node.js 镜像：

```dockerfile
# 定义 Node.js 版本参数，默认版本为 14
ARG NODE_VERSION=14
FROM node:${NODE_VERSION}

WORKDIR /app
COPY . .

RUN npm install
CMD ["node", "app.js"]
```

- **默认构建：**  
  ```
  docker build -t mynodeapp .
  ```  
  会基于 `node:14` 构建镜像。

- **传入不同版本：**  
  ```
  docker build --build-arg NODE_VERSION=16 -t mynodeapp:16 .
  ```  
  此时将基于 `node:16` 构建镜像，所包含的 Node.js 版本不同，可能会影响依赖和运行时行为。

---

### 总结

通过在 Dockerfile 中使用 ARG 指令，可以使构建过程参数化：  
- **灵活性高：** 同一份 Dockerfile 能根据构建时传入的参数构建出不同的镜像。  
- **维护方便：** 改变参数值而不需要修改 Dockerfile 逻辑，即可实现不同环境或版本的构建。  
- **分歧效果明显：** 不同的参数值可能导致系统基础、软件版本、配置文件内容等各方面的差异，从而影响最终容器的行为和功能。

这些例子展示了如何利用 ARG 在 Dockerfile 中取得不同值，从而产生分歧的构建结果。