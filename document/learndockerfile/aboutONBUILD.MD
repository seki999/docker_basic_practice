该页面详细介绍了 Dockerfile 中的 **ONBUILD 指令** 的用途、工作机制及使用场景，下面结合页面内容做详细讲解：

---

### 1. ONBUILD 指令的基本概念

- **延迟触发的构建指令**  
  ONBUILD 指令用于在构建基于当前镜像的下游镜像时自动触发执行。也就是说，当你构建一个新镜像（子镜像）时，如果基础镜像中包含 ONBUILD 指令，这些指令就会被自动执行。
  
- **适用于构建可重用的基础镜像**  
  这种机制主要用于制作基础镜像（如语言运行时、框架镜像等），以便后续的应用镜像可以继承这些预定义的构建步骤，而不需要在每个 Dockerfile 中重复编写。

---

### 2. ONBUILD 的语法与使用

- **基本语法**  
  ONBUILD 指令的书写格式与其他指令类似，例如：
  ```dockerfile
  ONBUILD COPY . /app/src
  ```
  这表示当该镜像被用作基础镜像构建子镜像时，会自动执行 `COPY . /app/src` 操作。

- **支持的指令**  
  ONBUILD 可以与多种 Dockerfile 指令配合使用，如 COPY、ADD、RUN、CMD 等，但通常不建议在 ONBUILD 指令中使用一些可能引发歧义的操作。

---

### 3. 使用场景与示例

#### 示例 1：基础镜像的预设构建步骤

假设你想构建一个 Node.js 基础镜像，让所有基于它构建的镜像都默认将代码复制到 `/usr/src/app` 并安装依赖，可以这样写：
```dockerfile
# 基础镜像 Dockerfile
FROM node:14

# ONBUILD 指令，子镜像在构建时自动执行
ONBUILD COPY package.json /usr/src/app/
ONBUILD RUN cd /usr/src/app && npm install
ONBUILD COPY . /usr/src/app

# 后续的应用镜像只需基于这个镜像构建
```
当其他开发者使用这个基础镜像构建他们的应用镜像时，不需要再重复编写复制和安装依赖的命令，ONBUILD 指令会自动执行。

#### 示例 2：定制化镜像构建

在某些情况下，你可能希望让基础镜像预定义一些构建步骤，但又希望在子镜像中能够覆盖或扩展这些步骤。通过 ONBUILD 指令，可以使基础镜像在构建下游镜像时执行特定任务，从而保证一致的构建流程。

---

### 4. 注意事项

- **不可逆转性**  
  一旦使用 ONBUILD 指令构建了基础镜像，所有基于该镜像构建的子镜像都会自动触发这些命令，因此在制作公共基础镜像时，要谨慎考虑是否所有用户都适用这些默认步骤。

- **调试与维护**  
  由于 ONBUILD 指令在子镜像构建时才会触发，其行为可能不易在基础镜像构建时被发现。建议在设计基础镜像时，明确记录 ONBUILD 指令的作用，并在文档中加以说明，以便使用者了解。

- **适用场景限制**  
  ONBUILD 指令主要适用于构建框架或库类的基础镜像，而对于大多数应用镜像而言，直接编写 Dockerfile 可能更直观和灵活。

---

### 总结

**ONBUILD 指令** 为基础镜像的构建提供了一种“延迟执行”机制，使得在构建子镜像时自动执行预定义的构建步骤，简化了下游镜像的开发流程。然而，由于它会对所有基于该镜像构建的子镜像生效，使用时需要非常谨慎，并清晰地在文档中说明其行为和预期用途。（cite1†ONBUILD 为他人作嫁衣裳）

下面提供一个详细的例子，演示如何使用 ONBUILD 指令构建基础镜像，再基于该基础镜像构建子镜像，并展示构建、运行以及检查镜像和容器状态的整个过程。

---

## 1. 编写基础镜像的 Dockerfile（Dockerfile.base）

假设我们希望构建一个 Node.js 基础镜像，预定义好复制项目文件、安装依赖的步骤。我们可以在基础镜像中使用 ONBUILD 指令，这样当基于该镜像构建子镜像时，会自动触发这些步骤。

**内容如下：**

```dockerfile
# Dockerfile.base
FROM node:14

# 设置工作目录
WORKDIR /usr/src/app

# 当有下游镜像基于本镜像构建时，自动执行以下命令：
# 1. 将 package.json 文件复制到工作目录
ONBUILD COPY package.json /usr/src/app/
# 2. 安装项目依赖
ONBUILD RUN npm install
# 3. 将其他所有文件复制到工作目录
ONBUILD COPY . /usr/src/app
```

**说明：**

- 当我们基于此基础镜像构建子镜像时，子镜像构建上下文中必须包含 package.json（以及后续要复制的文件），否则 ONBUILD 指令会失败。

---

## 2. 构建基础镜像

在包含 Dockerfile.base 的目录下（假设没有其他不相关的文件），执行以下命令构建基础镜像：

```bash
docker build -t mynode-base -f Dockerfile.base .
```

构建完成后，可以用以下命令查看镜像列表，确认镜像已生成：

```bash
docker images
```

你会看到一个名为 `mynode-base` 的镜像。

---

## 3. 编写子镜像的 Dockerfile（Dockerfile.child）

在构建子镜像时，Docker 会自动触发基础镜像中定义的 ONBUILD 指令。为此，我们需要准备一个构建上下文，包括一个简单的 Node.js 项目文件，如 package.json 和 server.js。

**示例文件：**

- **package.json**

  ```json
  {
    "name": "demo-app",
    "version": "1.0.0",
    "dependencies": {
      "express": "^4.17.1"
    }
  }
  ```

- **server.js**

  ```javascript
  const express = require('express');
  const app = express();
  const port = 3000;
  
  app.get('/', (req, res) => res.send('Hello from child image!'));
  
  app.listen(port, () => console.log(`App listening on port ${port}!`));
  ```

**子镜像 Dockerfile：**

```dockerfile
# Dockerfile.child
# 使用刚才构建的基础镜像作为父镜像
FROM mynode-base

# 这里 ONBUILD 指令会自动执行：
#   COPY package.json /usr/src/app/
#   RUN npm install
#   COPY . /usr/src/app
# 也就是说，会将当前目录下的 package.json 和 server.js复制到 /usr/src/app 并安装依赖

# 指定容器启动命令，运行我们的 Node.js 应用
CMD ["node", "server.js"]
```

将以上 Dockerfile.child、package.json、server.js 放在同一目录中。

---

## 4. 构建子镜像

在子镜像构建上下文所在的目录中，执行：

```bash
docker build -t mynode-child -f Dockerfile.child .
```

构建过程中，会自动执行基础镜像中的 ONBUILD 指令：
- 首先会复制 package.json 到 `/usr/src/app`
- 然后执行 `npm install` 安装依赖
- 最后将整个构建上下文（包括 server.js 等文件）复制到 `/usr/src/app`

构建完成后，可以再次使用 `docker images` 查看是否生成了 `mynode-child` 镜像。

---

## 5. 运行子镜像并检查状态

启动一个容器来运行我们的 Node.js 应用：

```bash
docker run -d -p 3000:3000 --name demo-app mynode-child
```

- `-d` 表示后台运行  
- `-p 3000:3000` 将容器内的 3000 端口映射到宿主机的 3000 端口  
- `--name demo-app` 为容器命名

检查容器状态：

```bash
docker ps
```

你应能看到名为 `demo-app` 的容器在运行。

如果需要查看容器日志，确认应用启动正常：

```bash
docker logs demo-app
```

此外，你可以在浏览器中访问 [http://localhost:3000](http://localhost:3000) 来查看是否显示 “Hello from child image!”。

---

## 6. 总结流程

1. **基础镜像构建**：  
   - 编写 Dockerfile.base，定义 ONBUILD 指令。  
   - 执行 `docker build -t mynode-base -f Dockerfile.base .` 构建基础镜像。

2. **子镜像构建**：  
   - 准备构建上下文（包含 package.json、server.js 等文件）。  
   - 编写 Dockerfile.child，FROM 指向 `mynode-base`。  
   - 执行 `docker build -t mynode-child -f Dockerfile.child .` 构建子镜像，此时 ONBUILD 指令自动触发。

3. **运行与验证**：  
   - 使用 `docker run` 启动子镜像容器并映射端口。  
   - 通过 `docker ps`、`docker logs` 检查容器状态，并访问服务验证效果。

这种流程利用 ONBUILD 指令使得基础镜像预定义了标准构建步骤，而子镜像只需专注于自己的业务代码，大大简化了构建流程和维护成本。