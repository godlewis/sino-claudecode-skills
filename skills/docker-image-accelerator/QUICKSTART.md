# Docker Image Accelerator - 快速测试指南

## 安装测试

```bash
# 1. 安装 skill 到本地
python scripts/marketplace.py install docker-image-accelerator

# 2. 验证安装
ls ~/.claude/skills/docker-image-accelerator/
```

## 功能测试

### 测试 1: 简单镜像拉取

```bash
# 测试拉取 nginx 镜像
python skills/docker-image-accelerator/scripts/accelerate_docker_pull.py nginx:latest

# 验证镜像是否成功
docker images | grep nginx
```

**预期结果**:
- 镜像名称应为 `nginx:latest`（原始名称）
- 不应包含 `m.daocloud.io` 前缀

### 测试 2: Kubernetes 镜像拉取

```bash
# 测试拉取 Kubernetes pause 镜像
python skills/docker-image-accelerator/scripts/accelerate_docker_pull.py gcr.io/pause:3.1

# 验证镜像
docker images | grep pause
```

### 测试 3: 批量拉取

```bash
# 测试批量拉取多个镜像
python skills/docker-image-accelerator/scripts/accelerate_docker_pull.py nginx:latest redis:7 python:3.9-slim

# 验证所有镜像
docker images | grep -E "nginx|redis|python"
```

### 测试 4: 各种格式测试

```bash
# 测试不同的镜像名称格式
python skills/docker-image-accelerator/scripts/accelerate_docker_pull.py \
    alpine:latest \
    docker.io/library/busybox:latest \
    gcr.io/distroless/static:nonroot
```

## Claude Code 中测试

安装 skill 后，在 Claude Code 中对话：

```
docker pull nginx:latest
```

Claude 应该会：
1. 识别出需要拉取 Docker 镜像
2. 调用加速脚本
3. 显示加速拉取过程
4. 成功重命名为原始镜像名
5. 清理中间镜像标签

## 性能对比

### 不使用加速（如果可以访问）

```bash
time docker pull nginx:latest
```

### 使用加速

```bash
time python skills/docker-image-accelerator/scripts/accelerate_docker_pull.py nginx:latest
```

**预期**: 加速版本应该快 10-100 倍

## 验证清单

- [ ] 镜像成功拉取
- [ ] 镜像名称为原始名称（无 m.daocloud.io 前缀）
- [ ] 没有残留的加速镜像标签
- [ ] 可以正常使用镜像（如 `docker run nginx:latest`）
- [ ] 批量拉取正常工作
- [ ] 各种镜像格式都正确识别

## 故障排除

### 问题: 镜像拉取失败

**解决方案**:
1. 检查网络连接
2. 验证镜像名称是否正确
3. 查看 [同步队列状态](https://queue.m.daocloud.io/status/)

### 问题: 重命名失败

**解决方案**:
```bash
# 手动重命名
docker tag <加速镜像地址> <原始镜像名>
docker rmi <加速镜像地址>
```

### 问题: Docker 未运行

**解决方案**:
```bash
# 启动 Docker
sudo systemctl start docker  # Linux
# 或启动 Docker Desktop (Windows/Mac)
```

## 清理测试镜像

```bash
# 删除测试镜像
docker rmi nginx:latest redis:7 python:3.9-slim gcr.io/pause:3.1
```

## 下一步

- 阅读完整 [README](README.md)
- 查看 [更新日志](CHANGELOG.md)
- 了解 [技能定义](SKILL.md)
