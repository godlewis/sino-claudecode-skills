#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker 镜像加速拉取脚本
使用 DaoCloud 国内镜像源加速 Docker 镜像下载
"""

import subprocess
import sys
import re
from typing import Optional, Tuple


# 镜像源映射配置
REGISTRY_MIRRORS = {
    # 添加前缀方式（推荐）
    "docker.io": "m.daocloud.io/docker.io",
    "gcr.io": "m.daocloud.io/gcr.io",
    "ghcr.io": "m.daocloud.io/ghcr.io",
    "k8s.gcr.io": "m.daocloud.io/k8s.gcr.io",
    "registry.k8s.io": "m.daocloud.io/registry.k8s.io",
    "quay.io": "m.daocloud.io/quay.io",
    "k8s-gcr.m.daocloud.io": "m.daocloud.io/k8s.gcr.io",
    "docker.m.daocloud.io": "m.daocloud.io/docker.io",
    "elastic.m.daocloud.io": "m.daocloud.io/docker.elastic.co",
    "gcr.m.daocloud.io": "m.daocloud.io/gcr.io",
    "ghcr.m.daocloud.io": "m.daocloud.io/ghcr.io",
    "k8s.m.daocloud.io": "m.daocloud.io/registry.k8s.io",
    "mcr.m.daocloud.io": "m.daocloud.io/mcr.microsoft.com",
    "nvcr.m.daocloud.io": "m.daocloud.io/nvcr.io",
    "quay.m.daocloud.io": "m.daocloud.io/quay.io",
}


def normalize_image_name(image: str) -> str:
    """
    标准化镜像名称，处理省略 docker.io 的情况

    Args:
        image: 原始镜像名称

    Returns:
        str: 标准化的镜像名称
    """
    # 如果没有 registry 前缀，默认添加 docker.io/library/
    if '/' not in image:
        return f"docker.io/library/{image}"

    # 如果只有一层路径，可能是官方镜像，添加 docker.io/library/
    parts = image.split('/')
    if len(parts) == 2:
        # 检查第一部分是否是 registry（包含点号）还是用户/组织名
        if '.' not in parts[0] and ':' not in parts[0]:
            # 例如: nginx:latest, python:3.9, library/nginx, nginx/nginx
            return f"docker.io/{image}"

    return image


def convert_to_mirror_image(image: str) -> Optional[str]:
    """
    将原始镜像地址转换为 DaoCloud 加速镜像地址

    Args:
        image: 原始镜像地址（已标准化）

    Returns:
        Optional[str]: 加速镜像地址，如果不支持则返回 None
    """
    # 提取 registry 部分
    parts = image.split('/', 1)
    if len(parts) < 2:
        return None

    registry = parts[0]
    rest = parts[1] if len(parts) > 1 else ""

    # 检查是否在支持的镜像源中
    if registry in REGISTRY_MIRRORS:
        mirror_registry = REGISTRY_MIRRORS[registry]
        return f"{mirror_registry}/{rest}" if rest else mirror_registry

    # 如果已经是 m.daocloud.io 格式，直接返回
    if image.startswith("m.daocloud.io/"):
        return image

    # 默认添加 m.daocloud.io 前缀（支持所有镜像）
    return f"m.daocloud.io/{image}"


def run_command(command: list, check: bool = True) -> Tuple[int, str, str]:
    """
    执行 shell 命令

    Args:
        command: 命令列表
        check: 是否检查返回码

    Returns:
        Tuple[int, str, str]: (返回码, 标准输出, 标准错误)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr


def pull_image(image: str) -> Tuple[int, str, str]:
    """
    拉取 Docker 镜像

    Args:
        image: 镜像地址

    Returns:
        Tuple[int, str, str]: (返回码, 标准输出, 标准错误)
    """
    print(f"[INFO] Pulling image: {image}")
    return run_command(["docker", "pull", image], check=True)


def tag_image(source: str, target: str) -> Tuple[int, str, str]:
    """
    为镜像打标签

    Args:
        source: 源镜像
        target: 目标镜像

    Returns:
        Tuple[int, str, str]: (返回码, 标准输出, 标准错误)
    """
    print(f"[INFO] Tagging: {source} -> {target}")
    return run_command(["docker", "tag", source, target], check=True)


def remove_image(image: str) -> Tuple[int, str, str]:
    """
    删除镜像

    Args:
        image: 镜像地址

    Returns:
        Tuple[int, str, str]: (返回码, 标准输出, 标准错误)
    """
    print(f"[INFO] Removing mirror tag: {image}")
    return run_command(["docker", "rmi", image], check=False)


def accelerate_pull(original_image: str) -> bool:
    """
    使用加速源拉取镜像并重命名

    Args:
        original_image: 原始镜像名称

    Returns:
        bool: 是否成功
    """
    try:
        # 1. 标准化镜像名称
        normalized_image = normalize_image_name(original_image)
        print(f"[INFO] Original image: {original_image}")
        print(f"[INFO] Normalized: {normalized_image}")

        # 2. 转换为加速镜像地址
        mirror_image = convert_to_mirror_image(normalized_image)
        if not mirror_image:
            print(f"[ERROR] Unsupported image source '{original_image}'")
            return False

        print(f"[INFO] Mirror image: {mirror_image}")

        # 3. 使用加速源拉取镜像
        returncode, stdout, stderr = pull_image(mirror_image)
        if returncode != 0:
            print(f"[ERROR] Pull failed: {stderr}")
            return False

        print(f"[SUCCESS] Pull completed")

        # 4. 重命名为原始镜像名
        # 如果原始镜像名就是标准化的，使用标准化名称
        target_image = original_image if '/' in original_image else normalized_image

        returncode, stdout, stderr = tag_image(mirror_image, target_image)
        if returncode != 0:
            print(f"[WARNING] Rename warning: {stderr}")
            # 重命名失败不影响结果，镜像已经拉取成功
        else:
            print(f"[SUCCESS] Rename completed")

        # 5. 删除加速镜像标签（如果标签名不同）
        if mirror_image != target_image:
            returncode, stdout, stderr = remove_image(mirror_image)
            if returncode != 0:
                print(f"[WARNING] Cleanup warning: {stderr}")
            else:
                print(f"[SUCCESS] Cleanup completed")

        print(f"\n[SUCCESS] Image '{target_image}' pulled and configured successfully!")
        return True

    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python accelerate_docker_pull.py <镜像名称> [镜像名称2] ...")
        print("\n示例:")
        print("  python accelerate_docker_pull.py nginx:latest")
        print("  python accelerate_docker_pull.py gcr.io/pause:3.1")
        print("  python accelerate_docker_pull.py python:3.9-slim")
        sys.exit(1)

    images = sys.argv[1:]

    print("=" * 60)
    print("[INFO] Docker Image Accelerator")
    print("[INFO] Using DaoCloud mirror for acceleration")
    print("=" * 60)
    print()

    success_count = 0
    failed_count = 0

    for image in images:
        print(f"\n{'=' * 60}")
        if accelerate_pull(image):
            success_count += 1
        else:
            failed_count += 1

    print(f"\n{'=' * 60}")
    print(f"[SUMMARY] Success: {success_count}, Failed: {failed_count}")
    print(f"{'=' * 60}\n")

    sys.exit(0 if failed_count == 0 else 1)


if __name__ == "__main__":
    main()
