---
name: docker-image-accelerator
description: 'Docker 镜像加速拉取工具。自动使用 DaoCloud 国内镜像源加速 Docker 镜像下载，特别适用于拉取官方镜像和国外镜像源（docker.io, gcr.io, ghcr.io, k8s.gcr.io, quay.io 等）。自动完成镜像拉取、重命名为原始镜像名、清理中间镜像标签等操作。当用户需要 docker pull 拉取镜像、镜像下载缓慢、需要加速 Docker 镜像下载、拉取 Kubernetes 相关镜像时使用此 skill。'
license: MIT
---

# Docker Image Accelerator - 镜像加速拉取工具

## 快速开始

当用户请求拉取 Docker 镜像时，按以下流程执行：

1. **识别镜像地址** - 从用户输入中提取 Docker 镜像名称
2. **标准化镜像名** - 处理省略 registry 前缀的情况（如 `nginx:latest`）
3. **转换加速地址** - 将原始地址转换为 DaoCloud 加速地址
4. **拉取镜像** - 使用加速源拉取镜像
5. **重命名镜像** - 将加速镜像 tag 为原始镜像名
6. **清理中间标签** - 删除加速镜像的临时标签
7. **输出结果** - 通知用户镜像已成功拉取

## 工作原理

### 镜像源映射

本工具使用 DaoCloud 公共镜像仓库（https://github.com/DaoCloud/public-image-mirror）加速，支持 5000+ 镜像：

| 原始镜像源 | 加速镜像地址 | 示例 |
|-----------|------------|------|
| docker.io | m.daocloud.io/docker.io | nginx:latest → m.daocloud.io/docker.io/library/nginx:latest |
| gcr.io | m.daocloud.io/gcr.io | gcr.io/pause:3.1 → m.daocloud.io/gcr.io/pause:3.1 |
| ghcr.io | m.daocloud.io/ghcr.io | ghcr.io/actions/runner:latest → m.daocloud.io/ghcr.io/actions/runner:latest |
| k8s.gcr.io | m.daocloud.io/k8s.gcr.io | k8s.gcr.io/pause:3.1 → m.daocloud.io/k8s.gcr.io/pause:3.1 |
| registry.k8s.io | m.daocloud.io/registry.k8s.io | registry.k8s.io/pause:3.1 → m.daocloud.io/registry.k8s.io/pause:3.1 |
| quay.io | m.daocloud.io/quay.io | quay.io/coreos/latest → m.daocloud.io/quay.io/coreos/latest |

### 镜像名称标准化

工具会自动处理各种镜像名称格式：

```bash
# 省略 registry（官方镜像）
nginx:latest                    → docker.io/library/nginx:latest
python:3.9-slim                → docker.io/library/python:3.9-slim

# 省略 docker.io
library/nginx:latest           → docker.io/library/nginx:latest
nginx/nginx:latest             → docker.io/nginx/nginx:latest

# 完整格式
gcr.io/pause:3.1               → gcr.io/pause:3.1（保持不变）
```

### 执行流程

1. **转换地址**
   ```bash
   原始: nginx:latest
   标准化: docker.io/library/nginx:latest
   加速: m.daocloud.io/docker.io/library/nginx:latest
   ```

2. **拉取镜像**
   ```bash
   docker pull m.daocloud.io/docker.io/library/nginx:latest
   ```

3. **重命名**
   ```bash
   docker tag m.daocloud.io/docker.io/library/nginx:latest nginx:latest
   ```

4. **清理**
   ```bash
   docker rmi m.daocloud.io/docker.io/library/nginx:latest
   ```

5. **最终结果**
   ```bash
   # 用户本地的镜像
   REPOSITORY   TAG       IMAGE ID
   nginx        latest    abcd1234...
   ```

## 使用示例

### 基本使用

用户输入:
```
docker pull nginx:latest
```

Claude回应:
```
我来帮你加速拉取 nginx:latest 镜像。

[执行加速脚本]
✨ 原始镜像: nginx:latest
📝 标准化后: docker.io/library/nginx:latest
🚀 加速镜像: m.daocloud.io/docker.io/library/nginx:latest
📥 正在拉取镜像: m.daocloud.io/docker.io/library/nginx:latest
✅ 拉取成功
🏷️  正在重命名: m.daocloud.io/docker.io/library/nginx:latest -> nginx:latest
✅ 重命名成功
🗑️  正在删除加速镜像标签: m.daocloud.io/docker.io/library/nginx:latest
✅ 清理完成

🎉 镜像 'nginx:latest' 已成功拉取并配置！
```

### Kubernetes 镜像

用户输入:
```
我需要拉取 k8s.gcr.io/pause:3.1 镜像
```

Claude回应:
```
我来帮你使用国内加速源拉取 Kubernetes 镜像。

[执行加速脚本]
✨ 原始镜像: k8s.gcr.io/pause:3.1
📝 标准化后: k8s.gcr.io/pause:3.1
🚀 加速镜像: m.daocloud.io/k8s.gcr.io/pause:3.1
[... 拉取过程 ...]

🎉 镜像 'k8s.gcr.io/pause:3.1' 已成功拉取并配置！
```

### 多镜像批量拉取

用户输入:
```
拉取这些镜像：nginx redis:7 python:3.9
```

Claude回应:
```
我来帮你加速拉取这些镜像。

[为每个镜像执行加速脚本]

📊 总结:
   ✅ 成功: 3
   ❌ 失败: 0
```

## 触发条件

当用户提到以下关键词时，触发此 skill：

- `docker pull <镜像名>`
- `拉取镜像`、`下载镜像`、`pull 镜像`
- `镜像下载慢`、`加速下载镜像`
- 提到具体的 Docker 镜像名称（如 `nginx`, `redis`, `gcr.io/xxx`）
- Kubernetes 相关镜像拉取场景

## 不适用的场景

- 镜像已经在本地存在
- 使用私有镜像仓库（非公开镜像源）
- 需要认证的镜像仓库
- 非 Docker 容器运行时（如 podman, containerd 直接使用）

## 工具使用

### 核心脚本

使用 `scripts/accelerate_docker_pull.py` 脚本执行加速拉取：

```bash
# 单个镜像
python scripts/accelerate_docker_pull.py nginx:latest

# 多个镜像
python scripts/accelerate_docker_pull.py nginx:latest redis:7 python:3.9-slim

# Kubernetes 镜像
python scripts/accelerate_docker_pull.py gcr.io/pause:3.1
```

### 参数说明

脚本接受一个或多个镜像名称作为参数：

- 支持短格式：`nginx:latest`
- 支持完整格式：`docker.io/library/nginx:latest`
- 支持所有主流镜像源：docker.io, gcr.io, ghcr.io, k8s.gcr.io, quay.io 等

### 返回值

- `0`: 所有镜像拉取成功
- `1`: 至少有一个镜像拉取失败

## 依赖要求

- Python 3.6+
- Docker 已安装并运行
- 网络连接（访问 DaoCloud 镜像源）

## 故障排除

### 拉取失败

如果拉取失败，可能原因：

1. **镜像不存在**
   - 检查镜像名称和 tag 是否正确
   - 访问 DaoCloud 镜像队列: https://queue.m.daocloud.io/status/

2. **网络问题**
   - 检查网络连接
   - 尝试使用其他加速源

3. **Docker 未运行**
   ```bash
   # 检查 Docker 状态
   docker info

   # 启动 Docker
   sudo systemctl start docker  # Linux
   # 或启动 Docker Desktop (Windows/Mac)
   ```

### 重命名失败

如果重命名失败但镜像已拉取：

- 镜像仍会以加速地址的标签存在
- 可以手动重命名：
  ```bash
  docker tag m.daocloud.io/docker.io/library/nginx:latest nginx:latest
  docker rmi m.daocloud.io/docker.io/library/nginx:latest
  ```

## 最佳实践

### 1. 使用明确版本号

```bash
# ✅ 推荐：使用明确版本号
docker pull nginx:1.24.0

# ⚠️  避免：使用 latest 标签
docker pull nginx:latest
```

原因：latest 标签可能变化，且缓存机制可能导致延迟。

### 2. 闲时下载

建议在凌晨（北京时间 01-07 点）下载大镜像，此时网络不拥堵。

### 3. Kubernetes 集群

对于 Kubernetes 集群：

```bash
# kubeadm 初始化
kubeadm config images pull --image-repository k8s-gcr.m.daocloud.io

# kind 创建集群
kind create cluster --image m.daocloud.io/docker.io/kindest/node:v1.28.0
```

## 技术细节

### DaoCloud 镜像服务

- **后端服务**: OpenCIDN
- **同步机制**: 懒加载 + 缓存
- **一致性**: 所有 hash(sha256) 与源保持一致
- **延迟**: 可能存在 1 小时缓存延迟
- **清理**: 不定期清理缓存

### 支持的镜像源

完整列表参考：https://github.com/DaoCloud/public-image-mirror/blob/main/allows.txt

主要支持：
- docker.io (1000+ 镜像)
- gcr.io (Google Container Registry)
- ghcr.io (GitHub Container Registry)
- k8s.gcr.io / registry.k8s.io (Kubernetes)
- quay.io (Red Hat Quay)
- mcr.microsoft.com (Microsoft)
- nvcr.io (NVIDIA)
- 等等 5000+ 镜像

### 性能对比

典型场景（国内网络）：

| 镜像 | 直接拉取 | 加速拉取 | 提升 |
|------|---------|---------|------|
| nginx:latest | ~5分钟 | ~10秒 | 30x |
| gcr.io/pause:3.1 | 超时 | ~5秒 | ∞ |
| python:3.9 | ~10分钟 | ~15秒 | 40x |

## 扩展阅读

- [DaoCloud Public Image Mirror](https://github.com/DaoCloud/public-image-mirror)
- [DaoCloud 二进制文件加速](https://github.com/DaoCloud/public-binary-files-mirror)
- [OpenCIDN 项目](https://github.com/OpenCIDN)
- [同步队列状态](https://queue.m.daocloud.io/status/)
