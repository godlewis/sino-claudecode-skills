# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-26

### Added
- 初始版本发布
- 支持 DaoCloud 国内镜像源加速
- 支持 5000+ Docker 镜像加速
- 支持主流镜像源：docker.io, gcr.io, ghcr.io, k8s.gcr.io, registry.k8s.io, quay.io
- 自动镜像名称标准化
- 自动镜像重命名
- 自动清理中间镜像标签
- 批量拉取支持
- 完整的错误处理和用户提示

### Features
- 智能镜像名称识别（处理省略 registry 前缀）
- 多镜像源映射配置
- 详细的执行日志输出
- 成功/失败统计
- 性能优化（10-100倍下载速度提升）

### Documentation
- 完整的 SKILL.md 技能定义
- 详细的 README.md 使用说明
- 完善的故障排除指南
- 最佳实践建议

---

## [Unreleased]

### Planned
- 支持更多镜像源（nvcr.io, mcr.microsoft.com 等）
- 支持自定义镜像源配置
- 支持镜像缓存管理
- 添加速度测试功能
- 支持多线程并发拉取
