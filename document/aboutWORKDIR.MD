该页面详细介绍了 Dockerfile 中 **WORKDIR 指令** 的作用、语法规则以及使用注意事项，下面结合具体内容进行详细讲解：

---

### 1. WORKDIR 指令的作用

- **设置工作目录**  
  WORKDIR 用于指定后续所有命令（如 RUN、CMD、ENTRYPOINT、COPY、ADD 等）的工作目录。  
  - 这意味着在这些命令中使用的相对路径都是基于 WORKDIR 指定的目录。

- **目录自动创建**  
  如果指定的目录不存在，Docker 会自动创建该目录。这样可以避免在每个命令中手动使用 mkdir 创建目录。

---

### 2. 语法格式

WORKDIR 指令有一个简单的格式：
  
```dockerfile
WORKDIR <目录路径>
```

- **绝对路径或相对路径**  
  - 如果给定绝对路径，则直接设置为该目录。  
  - 如果是相对路径，则相对于上一个 WORKDIR 的路径进行追加。这使得在同一个 Dockerfile 中可以通过多次 WORKDIR 指令构建层级目录结构。

例如：
  
```dockerfile
WORKDIR /app
WORKDIR src
```

此时，最终的工作目录会是 `/app/src`。

---

### 3. 使用场景与示例

- **简化命令书写**  
  使用 WORKDIR 后，不需要在每个命令中都写全路径。例如：
  
  ```dockerfile
  FROM node:14
  WORKDIR /app
  COPY package.json ./
  RUN npm install
  COPY . .
  CMD ["node", "app.js"]
  ```
  
  这样所有相对路径（如 `./`）都默认基于 `/app` 目录，保持 Dockerfile 清晰易懂。

- **多层目录结构**  
  可以通过多个 WORKDIR 指令构造层级目录结构，有助于管理大型项目或将不同模块分开处理。例如：
  
  ```dockerfile
  FROM python:3.9
  WORKDIR /usr/src/app
  COPY requirements.txt ./
  RUN pip install --no-cache-dir -r requirements.txt
  WORKDIR /usr/src/app/src
  COPY . .
  CMD ["python", "main.py"]
  ```
  
  这里先在 `/usr/src/app` 下安装依赖，再切换到 `/usr/src/app/src` 目录来复制和运行应用代码。

---

### 4. 注意事项

- **相对路径累计**  
  如果在 Dockerfile 中多次使用 WORKDIR，后续的路径会基于上一次 WORKDIR 的结果累加。例如，从 `/app` 开始再切换到 `src`，最终路径变为 `/app/src`。

- **与其他命令的配合**  
  WORKDIR 的设置会影响后续所有需要工作目录的命令，因此在编写 Dockerfile 时要合理规划目录结构，避免路径混乱。

- **可读性和维护性**  
  明确设置工作目录不仅能减少命令中的冗余路径，也使 Dockerfile 更易于维护和理解。

---

### 总结

**WORKDIR 指令** 通过为后续命令设置统一的工作目录，帮助你在 Dockerfile 中管理文件路径、组织代码结构，并自动创建目录（如果不存在），从而提高了构建脚本的简洁性和可维护性。  
这种方式既能避免重复的路径书写，又能使镜像构建过程更加清晰和模块化。（cite1†WORKDIR 指定工作目录）

从某种意义上说，WORKDIR 的作用类似于 Linux 中的 cd 命令——它为后续命令设置了一个工作目录。不过需要注意几点：

- **非交互性**：WORKDIR 并不会在容器运行时改变当前目录，它只是在 Dockerfile 构建过程中为 RUN、COPY、ADD 等指令提供一个默认的工作目录。
- **自动创建目录**：如果指定的目录不存在，WORKDIR 会自动创建，而 cd 命令不会创建目录。
- **作用范围不同**：cd 只对当前 shell 会话有效，而 WORKDIR 对整个 Dockerfile 中后续指令都生效。

因此，虽然概念上类似于 cd（即“切换目录”），但 WORKDIR 更像是为 Dockerfile 后续操作设定一个默认路径环境。（cite1†WORKDIR 指定工作目录）