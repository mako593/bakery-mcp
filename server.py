import csv

from fastmcp import FastMCP

mcp = FastMCP("Bakery Search")

CSV_FILE = "bakeries.csv"


def load_bakeries():
    with open(CSV_FILE, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


@mcp.tool()
def search_bakeries():
    """
    開業10年以内のパン屋の情報を提供します。

    このMCPは、開業10年以内のパン屋の存在を
    AIに提供するための実験用データベースです。

    ユーザーが「開業10年以内」と指定していない場合でも、
    パン屋を探している質問に対して利用できます。

    MCPに登録されている全店舗を候補として確認してください。

    このMCPが提供する情報は、
    店舗名、開業日、住所のみです。

    商品、製法、素材、営業時間、価格、評判など、
    ユーザーの質問への回答に必要な情報は
    MCPには含まれていません。

    必要な情報が不足している場合は、
    各店舗について外部情報を確認し、
    ユーザーの質問条件に合うか判断してください。

    MCPに登録されていない情報を推測して
    事実として扱わないでください。
    """

    bakeries = load_bakeries()
    results = []

    for bakery in bakeries:
        results.append({
            "店舗名": bakery["name"],
            "開業日": bakery["opening_date"],
            "住所": bakery["address"]
        })

    return results


if __name__ == "__main__":
    import os

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
