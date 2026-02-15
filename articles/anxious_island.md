---
title: "beautyspot v2.4.1 のリリース"
emoji: "😺"
type: "tech"
topics: [Python, beautyspot]
published: true
---

# beautyspot v2.4.1 をリリースしました

- [github](https://github.com/neelbauman/beautyspot)
- [公式ドキュメント](https://neelbauman.github.io/beautyspot/)

## やったこと

1. タスク単位でのシリアライザ上書き機能 (Per-Task Serializer Override)
これが今回の目玉機能と言えます。
これまで beautyspot は安全性重視で msgpack を標準としていましたが、EDA（探索的データ分析）などの用途で柔軟性が欲しいという要望に応え、タスクごとに pickle など任意のシリアライザを指定できるようになりました。

また、カスタムシリアライザをmarkやcached_runに直接渡せるようになったことで、カスタム型への対応も、シリアライザのカスタムで対応することができるようになりました。

2. テスト戦略の拡張 (Integration Tests)
ユニットテストだけでなく、パイプライン全体やCLIの挙動を検証するための「高レベル結合テスト（Integration Tests）」が導入されました。


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

```python
from openai import OpenAI
from pydantic import BaseModel
from beautyspot import Spot, KeyGen, serializer
from beautyspot.serializer import MsgpackSerializer
import pickle

spot = Spot("myproject", default_version="v0.1.0")

# === データ定義 ===

class User(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserList(BaseModel):
    users: list[User]


# === カスタムシリアライザ作成 ===

serializer = MsgpackSerializer()
serializer.register(
    code=10,
    type_=UserList,
    encoder=lambda x: x.model_dump(),
    decoder=lambda x: UserList.model_validate(x),
)


# === markにカスタムシリアライザを渡す ===

@spot.mark(
    keygen=KeyGen.map(
        client=KeyGen.IGNORE,
    ),
    serializer=serializer,
)
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


