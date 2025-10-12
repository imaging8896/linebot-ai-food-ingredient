from linebot.v3.messaging import ApiClient, MessagingApi, MessagingApiBlob, ReplyMessageRequest, ValidateMessageRequest, Message

from ..logging import logger


class UnableToFetchImageError(Exception):
    pass


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

def get_image(api_client: ApiClient, image_id: str, retry: int = 1):
    message_api = MessagingApiBlob(api_client)
    for _ in range(retry + 1):
        try:
            return message_api.get_message_content(image_id, _request_timeout=(5, 60))
        except Exception:
            logger.warning(f"Failed to get image content for image_id={image_id}, retrying...", exc_info=True)
    raise UnableToFetchImageError(f"Failed to get image content for image_id={image_id} after {retry} retries")
