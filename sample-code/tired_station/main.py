from openai import OpenAI
from pydantic import BaseModel
from beautyspot import Spot, KeyGen

spot = Spot("myproject", default_version="v0.1.1")


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

