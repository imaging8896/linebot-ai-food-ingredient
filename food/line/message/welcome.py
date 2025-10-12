from linebot.v3.messaging import FlexMessage, FlexBubble, FlexBox, FlexText, FlexSeparator

from .component.quick_reply import quick_reply_general, OPEN_CAMERA_TEXT, OPEN_CAMERA_ROLL_TEXT
from ..constant import LINE_BOT_NAME


def flex_message_welcome(with_sorry_message: bool = False) -> FlexMessage:
    return FlexMessage(
        altText=f"歡迎使用『{LINE_BOT_NAME}』", # Text show outside
        contents=FlexBubble(
            size="giga",
            header=FlexBox(
                layout="vertical",
                contents=[
                    FlexText(weight="bold", size="md", wrap=True, text=f"歡迎使用『{LINE_BOT_NAME}』"),  # type: ignore
                    FlexSeparator(margin="lg"),
                ] if not with_sorry_message else [
                    FlexText(weight="bold", size="md", wrap=True, text=f"歡迎使用『{LINE_BOT_NAME}』"),  # type: ignore
                    FlexText(size="sm", wrap=True, color="#FF0000", text="目前服務不穩定，請見諒。"),  # type: ignore
                    FlexSeparator(margin="lg"),
                ]
            ),  # type: ignore
            body=FlexBox(
                layout="vertical",
                contents=[
                    FlexText(text=f"1.點選『{OPEN_CAMERA_TEXT}』拍下食物成分。", wrap=True),  # type: ignore
                    FlexText(text=f"2.點選『{OPEN_CAMERA_ROLL_TEXT}』打開相簿，選擇食物成分照片。", wrap=True),  # type: ignore
                ]
            )  # type: ignore
        ),
        quickReply=quick_reply_general(),
    )
