from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage, ValidateMessageRequest, QuickReply, QuickReplyItem, MessageAction, Message
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent, JoinEvent

from . import app_config
from . import app_context
from .line import postback


logger = app_context.app_logger

linebot_configuration = Configuration(access_token=app_config.LINE_CHANNEL_ACCESS_TOKEN)

linebot_handler = WebhookHandler(app_config.LINE_CHANNEL_SECRET)


@linebot_handler.add(MessageEvent, message=TextMessageContent)
def handle_linebot_message_text(linebot_event: MessageEvent):
    # Line event
    # {
    #     "type": "message",
    #     "message": {
    #         "type": "text",
    #         "id": "15542015634833",
    #         "quoteToken": "xxx",
    #         "text": "123"
    #     },
    #     "timestamp": 1644116599193,

    message_dict = linebot_event.message.to_dict()
    event_message: str = message_dict["text"]
    quote_token: str = message_dict["quoteToken"]

    user_id, source_type, reply_token, group_id, room_id = _parse_linebot_event(linebot_event)


@linebot_handler.add(PostbackEvent)
def handle_linebot_postback(linebot_event: PostbackEvent):
    user_id, source_type, reply_token, _, _ = _parse_linebot_event(linebot_event)
    quote_token = None

    postback_command, postback_args, postback_kw = postback.parse_postback_data(linebot_event.postback.data)


@linebot_handler.add(JoinEvent)
def handle_joined(event: JoinEvent):
    try:
        with ApiClient(linebot_configuration) as api_client:
            logger.info(f"Joined event: {event}")
            user_id, _, reply_token, _, _ = _parse_linebot_event(event)
            quote_token = None

            # messages = [stock_handler.get_welcome_message_for_group()]

            # message_api = MessagingApi(api_client)
            # message_api.validate_reply(ValidateMessageRequest(messages=messages))

            # message_api.reply_message(ReplyMessageRequest(replyToken=reply_token, notificationDisabled=False, messages=messages))
    except Exception:
        logger.exception("APP joined event got exception")
        # message_api.reply_message(ReplyMessageRequest(replyToken=reply_token, notificationDisabled=False, messages=messages))
        raise


def _parse_linebot_event(linebot_event: MessageEvent | PostbackEvent | JoinEvent):
    # User direct
    #     "source": {
    #         "type": "user",
    #         "userId": "U06faf0b1aae47b199905fcaf64b3dfad"
    #     },
    # In group
    #     "source": {
    #         "type": "group",
    #         "groupId": "C2dff2fdac0ce7cce00cef67d0986bbf5",
    #         "userId": "U06faf0b1aae47b199905fcaf64b3dfad"
    #     },
    #     "replyToken": "7a8537d675344ad099e89386732a75d0",
    #     "mode": "active"
    # }
    if linebot_event.source is None:
        msg = f"Line event source is None, cannot process the event. {linebot_event=}"
        raise ValueError(msg)
    
    if linebot_event.reply_token is None:
        msg = f"Line event reply_token is None, cannot process the event. {linebot_event=}"
        raise ValueError(msg)

    source_dict = linebot_event.source.to_dict()
    user_id: str = source_dict["userId"]
    source_type: str = linebot_event.source.type
    reply_token: str = linebot_event.reply_token
    group_id: str | None = getattr(linebot_event.source, "group_id", None)
    room_id: str | None = getattr(linebot_event.source, "room_id", None)

    return user_id, source_type, reply_token, group_id, room_id
