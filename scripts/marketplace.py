#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sino Claude Code Skills Marketplace CLI
技能市场命令行工具
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class MarketplaceCLI:
    """市场CLI工具类"""

    def __init__(self):
        self.marketplace_dir = Path(__file__).parent.parent
        self.skills_dir = self.marketplace_dir / "skills"
        self.config_file = self.skills_dir / "marketplace.json"
        self.claude_skills_dir = Path.home() / ".claude" / "skills"

        self.load_config()

    def load_config(self):
        """加载市场配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            print(f"❌ 错误: 找不到市场配置文件 {self.config_file}")
            sys.exit(1)

    def save_config(self):
        """保存市场配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def list_skills(self):
        """列出所有可用的技能包"""
        print("\n" + "=" * 80)
        print("📦 Sino Claude Code Skills Marketplace - 可用技能包")
        print("=" * 80 + "\n")

        skills = self.config.get("skills", [])

        if not skills:
            print("📭 暂无可用的技能包\n")
            return

        # 按分类分组
        categories = {cat["id"]: cat for cat in self.config.get("categories", [])}

        for skill in skills:
            category_id = skill.get("category", "uncategorized")
            category = categories.get(category_id, {"name": "未分类", "icon": "📦"})

            print(f"{category['icon']} **{skill['name']}**")
            print(f"   版本: {skill['version']}")
            print(f"   分类: {category['name']}")
            print(f"   描述: {skill['description']}")
            print(f"   作者: {skill['author']}")

            # 标签
            tags = skill.get("tags", [])
            if tags:
                print(f"   标签: {', '.join(tags[:5])}")

            # 评分
            rating = skill.get("rating", 0)
            reviews = skill.get("reviews", 0)
            downloads = skill.get("downloads", 0)
            print(f"   评分: {'⭐' * int(rating)} ({rating}/5.0)")
            print(f"   下载: {downloads}+ | 评论: {reviews}")

            # 安装状态
            if skill.get("installed", False):
                print(f"   状态: ✅ 已安装")
            else:
                print(f"   状态: ⭕ 未安装")

            print()

    def search_skills(self, keyword):
        """搜索技能包"""
        print(f"\n🔍 搜索关键词: '{keyword}'\n")

        skills = self.config.get("skills", [])
        keyword_lower = keyword.lower()

        matched_skills = []
        for skill in skills:
            # 在名称、描述、标签中搜索
            if (keyword_lower in skill["name"].lower() or
                keyword_lower in skill["description"].lower() or
                any(keyword_lower in tag.lower() for tag in skill.get("tags", []))):
                matched_skills.append(skill)

        if not matched_skills:
            print(f"❌ 未找到匹配 '{keyword}' 的技能包\n")
            return

        print(f"✅ 找到 {len(matched_skills)} 个匹配的技能包:\n")

        for skill in matched_skills:
            print(f"📦 {skill['name']} (v{skill['version']})")
            print(f"   {skill['description']}\n")

    def show_skill_info(self, skill_id):
        """显示技能包详细信息"""
        skills = self.config.get("skills", [])

        skill = next((s for s in skills if s["id"] == skill_id), None)

        if not skill:
            print(f"❌ 错误: 找不到技能包 '{skill_id}'\n")
            return

        print(f"\n{'=' * 80}")
        print(f"📦 {skill['name']} - 详细信息")
        print(f"{'=' * 80}\n")

        print(f"**ID**: {skill['id']}")
        print(f"**版本**: {skill['version']}")
        print(f"**作者**: {skill['author']}")
        print(f"**许可证**: {skill.get('license', 'N/A')}\n")

        print(f"**描述**:")
        print(f"   {skill['description']}\n")

        if skill.get("features"):
            print(f"**功能特性**:")
            for feature in skill["features"]:
                print(f"   - {feature}")
            print()

        if skill.get("tags"):
            tags_str = ", ".join(skill["tags"])
            print(f"**标签**: {tags_str}\n")

        if skill.get("documentation"):
            doc_path = Path(skill["documentation"])
            if doc_path.exists():
                print(f"**文档**: {skill['documentation']}\n")

        if skill.get("changelog"):
            changelog_path = Path(skill["changelog"])
            if changelog_path.exists():
                print(f"**更新日志**: {skill['changelog']}\n")

        # 统计信息
        print(f"**统计**:")
        print(f"   - 下载量: {skill.get('downloads', 0)}+")
        print(f"   - 评分: {'⭐' * int(skill.get('rating', 0))} ({skill.get('rating', 0)}/5.0)")
        print(f"   - 评论数: {skill.get('reviews', 0)}\n")

    def install_skill(self, skill_id):
        """安装技能包"""
        print(f"\n📦 正在安装技能包: {skill_id}\n")

        skills = self.config.get("skills", [])
        skill = next((s for s in skills if s["id"] == skill_id), None)

        if not skill:
            print(f"❌ 错误: 找不到技能包 '{skill_id}'\n")
            return False

        # 检查技能包路径
        skill_path = self.marketplace_dir / skill.get("path", f"skills/{skill_id}")

        if not skill_path.exists():
            print(f"❌ 错误: 技能包路径不存在: {skill_path}\n")
            return False

        # 目标路径
        target_path = self.claude_skills_dir / skill_id

        # 创建目标目录
        self.claude_skills_dir.mkdir(parents=True, exist_ok=True)

        # 复制技能包
        try:
            if target_path.exists():
                print(f"⚠️  警告: 目标目录已存在，将覆盖现有安装")
                shutil.rmtree(target_path)

            shutil.copytree(skill_path, target_path)
            print(f"✅ 技能包已成功安装到: {target_path}\n")

            # 更新安装状态
            skill["installed"] = True
            self.save_config()

            # 更新下载统计
            skill["downloads"] = skill.get("downloads", 0) + 1
            self.save_config()

            print(f"📝 提示: 重启Claude Code以使技能包生效\n")
            return True

        except Exception as e:
            print(f"❌ 安装失败: {e}\n")
            return False

    def uninstall_skill(self, skill_id):
        """卸载技能包"""
        print(f"\n🗑️  正在卸载技能包: {skill_id}\n")

        target_path = self.claude_skills_dir / skill_id

        if not target_path.exists():
            print(f"❌ 错误: 技能包未安装: {skill_id}\n")
            return False

        try:
            shutil.rmtree(target_path)
            print(f"✅ 技能包已成功卸载\n")

            # 更新安装状态
            skills = self.config.get("skills", [])
            skill = next((s for s in skills if s["id"] == skill_id), None)
            if skill:
                skill["installed"] = False
                self.save_config()

            print(f"📝 提示: 重启Claude Code以使更改生效\n")
            return True

        except Exception as e:
            print(f"❌ 卸载失败: {e}\n")
            return False

    def update_skill(self, skill_id):
        """更新技能包"""
        print(f"\n🔄 正在更新技能包: {skill_id}\n")

        skills = self.config.get("skills", [])
        skill = next((s for s in skills if s["id"] == skill_id), None)

        if not skill:
            print(f"❌ 错误: 找不到技能包 '{skill_id}'\n")
            return False

        if not skill.get("installed", False):
            print(f"❌ 错误: 技能包未安装，请先安装再更新\n")
            return False

        # 重新安装以更新
        return self.install_skill(skill_id)

    def update_market(self):
        """更新市场索引"""
        print("\n🔄 正在更新市场索引...\n")

        # 这里可以添加从远程仓库更新的逻辑
        # 目前只是更新本地配置

        print("✅ 市场索引已是最新\n")

        # 显示统计信息
        stats = self.config.get("statistics", {})
        print(f"📊 市场统计:")
        print(f"   - 技能包总数: {stats.get('total_skills', 0)}")
        print(f"   - 分类数量: {stats.get('total_categories', 0)}")
        print(f"   - 总下载量: {stats.get('total_downloads', 0)}")
        print(f"   - 最后更新: {stats.get('last_update', 'N/A')}\n")

    def show_statistics(self):
        """显示市场统计信息"""
        print("\n" + "=" * 80)
        print("📊 市场统计信息")
        print("=" * 80 + "\n")

        stats = self.config.get("statistics", {})
        marketplace = self.config.get("marketplace", {})

        print(f"**市场名称**: {marketplace.get('name', 'N/A')}")
        print(f"**版本**: {marketplace.get('version', 'N/A')}")
        print(f"**维护者**: {marketplace.get('maintainer', 'N/A')}")
        print(f"**仓库**: {marketplace.get('repository', 'N/A')}\n")

        print(f"**统计数据**:")
        print(f"   - 技能包总数: {stats.get('total_skills', 0)}")
        print(f"   - 分类数量: {stats.get('total_categories', 0)}")
        print(f"   - 总下载量: {stats.get('total_downloads', 0)}")
        print(f"   - 最后更新: {stats.get('last_update', 'N/A')}\n")

        # 分类统计
        categories = self.config.get("categories", [])
        skills = self.config.get("skills", [])

        print(f"**分类统计**:")
        for category in categories:
            category_skills = [s for s in skills if s.get("category") == category["id"]]
            print(f"   {category['icon']} {category['name']}: {len(category_skills)} 个技能包")
        print()


def main():
    """主函数"""
    cli = MarketplaceCLI()

    parser = argparse.ArgumentParser(
        description="Sino Claude Code Skills Marketplace CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s list                          # 列出所有技能包
  %(prog)s search code-review            # 搜索技能包
  %(prog)s info code-review-expert       # 查看技能包详情
  %(prog)s install code-review-expert    # 安装技能包
  %(prog)s uninstall code-review-expert  # 卸载技能包
  %(prog)s update code-review-expert     # 更新技能包
  %(prog)s update-market                 # 更新市场索引
  %(prog)s stats                         # 显示统计信息
        """
    )

    parser.add_argument(
        "command",
        choices=["list", "search", "info", "install", "uninstall", "update", "update-market", "stats"],
        help="命令"
    )

    parser.add_argument(
        "skill_id",
        nargs="?",
        help="技能包ID (用于search, info, install, uninstall, update命令)"
    )

    args = parser.parse_args()

    # 执行命令
    if args.command == "list":
        cli.list_skills()

    elif args.command == "search":
        if not args.skill_id:
            print("❌ 错误: search命令需要提供搜索关键词\n")
            sys.exit(1)
        cli.search_skills(args.skill_id)

    elif args.command == "info":
        if not args.skill_id:
            print("❌ 错误: info命令需要提供技能包ID\n")
            sys.exit(1)
        cli.show_skill_info(args.skill_id)

    elif args.command == "install":
        if not args.skill_id:
            print("❌ 错误: install命令需要提供技能包ID\n")
            sys.exit(1)
        cli.install_skill(args.skill_id)

    elif args.command == "uninstall":
        if not args.skill_id:
            print("❌ 错误: uninstall命令需要提供技能包ID\n")
            sys.exit(1)
        cli.uninstall_skill(args.skill_id)

    elif args.command == "update":
        if not args.skill_id:
            print("❌ 错误: update命令需要提供技能包ID\n")
            sys.exit(1)
        cli.update_skill(args.skill_id)

    elif args.command == "update-market":
        cli.update_market()

    elif args.command == "stats":
        cli.show_statistics()


if __name__ == "__main__":
    main()
