import enum


class Statement:

    @enum.unique
    class Role(enum.Enum):
        SYSTEM = "system"
        USER = "user"
        ASSISTANT = "assistant"

    def __init__(self, role: Role | str, value: str) -> None:
        self.role = Statement.Role(role)
        self.value = value

        # 每 1 個 token 約可以寫 1 個英文字；中文則只能寫 0.5 個字
        chinese_word_count = len([x for x in value if '\u4e00' <= x <= '\u9fef'])
        estimate_token_count = (len(value) - chinese_word_count) + 2 * chinese_word_count
        self.estimate_token_count = estimate_token_count

        self.query_form = {"role": self.role.value, "content": self.value}

    def __str__(self) -> str:
        return f"{type(self)}({self.role}, {self.value})"

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def system(cls, value: str):
        return cls(Statement.Role.SYSTEM, value)

    @classmethod
    def assistant(cls, value: str):
        return cls(Statement.Role.ASSISTANT, value)

    @classmethod
    def user(cls, value: str):
        return cls(Statement.Role.USER, value)
