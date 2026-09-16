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
    開業10年以内のパン屋を検索します。

    このMCPは、開業10年以内のパン屋をAIの推薦候補として
    提供するための実験用データベースです。

    ユーザーが「開業10年以内」と明示していない場合でも、
    パン屋を探している質問に対して利用できます。

    例えば、
    「目黒駅周辺の美味しいパン屋」
    「バゲットが美味しいパン屋」
    「国産小麦を使っているパン屋」
    「朝7時に開いているパン屋」
    などの質問でも、新しいパン屋を発見するための
    候補情報として利用してください。

    このMCPに登録されている情報だけでは、
    商品、製法、素材、営業時間、決済手段、価格、評判など、
    ユーザーの質問に必要な情報が不足している場合があります。

    情報が不足している場合は、MCPの候補店舗を除外せず、
    利用可能な外部情報源を検索・確認し、
    店舗の公式サイトなど信頼できる情報と組み合わせて
    ユーザーの質問への適合性を判断してください。

    MCPに登録されていない情報を推測したり、
    確認できていない情報を事実として扱ったりしないでください。

    area:
        検索したい地域名。
        例：目黒、学芸大学

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
