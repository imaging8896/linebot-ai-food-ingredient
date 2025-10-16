from linebot.v3.messaging import TextMessage

from .component.quick_reply import quick_reply_general


def flex_message_texts(text: str, quote_token: str | None = None) -> list[TextMessage]:
    max_message_length = 1000
    max_message_body_count = 5
    messages = []
    for i in range(0, len(text), max_message_length):
        if i == max_message_body_count - 1:
            messages.append(
                TextMessage(
                    text=text[i:i+max_message_length] + "\n過多無法顯示...", 
                    quoteToken=quote_token, 
                    quickReply=quick_reply_general(),
                )
            )
        else:
            messages.append(
                TextMessage(
                    text=text[i:i+max_message_length],
                    quoteToken=quote_token,
                    quickReply=quick_reply_general(),
                )
            )

    return messages
