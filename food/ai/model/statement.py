import enum


class Statement:

    @enum.unique
    class Role(enum.Enum):
        SYSTEM = "system"
        USER = "user"
        ASSISTANT = "assistant"

    class Content:

        @enum.unique
        class Type(enum.Enum):
            TEXT = "input_text"
            IMAGE = "input_image"

        def __init__(self, content_type: Type, value: str | bytearray) -> None:
            self.type = content_type

            if isinstance(value, str):
                self.value = value
            else:
                if content_type != self.Type.IMAGE:
                    raise ValueError(f"Not text content should be image content. Got {content_type}")
                if not isinstance(value, bytearray):
                    raise ValueError(f"Image content value should be bytearray. Got {type(value)=}")

                import base64

                base64_image = base64.b64encode(value).decode("utf-8")
                self.value = f"data:image/jpeg;base64,{base64_image}"

        def __str__(self) -> str:
            return f"{type(self)}({self.type}, {self.value})"

        @property
        def query_form(self):
            return {
                self.Type.TEXT: {"type": self.type.value, "text": self.value},
                self.Type.IMAGE: {"type": self.type.value, "image_url": self.value, "detail": "high"},
            }[self.type]

    def __init__(self, role: Role, content: Content) -> None:
        self.role = role
        self.content = content

        # 每 1 個 token 約可以寫 1 個英文字；中文則只能寫 0.5 個字
        chinese_word_count = len([x for x in content.value if '\u4e00' <= x <= '\u9fef'])
        estimate_token_count = (len(content.value) - chinese_word_count) + 2 * chinese_word_count
        self.estimate_token_count = estimate_token_count

    @property
    def query_form(self):
        return {"role": self.role.value, "content": [self.content.query_form]}

    def __str__(self) -> str:
        return f"{type(self)}({self.role}, {self.content})"

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def system(cls, content: Content):
        return cls(Statement.Role.SYSTEM, content)

    @classmethod
    def assistant(cls, content: Content):
        return cls(Statement.Role.ASSISTANT, content)

    @classmethod
    def user(cls, content: Content):
        return cls(Statement.Role.USER, content)
