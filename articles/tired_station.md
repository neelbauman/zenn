---
title: "beautyspot2.3.1のリリース"
emoji: "😺"
type: "tech"
topics: [Python, beautyspot]
published: false
---

# beautyspot v2.3.1 をリリースしました

- [github](https://github.com/neelbauman/beautyspot)
- [公式ドキュメント](https://neelbauman.github.io/beautyspot/)

## やったこと

- Spotの引数による、default設定のバグ解消
- input_key_genからkeygenへの変更（後方互換あり）
- テストのリファクタリング


# 使用例

## インストール方法

pipを使用している場合
```
pip install beautyspot[dashboard]
```

uv を使用している場合
```
uv add beautyspot
```

## 使用例

以下のコードを単に繰り返し実行すると、リクエストをスキップしてキャッシュを利用する。

引数nを変えたり、default_versionを変えたり、version引数を与えたりしたらキャッシュヒットしないので、再計算する。

```
from openai import OpenAI
from pydantic import BaseModel
from beautyspot import Spot, KeyGen


# 初期化
spot = Spot("myproject", default_version="v0.1.0")


# === データ構造定義 ===

class User(BaseModel):
    first_name: str
    last_name: str
    email: str

@spot.register(
    code=10,
    encoder=lambda x: x.model_dump(),
    decoder=lambda x: UserList.model_validate(x),
)
class UserList(BaseModel):
    users: list[User]


# === 関数定義時にマーカーをつける === 

@spot.mark(keygen=KeyGen.map(
    client=KeyGen.IGNORE,
))
def get_test_users(client: OpenAI, n: int) -> UserList:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a test data generator."},
            {"role": "user", "content": f"Generate {n} realistic sample users."}
        ],
        response_format=UserList,
    )

    user_list_obj = completion.choices[0].message.parsed
    if user_list_obj is None:
        raise ValueError("response is None")
    return user_list_obj


def main():
    client = OpenAI()

    user_list_obj = get_test_users(client, 6)

    print(f"--- Generated {len(user_list_obj.users)} Users ---")
    
    for user in user_list_obj.users:
        print(f"Name: {user.first_name} {user.last_name} | Email: {user.email}")

if __name__ == "__main__":
    main()
```


## Dashboardを確認

一通り試してみたら、

```
uv run dashboard ui .beautyspot/myproject.db
```

でダッシュボードが起動する。


