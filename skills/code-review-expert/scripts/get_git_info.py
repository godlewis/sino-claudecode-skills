#!/usr/bin/env python3
"""
Git信息提取工具
用于代码审查时提取git仓库的变更信息、提交者信息等
"""

import subprocess
import json
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Any


def run_git_command(command: List[str]) -> str:
    """执行git命令并返回输出"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"错误: 执行git命令失败: {' '.join(command)}", file=sys.stderr)
        print(f"错误信息: {e.stderr}", file=sys.stderr)
        return ""
    except FileNotFoundError:
        print("错误: 未找到git命令,请确保git已安装", file=sys.stderr)
        return ""


def is_git_repository() -> bool:
    """检查是否在git仓库中"""
    result = run_git_command(["git", "rev-parse", "--is-inside-work-tree"])
    return result == "true"


def get_current_branch() -> str:
    """获取当前分支名"""
    return run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])


def get_remote_url() -> str:
    """获取远程仓库URL"""
    return run_git_command(["git", "config", "--get", "remote.origin.url"])


def get_changed_files(commit_range: str = None) -> List[Dict[str, Any]]:
    """获取变更的文件列表"""
    if commit_range:
        command = ["git", "diff", "--name-status", commit_range]
    else:
        # 获取未暂存的变更
        command = ["git", "status", "--porcelain"]

    output = run_git_command(command)
    if not output:
        return []

    files = []
    for line in output.split('\n'):
        if not line:
            continue

        # git status --porcelain格式: XY filename
        if len(line) >= 3:
            status = line[:2]
            filename = line[3:]
            files.append({
                'filename': filename,
                'status': status,
                'status_description': get_file_status_description(status)
            })

    return files


def get_file_status_description(status: str) -> str:
    """将文件状态代码转换为可读描述"""
    status_map = {
        'M': '已修改',
        'A': '新增',
        'D': '已删除',
        'R': '重命名',
        'C': '复制',
        '??': '未跟踪',
        'MM': '已修改(暂存区和工作区)',
        'AM': '新增后修改',
        'RM': '重命名后修改'
    }

    # 简化状态表示
    simplified_status = status.replace(' ', '').strip()
    if simplified_status in status_map:
        return status_map[simplified_status]

    # 暂存区状态 X, 工作区状态 Y
    if len(simplified_status) == 2:
        index_status = simplified_status[0]
        worktree_status = simplified_status[1]
        return f"暂存区:{index_status}, 工作区:{worktree_status}"

    return status


def get_diff(commit_range: str = None, file_path: str = None) -> str:
    """获取代码差异"""
    command = ["git", "diff"]

    if commit_range:
        command.append(commit_range)
    else:
        # 包含已暂存和未暂存的变更
        command.append("HEAD")

    if file_path:
        command.append("--")
        command.append(file_path)

    return run_git_command(command)


def get_last_commit_info() -> Dict[str, Any]:
    """获取最后一次提交信息"""
    # 获取提交哈希
    commit_hash = run_git_command(["git", "rev-parse", "HEAD"])

    # 获取作者信息
    author_name = run_git_command(["git", "log", "-1", "--pretty=%an"])
    author_email = run_git_command(["git", "log", "-1", "--pretty=%ae"])

    # 获取提交者信息(可能与作者不同)
    committer_name = run_git_command(["git", "log", "-1", "--pretty=%cn"])
    committer_email = run_git_command(["git", "log", "-1", "--pretty=%ce"])

    # 获取提交日期
    commit_date = run_git_command(["git", "log", "-1", "--pretty=%ci"])
    commit_date_timestamp = run_git_command(["git", "log", "-1", "--pretty=%ct"])

    # 获取提交消息
    commit_message = run_git_command(["git", "log", "-1", "--pretty=%B"])

    return {
        'hash': commit_hash,
        'short_hash': run_git_command(["git", "rev-parse", "--short", "HEAD"]),
        'author': {
            'name': author_name,
            'email': author_email
        },
        'committer': {
            'name': committer_name,
            'email': committer_email
        },
        'date': commit_date,
        'timestamp': int(commit_date_timestamp) if commit_date_timestamp else None,
        'message': commit_message.strip(),
        'message_summary': run_git_command(["git", "log", "-1", "--pretty=%s"])
    }


def get_commit_history(limit: int = 10) -> List[Dict[str, Any]]:
    """获取提交历史"""
    output = run_git_command([
        "git", "log",
        f"-{limit}",
        "--pretty=format:%H|%an|%ae|%cn|%ce|%ci|%s"
    ])

    if not output:
        return []

    commits = []
    for line in output.split('\n'):
        if not line:
            continue

        parts = line.split('|')
        if len(parts) >= 7:
            commits.append({
                'hash': parts[0],
                'short_hash': parts[0][:7],
                'author_name': parts[1],
                'author_email': parts[2],
                'committer_name': parts[3],
                'committer_email': parts[4],
                'date': parts[5],
                'message': parts[6]
            })

    return commits


def get_statistics(commit_range: str = None) -> Dict[str, Any]:
    """获取代码统计信息"""
    command = ["git", "diff", "--stat"]

    if commit_range:
        command.append(commit_range)
    else:
        command.append("HEAD")

    output = run_git_command(command)
    if not output:
        return {
            'files_changed': 0,
            'insertions': 0,
            'deletions': 0
        }

    # 解析最后一行统计信息
    # 格式: " X files changed, Y insertions(+), Z deletions(-)"
    lines = output.split('\n')
    summary_line = lines[-1] if lines else ""

    stats = {
        'files_changed': 0,
        'insertions': 0,
        'deletions': 0,
        'details': []
    }

    # 解析详细统计
    for line in lines:
        if '|' in line and '(' in line:
            # 格式: "path/to/file | X + Y -"
            parts = line.split('|')
            if len(parts) >= 2:
                filename = parts[0].strip()
                changes = parts[1]
                stats['details'].append({
                    'filename': filename,
                    'changes': changes.strip()
                })

    # 解析汇总行
    import re
    match = re.search(r'(\d+) file', summary_line)
    if match:
        stats['files_changed'] = int(match.group(1))

    match = re.search(r'(\d+) insertion', summary_line)
    if match:
        stats['insertions'] = int(match.group(1))

    match = re.search(r'(\d+) deletion', summary_line)
    if match:
        stats['deletions'] = int(match.group(1))

    return stats


def get_git_info(commit_range: str = None, include_diff: bool = True) -> Dict[str, Any]:
    """获取完整的git信息"""
    if not is_git_repository():
        return {
            'error': '当前目录不是git仓库',
            'is_git_repo': False
        }

    info = {
        'is_git_repo': True,
        'branch': get_current_branch(),
        'remote_url': get_remote_url(),
        'last_commit': get_last_commit_info(),
        'changed_files': get_changed_files(commit_range),
        'statistics': get_statistics(commit_range),
        'collected_at': datetime.now().isoformat()
    }

    if include_diff:
        info['diff'] = get_diff(commit_range)

    return info


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='提取git仓库信息用于代码审查',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 获取当前状态信息
  python get_git_info.py

  # 获取指定提交范围的信息
  python get_git_info.py --commit-range HEAD~5..HEAD

  # 获取特定分支的信息
  python get_git_info.py --branch feature/user-auth

  # 仅获取文件变更,不包括diff
  python get_git_info.py --no-diff

  # 输出格式化为JSON
  python get_git_info.py --format json
        '''
    )

    parser.add_argument(
        '--commit-range',
        help='git提交范围,如HEAD~5..HEAD'
    )

    parser.add_argument(
        '--branch',
        help='指定分支名'
    )

    parser.add_argument(
        '--no-diff',
        action='store_true',
        help='不包含代码差异(diff)'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='输出格式(默认: text)'
    )

    parser.add_argument(
        '--output',
        help='输出到文件'
    )

    args = parser.parse_args()

    # 如果指定了分支,先切换或获取该分支信息
    commit_range = args.commit_range
    if args.branch:
        # 可以在这里添加分支切换逻辑
        # 为安全起见,仅获取分支信息
        pass

    # 获取git信息
    info = get_git_info(commit_range, not args.no_diff)

    # 格式化输出
    if args.format == 'json':
        output = json.dumps(info, indent=2, ensure_ascii=False)
    else:
        # 文本格式输出
        output = format_git_info_text(info)

    # 输出到文件或控制台
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Git信息已保存到: {args.output}")
    else:
        print(output)


def format_git_info_text(info: Dict[str, Any]) -> str:
    """格式化git信息为文本"""
    if not info.get('is_git_repo'):
        return "错误: 当前目录不是git仓库"

    output = []
    output.append("=" * 80)
    output.append("Git 仓库信息")
    output.append("=" * 80)
    output.append("")

    # 基本信息
    output.append("【基本信息】")
    output.append(f"分支: {info['branch']}")
    output.append(f"远程仓库: {info['remote_url'] or '未配置'}")
    output.append("")

    # 最后一次提交信息
    if info.get('last_commit'):
        commit = info['last_commit']
        output.append("【最后一次提交】")
        output.append(f"提交哈希: {commit.get('short_hash', 'N/A')}")
        output.append(f"提交时间: {commit.get('date', 'N/A')}")
        output.append(f"作者: {commit['author']['name']} <{commit['author']['email']}>")
        output.append(f"提交者: {commit['committer']['name']} <{commit['committer']['email']}>")
        output.append(f"提交消息:")
        for line in commit['message'].split('\n'):
            output.append(f"  {line}")
        output.append("")

    # 变更文件
    if info.get('changed_files'):
        output.append("【变更文件列表】")
        for file_info in info['changed_files']:
            status_desc = file_info.get('status_description', file_info['status'])
            output.append(f"  [{file_info['status']}] {file_info['filename']} - {status_desc}")
        output.append("")

    # 统计信息
    if info.get('statistics'):
        stats = info['statistics']
        output.append("【代码统计】")
        output.append(f"  变更文件数: {stats['files_changed']}")
        output.append(f"  新增行数: {stats['insertions']}")
        output.append(f"  删除行数: {stats['deletions']}")
        output.append("")

    # 代码差异(如果有)
    if info.get('diff'):
        output.append("【代码差异】")
        output.append("-" * 80)
        diff_lines = info['diff'].split('\n')
        # 限制显示行数,避免输出过长
        max_lines = 500
        if len(diff_lines) > max_lines:
            output.extend(diff_lines[:max_lines])
            output.append(f"\n... (省略 {len(diff_lines) - max_lines} 行,使用 --format json 查看完整内容)")
        else:
            output.extend(diff_lines)
        output.append("-" * 80)

    return "\n".join(output)


if __name__ == '__main__':
    main()
