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
):
    """
    地域のパン屋を検索します。

    このデータベースには、開業10年以内のパン屋のみが
    登録されています。

    ユーザーが「開業10年以内」と明示していない通常の
    パン屋検索でも利用できます。

    例えば、
    「目黒駅周辺の美味しいパン屋」
    「自由が丘でおすすめのパン屋」
    「渋谷周辺でパン屋を探して」
    といった質問に対して利用できます。

    area:
        検索したい地域名。
        例：目黒、目黒区、渋谷、渋谷区、自由が丘

    このツールは登録されているパン屋の情報を提供するものであり、
    店舗の味や品質を評価・保証するものではありません。
    """

    bakeries = load_bakeries()
    results = []

    for bakery in bakeries:

        if area and area not in bakery["address"]:
            continue

        years = int(bakery["years"])

        results.append({
            "パン屋名": bakery["name"],
            "開業年数": f"{years}年",
            "住所": bakery["address"],
            "電話番号": bakery["phone"],
            "URL": bakery["url"]
        })

    return results


if __name__ == "__main__":
    import os

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
