#!/usr/bin/env python3
"""
代码审查报告生成辅助工具
自动创建docs目录并保存审查报告
"""

import os
import sys
from datetime import datetime
from pathlib import Path


def get_docs_directory() -> Path:
    """
    获取项目的文档目录

    优先级: docs/ > doc/ > 创建docs/

    Returns:
        Path: 文档目录路径
    """
    project_root = Path.cwd()

    # 1. 检查 docs 目录
    docs_dir = project_root / "docs"
    if docs_dir.exists() and docs_dir.is_dir():
        return docs_dir

    # 2. 检查 doc 目录
    doc_dir = project_root / "doc"
    if doc_dir.exists() and doc_dir.is_dir():
        return doc_dir

    # 3. 创建 docs 目录
    docs_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ 已创建文档目录: {docs_dir}")
    return docs_dir


def generate_report_filename() -> str:
    """
    生成报告文件名(中文格式)

    Returns:
        str: 报告文件名
    """
    timestamp = datetime.now().strftime("%Y年%m月%d日%H时%M分")
    return f"代码审查报告_{timestamp}.md"


def save_report(content: str, custom_name: str = None) -> str:
    """
    保存代码审查报告到docs目录

    Args:
        content: 报告内容
        custom_name: 自定义文件名(可选)

    Returns:
        str: 保存的文件路径
    """
    # 获取docs目录
    docs_dir = get_docs_directory()

    # 生成文件名
    filename = custom_name or generate_report_filename()

    # 确保扩展名是.md
    if not filename.endswith('.md'):
        filename += '.md'

    # 完整路径
    report_path = docs_dir / filename

    # 保存文件
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n✅ 代码审查报告已成功保存!")
        print(f"📁 位置: {report_path}")
        print(f"📊 文件大小: {report_path.stat().st_size} 字节")

        return str(report_path)

    except Exception as e:
        print(f"\n❌ 保存报告失败: {e}")
        sys.exit(1)


def list_existing_reports() -> list:
    """
    列出现有的代码审查报告

    Returns:
        list: 报告文件列表
    """
    docs_dir = get_docs_directory()
    reports = list(docs_dir.glob("代码审查报告_*.md"))
    reports.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return reports


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='代码审查报告生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 查看现有报告列表
  python save_review_report.py --list

  # 从标准输入读取报告内容并保存
  echo "报告内容" | python save_review_report.py

  # 从文件读取报告并保存
  python save_review_report.py --input report.md

  # 使用自定义文件名
  python save_review_report.py --name "我的代码审查报告.md"
        '''
    )

    parser.add_argument(
        '--input',
        '-i',
        help='输入文件路径'
    )

    parser.add_argument(
        '--name',
        '-n',
        help='自定义报告文件名'
    )

    parser.add_argument(
        '--list',
        '-l',
        action='store_true',
        help='列出现有的代码审查报告'
    )

    parser.add_argument(
        '--content',
        '-c',
        help='直接提供报告内容'
    )

    args = parser.parse_args()

    # 列出报告
    if args.list:
        reports = list_existing_reports()
        if reports:
            print(f"\n📋 现有的代码审查报告 (共 {len(reports)} 个):\n")
            for i, report in enumerate(reports, 1):
                mtime = datetime.fromtimestamp(report.stat().st_mtime)
                size = report.stat().st_size
                print(f"{i}. {report.name}")
                print(f"   📅 {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   📊 {size} 字节")
                print()
        else:
            print("\n📋 当前没有代码审查报告\n")
        return

    # 确定报告内容
    content = None

    if args.content:
        content = args.content
    elif args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ 错误: 输入文件不存在: {args.input}", file=sys.stderr)
            sys.exit(1)
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # 从标准输入读取
        print("📝 请输入报告内容 (Ctrl+D 结束输入):")
        try:
            content = sys.stdin.read()
        except KeyboardInterrupt:
            print("\n\n❌ 输入已取消")
            sys.exit(1)

    if not content or content.strip() == "":
        print("❌ 错误: 报告内容为空", file=sys.stderr)
        sys.exit(1)

    # 保存报告
    save_report(content, args.name)


if __name__ == '__main__':
    # 如果没有任何参数,显示帮助信息
    if len(sys.argv) == 1:
        print(__doc__)
        print("\n提示: 使用 --help 查看详细帮助\n")
        sys.exit(0)

    main()
