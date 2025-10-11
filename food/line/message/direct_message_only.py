from linebot.v3.messaging import FlexMessage, FlexBubble, FlexBox, FlexText, FlexSeparator


def flex_message_direct_message_only() -> FlexMessage:
    return FlexMessage(
        altText="請直接訊息我來獲得服務", # Text show outside
        contents=FlexBubble(
            size="giga",
            header=FlexBox(
                layout="vertical",
                contents=[
                    FlexText(weight="bold", size="md", wrap=True, text="請直接訊息我來獲得服務"),  # type: ignore
                    FlexSeparator(margin="lg"),
                ]
            ),  # type: ignore
            body=FlexBox(
                layout="vertical",
                contents=[
                    FlexText(text=f"需要AI幫你分析食物成分，請點我的頭像，直接送訊息給我。", wrap=True),  # type: ignore
                ]
            )  # type: ignore
        ),
    )
