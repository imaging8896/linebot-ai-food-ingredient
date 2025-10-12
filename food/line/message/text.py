from linebot.v3.messaging import TextMessage

from .component.quick_reply import quick_reply_general


def flex_message_text(text: str, quote_token: str | None = None) -> TextMessage:
    return TextMessage(
        text=text,
        quoteToken=quote_token,
        quickReply=quick_reply_general(),
    )
