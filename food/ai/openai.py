import re

from .model.query import Query
from .model.statement import Statement

from .logging import logger


class OpenAI:

    def __init__(self) -> None:
        import openai

        self.client = openai.OpenAI()

    def evaluate_food_from_image_content(self, image_bytes: bytes | bytearray):
        image_bytes = bytearray(image_bytes)

        non_food_ingredient_reply = "無法辨識圖片中的食物成分"

        query = Query(
            statements=[
                Statement.system(
                    Statement.Content(
                        Statement.Content.Type.TEXT, 
                        "你是一位專業營養師，使用者會上傳『食物成分表的照片』或是『食物的照片』。"
                        "對於『食物成分表的照片』，請協助精準辨識照片中的每一個食物成分，條列以『|||』分隔並以繁體中文回覆，回應範例：'牛奶|||蔗糖|||果糖|||香料'。"
                        "對於『食物的照片』，請協助辨識精準照片中的每一個食物，並根據圖中食物大小精準估計蛋白質(代號P)、碳水(代號C)、脂肪(代號A)和膳食纖維(代號F)，單位都是克數，"
                        "條列以『|||』分隔並以繁體中文回覆，回應範例：'牛肉{P20g,C0.2g,A3.1g,F10g}|||青椒{P5g,C1g,A3g,F0.1g}|||洋蔥{P10.2g,C2g,A3g,F0g}'。"
                        f"若不是以上兩種圖片，請回覆「{non_food_ingredient_reply}」。",
                    )
                ),
                Statement.user(
                    Statement.Content(Statement.Content.Type.IMAGE, image_bytes)
                ),
            ],
        )

        response = self.client.responses.create(
            model="o4-mini", # 貴一些
            # model="gpt-5-mini",
            temperature=1,
            input=query.value,  # type: ignore
        )
        if response.usage:
            logger.info(f"'evaluate_food_from_image_content' total tokens: {response.usage.total_tokens}")

        result = str(response.output_text)
        if non_food_ingredient_reply in result:
            return
        
        results = result.split("|||")

        if "{" in result:
            # 食物照片

            def _parse_ingredient(x: str):
                # {P20g,C0g,A3g,F10g}
                if m := re.match(r"^(.+)\{P([\d|\.]+)g,C([\d|\.]+)g,A([\d|\.]+)g,F([\d|\.]+)g\}$", x):
                    return m.group(1), float(m.group(2)), float(m.group(3)), float(m.group(4)), float(m.group(5))
                raise ValueError(f"Cannot parse ingredient nutrition info from {x}")

            results = [_parse_ingredient(x) for x in results ]
            return {name: (protein, carbs, fat, fiber) for name, protein, carbs, fat, fiber in results}
        return {x: None for x in results}

    def evaluate_food_ingredients(self, food_ingredients: list[str]):
        query = Query(
            statements=[
                Statement.system(
                    Statement.Content(
                        Statement.Content.Type.TEXT, 
                        "輸入食物成分（以『,』分隔），請評估每一個食物成分『俗稱』『描述用途』『是否天然』『是否是添加物』『有健康疑慮的原因』。"
                        "去除並且不分析重複的成分，只輸出可能不健康的成分，不要有其他廢話。"
                    )
                ),
                Statement.user(
                    Statement.Content(Statement.Content.Type.TEXT, ",".join(food_ingredients))
                ),
            ],
        )

        response = self.client.responses.create(
            model="o3-mini",
            temperature=1,
            input=query.value,  # type: ignore
        )
        if response.usage:
            logger.info(f"'evaluate_food_ingredients' total tokens: {response.usage.total_tokens}")

        return str(response.output_text)
