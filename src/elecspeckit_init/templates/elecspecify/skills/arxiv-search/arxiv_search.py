#!/usr/bin/env python3
"""
arXiv 论文搜索脚本

使用 arXiv API 搜索学术论文
"""

import argparse
import sys

try:
    import arxiv
except ImportError:
    print("错误: 未安装 arxiv 库", file=sys.stderr)
    print("请运行: pip install arxiv", file=sys.stderr)
    sys.exit(1)

from datetime import datetime


def search_arxiv(query, max_results=10, start_date=None, end_date=None):
    """
    搜索 arXiv 论文

    Args:
        query: 搜索关键词
        max_results: 最大结果数量
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)

    Returns:
        论文列表
    """
    # 构建搜索查询
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    results = []
    for paper in search.results():
        # 时间过滤
        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            if paper.published.replace(tzinfo=None) < start:
                continue

        if end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            if paper.published.replace(tzinfo=None) > end:
                continue

        results.append(
            {
                "title": paper.title,
                "authors": [author.name for author in paper.authors],
                "published": paper.published.strftime("%Y-%m-%d"),
                "summary": paper.summary[:300] + "..."
                if len(paper.summary) > 300
                else paper.summary,
                "url": paper.entry_id,
                "pdf_url": paper.pdf_url,
            }
        )

    return results


def main():
    parser = argparse.ArgumentParser(description="搜索 arXiv 论文")
    parser.add_argument("--query", required=True, help="搜索关键词")
    parser.add_argument("--max-results", type=int, default=10, help="最大结果数量")
    parser.add_argument("--start-date", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")

    args = parser.parse_args()

    try:
        results = search_arxiv(
            query=args.query,
            max_results=args.max_results,
            start_date=args.start_date,
            end_date=args.end_date,
        )

        if args.json:
            import json

            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            if not results:
                print("未找到匹配的论文")
                sys.exit(0)

            for i, paper in enumerate(results, 1):
                print(f"\n{i}. {paper['title']}")
                print(f"   作者: {', '.join(paper['authors'][:3])}")
                if len(paper['authors']) > 3:
                    print(f"         等 {len(paper['authors'])} 人")
                print(f"   发表: {paper['published']}")
                print(f"   摘要: {paper['summary']}")
                print(f"   链接: {paper['url']}")
                print(f"   PDF:  {paper['pdf_url']}")

    except Exception as e:
        print(f"搜索失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
