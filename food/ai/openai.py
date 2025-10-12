from .model.query import Query
from .model.statement import Statement

from .logging import logger


class OpenAI:

    def __init__(self) -> None:
        import openai

        self.client = openai.OpenAI()

    def retrieve_food_ingredients_from_image_content(self, image_bytes: bytes | bytearray):
        image_bytes = bytearray(image_bytes)

        non_food_ingredient_reply = "無法辨識圖片中的食物成分"

        query = Query(
            statements=[
                Statement.system(
                    Statement.Content(
                        Statement.Content.Type.TEXT, 
                        "使用者會上傳食物成分圖片，請協助辨識圖片中的每一個食物成分，條列以『|||』分隔並以繁體中文回覆。"
                        "回應範例：牛奶|||蔗糖|||果糖|||香料"
                        f"若不是食物成分圖片，請回覆「{non_food_ingredient_reply}」。",
                    )
                ),
                Statement.user(
                    Statement.Content(Statement.Content.Type.IMAGE, image_bytes)
                ),
            ],
        )

        response = self.client.responses.create(
            # model="o4-mini", # 貴一些
            model="gpt-5-mini", # 目前只有 o4-mini 支援圖片辨識
            temperature=1,
            input=query.value,  # type: ignore
        )
        if response.usage:
            logger.info(f"'retrieve_food_ingredients_from_image_content' total tokens: {response.usage.total_tokens}")

        result = str(response.output_text)
        if non_food_ingredient_reply not in result:
            return result.split("|||")

    def evaluate_food_ingredients(self, food_ingredients: list[str]):
        query = Query(
            statements=[
                Statement.system(
                    Statement.Content(
                        Statement.Content.Type.TEXT, 
                        "輸入食物成分（以『,』分隔），請評估每一個食物成分『描述用途(50字以內)』『是否天然』『是否是添加物』『是否有健康疑慮』。"
                        "只輸出分析結果，不要有其他廢話。"
                    )
                ),
                Statement.user(
                    Statement.Content(Statement.Content.Type.TEXT, ",".join(food_ingredients))
                ),
            ],
        )

        response = self.client.responses.create(
            model="o3-mini", # 貴一些
            temperature=1,
            input=query.value,  # type: ignore
        )
        if response.usage:
            logger.info(f"'evaluate_food_ingredients' total tokens: {response.usage.total_tokens}")

        return str(response.output_text)
