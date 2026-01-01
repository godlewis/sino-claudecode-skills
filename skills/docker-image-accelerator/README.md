# Docker Image Accelerator

🚀 Docker 镜像加速拉取工具 - 使用 DaoCloud 国内镜像源加速 Docker 镜像下载

## 功能特性

- ⚡ **高速下载** - 使用 DaoCloud 国内镜像源，下载速度提升 10-100 倍
- 🔄 **自动重命名** - 自动将加速镜像重命名为原始镜像名
- 🗑️ **自动清理** - 自动清理中间镜像标签
- 🌍 **全镜像源支持** - 支持 docker.io, gcr.io, ghcr.io, k8s.gcr.io, quay.io 等 5000+ 镜像
- 📦 **智能识别** - 自动识别并标准化各种镜像名称格式
- 🎯 **批量处理** - 支持一次拉取多个镜像

## 适用场景

- 拉取官方 Docker Hub 镜像（docker.io）
- 拉取 Google Container Registry 镜像（gcr.io）
- 拉取 GitHub Container Registry 镜像（ghcr.io）
- 拉取 Kubernetes 镜像（k8s.gcr.io, registry.k8s.io）
- 拉取 Red Hat Quay 镜像（quay.io）
- 镜像下载缓慢或超时的情况
- Kubernetes 集群初始化和部署

## 安装

### 方法1: 使用 CLI 工具（推荐）

```bash
# 在 Claude Code Skills Marketplace 中安装
python scripts/marketplace.py install docker-image-accelerator
```

### 方法2: 手动安装

```bash
# 复制 skill 到 Claude skills 目录
cp -r skills/docker-image-accelerator ~/.claude/skills/

# 重启 Claude Code
```

## 使用方法

### 在 Claude Code 中使用

安装后，直接对话即可：

```
docker pull nginx:latest
```

Claude 会自动调用加速工具：

```
我来帮你加速拉取 nginx:latest 镜像。

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

### 命令行直接使用

```bash
# 拉取单个镜像
python skills/docker-image-accelerator/scripts/accelerate_docker_pull.py nginx:latest

# 拉取多个镜像
python skills/docker-image-accelerator/scripts/accelerate_docker_pull.py nginx:latest redis:7 python:3.9-slim

# 拉取 Kubernetes 镜像
python skills/docker-image-accelerator/scripts/accelerate_docker_pull.py gcr.io/pause:3.1
```

## 支持的镜像源

| 镜像源 | 加速地址 | 示例 |
|--------|---------|------|
| docker.io | m.daocloud.io/docker.io | `nginx:latest` |
| gcr.io | m.daocloud.io/gcr.io | `gcr.io/pause:3.1` |
| ghcr.io | m.daocloud.io/ghcr.io | `ghcr.io/actions/runner:latest` |
| k8s.gcr.io | m.daocloud.io/k8s.gcr.io | `k8s.gcr.io/pause:3.1` |
| registry.k8s.io | m.daocloud.io/registry.k8s.io | `registry.k8s.io/pause:3.1` |
| quay.io | m.daocloud.io/quay.io | `quay.io/coreos/latest` |

完整列表: [DaoCloud public-image-mirror](https://github.com/DaoCloud/public-image-mirror/blob/main/allows.txt)

## 工作原理

1. **识别镜像** - 从用户输入提取 Docker 镜像名称
2. **标准化** - 处理省略 registry 前缀的情况（如 `nginx:latest` → `docker.io/library/nginx:latest`）
3. **转换** - 将原始地址转换为 DaoCloud 加速地址
4. **拉取** - 使用加速源拉取镜像
5. **重命名** - 将加速镜像 tag 为原始镜像名
6. **清理** - 删除加速镜像的临时标签

## 使用示例

### 基础镜像

```
docker pull nginx:latest
docker pull redis:7
docker pull python:3.9-slim
```

### Kubernetes 镜像

```
docker pull k8s.gcr.io/pause:3.1
docker pull registry.k8s.io/kube-apiserver:v1.28.0
```

### 第三方镜像

```
docker pull gcr.io/distroless/static:nonroot
docker pull ghcr.io/actions/runner:latest
docker pull quay.io/coreos/latest:latest
```

## 性能对比

典型场景（国内网络环境）：

| 镜像 | 大小 | 直接拉取 | 加速拉取 | 提升 |
|------|------|---------|---------|------|
| nginx:latest | 140MB | ~5分钟 | ~10秒 | 30x |
| gcr.io/pause:3.1 | 700KB | 超时 | ~5秒 | ∞ |
| python:3.9-slim | 120MB | ~10分钟 | ~15秒 | 40x |
| k8s.gcr.io/kube-apiserver:v1.28.0 | 35MB | 超时 | ~8秒 | ∞ |

## 依赖要求

- Python 3.6+
- Docker 已安装并运行
- 网络连接

## 配置

### Docker 配置（可选）

如果希望全局使用镜像加速，可以配置 Docker daemon：

编辑 `/etc/docker/daemon.json`:

```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io"
  ]
}
```

重启 Docker：

```bash
sudo systemctl restart docker  # Linux
# 或重启 Docker Desktop (Windows/Mac)
```

**注意**: 全局配置只对 docker.io 有效，其他镜像源仍需要使用本工具。

### Containerd 配置

编辑 `/etc/containerd/config.toml`:

```toml
[plugins."io.containerd.grpc.v1.cri".registry]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
    [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
      endpoint = ["https://docker.m.daocloud.io"]
    [plugins."io.containerd.grpc.v1.cri".registry.mirrors."k8s.gcr.io"]
      endpoint = ["https://k8s-gcr.m.daocloud.io"]
```

## 故障排除

### 拉取失败

**问题**: 拉取失败，提示镜像不存在

**解决方案**:
1. 检查镜像名称和 tag 是否正确
2. 查看 [同步队列状态](https://queue.m.daocloud.io/status/)
3. 尝试使用明确版本号而非 `latest`

### 重命名失败

**问题**: 镜像已拉取但重命名失败

**解决方案**:
- 手动重命名：
  ```bash
  docker tag <加速镜像地址> <原始镜像名>
  docker rmi <加速镜像地址>
  ```

### Docker 未运行

**问题**: 提示 Docker 未运行

**解决方案**:
```bash
# 检查 Docker 状态
docker info

# 启动 Docker
sudo systemctl start docker  # Linux
```

## 最佳实践

### 1. 使用明确版本号

```bash
# ✅ 推荐
docker pull nginx:1.24.0

# ⚠️  避免
docker pull nginx:latest
```

### 2. 闲时下载大镜像

建议在凌晨（北京时间 01-07 点）下载，网络不拥堵。

### 3. Kubernetes 集群

```bash
# kubeadm
kubeadm config images pull --image-repository k8s-gcr.m.daocloud.io

# kind
kind create cluster --image m.daocloud.io/docker.io/kindest/node:v1.28.0
```

## 工作原理详解

### DaoCloud 镜像服务

- **后端**: OpenCIDN
- **同步机制**: 懒加载 + 缓存
- **一致性**: 所有 hash(sha256) 与源保持一致
- **延迟**: 可能存在 1 小时缓存延迟
- **清理**: 不定期清理缓存

### 镜像地址转换

```python
# 示例转换
nginx:latest                    # 用户输入
↓
docker.io/library/nginx:latest  # 标准化
↓
m.daocloud.io/docker.io/library/nginx:latest  # 加速地址
```

## 参考资源

- [DaoCloud Public Image Mirror](https://github.com/DaoCloud/public-image-mirror)
- [OpenCIDN 项目](https://github.com/OpenCIDN)
- [同步队列状态](https://queue.m.daocloud.io/status/)
- [DaoCloud 二进制文件加速](https://github.com/DaoCloud/public-binary-files-mirror)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

感谢 [DaoCloud](https://www.daocloud.io/) 提供公共镜像服务！
