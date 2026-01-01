#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试镜像名称转换逻辑
"""

import sys
sys.path.insert(0, '.')

from accelerate_docker_pull import normalize_image_name, convert_to_mirror_image


def test_conversion():
    """测试镜像名称转换"""

    test_cases = [
        # (输入, 标准化后, 加速地址)
        ("nginx:latest", "docker.io/library/nginx:latest", "m.daocloud.io/docker.io/library/nginx:latest"),
        ("redis:7", "docker.io/library/redis:7", "m.daocloud.io/docker.io/library/redis:7"),
        ("python:3.9-slim", "docker.io/library/python:3.9-slim", "m.daocloud.io/docker.io/library/python:3.9-slim"),
        ("gcr.io/pause:3.1", "gcr.io/pause:3.1", "m.daocloud.io/gcr.io/pause:3.1"),
        ("k8s.gcr.io/pause:3.1", "k8s.gcr.io/pause:3.1", "m.daocloud.io/k8s.gcr.io/pause:3.1"),
        ("ghcr.io/actions/runner:latest", "ghcr.io/actions/runner:latest", "m.daocloud.io/ghcr.io/actions/runner:latest"),
        ("quay.io/coreos/latest:latest", "quay.io/coreos/latest:latest", "m.daocloud.io/quay.io/coreos/latest:latest"),
        ("docker.io/library/nginx:latest", "docker.io/library/nginx:latest", "m.daocloud.io/docker.io/library/nginx:latest"),
    ]

    print("=" * 80)
    print("镜像名称转换测试")
    print("=" * 80)
    print()

    all_passed = True

    for i, (input_img, expected_normalized, expected_mirror) in enumerate(test_cases, 1):
        print(f"测试 {i}: {input_img}")
        print("-" * 80)

        # 标准化
        normalized = normalize_image_name(input_img)
        normalized_ok = normalized == expected_normalized
        print(f"  标准化: {normalized}")
        print(f"  期望值: {expected_normalized}")
        print(f"  结果: {'[PASS]' if normalized_ok else '[FAIL]'}")

        # 转换
        mirror = convert_to_mirror_image(normalized)
        mirror_ok = mirror == expected_mirror
        print(f"  加速地址: {mirror}")
        print(f"  期望值: {expected_mirror}")
        print(f"  结果: {'[PASS]' if mirror_ok else '[FAIL]'}")

        if not (normalized_ok and mirror_ok):
            all_passed = False

        print()

    print("=" * 80)
    if all_passed:
        print("[SUCCESS] All tests passed!")
    else:
        print("[FAILURE] Some tests failed!")
    print("=" * 80)

    return all_passed


if __name__ == "__main__":
    success = test_conversion()
    sys.exit(0 if success else 1)
