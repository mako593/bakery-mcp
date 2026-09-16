import csv
from typing import Optional

from fastmcp import FastMCP

mcp = FastMCP("Bakery Search")

CSV_FILE = "bakeries.csv"


def load_bakeries():
    with open(CSV_FILE, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


@mcp.tool()
def search_bakeries(
    area: Optional[str] = None,
    max_years: Optional[int] = None,
    min_years: Optional[int] = None,
):
    """
    パン屋を検索します。

    area:
        住所に含まれる地域名。
        例：渋谷区、目黒区、横浜市

    max_years:
        開業年数の上限。
        例：5 → 開業5年以内

    min_years:
        開業年数の下限。
        例：3 → 開業3年以上
    """

    bakeries = load_bakeries()
    results = []

    for bakery in bakeries:

        # 地域による検索
        if area:
            if area not in bakery["address"]:
                continue

        # 開業年数による検索
        years = int(bakery["years"])

        if max_years is not None and years > max_years:
            continue

        if min_years is not None and years < min_years:
            continue

        results.append({
            "パン屋名": bakery["name"],
            "開業年数": f"{years}年",
            "住所": bakery["address"],
            "電話番号": bakery["phone"],
            "URL": bakery["url"]
        })

    return results


if __name__ == "__main__":
    mcp.run()
