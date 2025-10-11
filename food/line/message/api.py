from linebot.v3.messaging import ApiClient, MessagingApi, ReplyMessageRequest, ValidateMessageRequest, Message


def reply_message(api_client: ApiClient, reply_token: str, messages: list[Message], notification_enabled: bool = True):
    message_api = MessagingApi(api_client)
    message_api.validate_reply(ValidateMessageRequest(messages=messages))

    message_api.reply_message(
        ReplyMessageRequest(
            replyToken=reply_token,
            notificationDisabled=not notification_enabled,
            messages=messages,
        )
    )
