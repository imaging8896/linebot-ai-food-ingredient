import os

from datetime import datetime

from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, ApiClient
from linebot.v3.webhooks import MessageEvent, TextMessageContent, ImageMessageContent, PostbackEvent, JoinEvent

from . import app_config
from . import app_context
from .ai.openai import OpenAI
from .helper import image as image_helper
from .line import postback
from .line.message import api as line_api
from .line.message.direct_message_only import flex_message_direct_message_only
from .line.message.text import flex_message_text
from .line.message.welcome import flex_message_welcome
from .line.event import EventSourceType


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
    _, source_type, reply_token, _, _ = _parse_linebot_event(linebot_event)

    if source_type != EventSourceType.USER:
        logger.warning("Ignored user message event from not user direct")
        return

    with ApiClient(linebot_configuration) as api_client:
        messages = []
        try:
            line_api.reply_message(api_client, reply_token, messages=[flex_message_welcome()])
        except Exception:
            logger.exception("Failed handling user message text event")
            line_api.reply_message(api_client, reply_token, messages=messages + [flex_message_welcome(with_sorry_message=True)])


@linebot_handler.add(MessageEvent, message=ImageMessageContent)
def handle_linebot_message_image(linebot_event: MessageEvent):
    # Line event
    # {
    #     "type": "message",
    #     "message": :{
    #       "type": "image",
    #       "id": "582877727984714001",
    #       "quoteToken": "xxxx",
    #       "contentProvider": {"type": "line"}
    #     },
    #     "timestamp": 1644116599193,
    user_id, source_type, reply_token, _, _ = _parse_linebot_event(linebot_event)

    if source_type != EventSourceType.USER:
        logger.warning("Ignored user message event from not user direct")
        return

    with ApiClient(linebot_configuration) as api_client:
        messages = []
        try:
            local_image_file_name = f"{user_id}_{datetime.now().isoformat()}.png"
            local_image_file = os.path.join(app_config.IMAGE_FOLDER, local_image_file_name)
            saved_image_url = app_config.IMAGE_URL_PREFIX + "/" + local_image_file_name

            try:
                food_image_bytes = line_api.get_image(api_client, linebot_event.message.id, retry=3)
            except line_api.UnableToFetchImageError:
                messages.append(flex_message_text(text="無法取得圖片，請確認圖片是否有效，或稍後再試試。"))
                raise

            image_helper.remove_images(image_prefix=user_id, remove_folder=app_config.IMAGE_FOLDER)
            
            image_helper.save_image_to_file(food_image_bytes, local_image_file)

            logger.info(f"已收到圖片，圖片網址：{saved_image_url}")

            food_ingredients = OpenAI().retrieve_food_ingredients_from_image_content(food_image_bytes)

            if food_ingredients:
                result = OpenAI().evaluate_food_ingredients(food_ingredients)
                max_message_length = 1000
                for i in range(0, len(result), max_message_length):
                    if i == 4:
                        messages.append(flex_message_text(text=result[i:i+max_message_length] + "\n過多無法顯示..."))
                    else:
                        messages.append(flex_message_text(text=result[i:i+max_message_length]))
            else:
                messages.append(flex_message_text(text="無法辨識圖片中的食物成分，請確認圖片是否有效，或稍後再試試。"))

            line_api.reply_message(api_client, reply_token, messages=messages)
        except Exception:
            logger.exception("Failed handling user message image event")
            line_api.reply_message(api_client, reply_token, messages=messages + [flex_message_welcome(with_sorry_message=True)])


@linebot_handler.add(PostbackEvent)
def handle_linebot_postback(linebot_event: PostbackEvent):
    _parse_linebot_event(linebot_event)

    postback_command, postback_args, postback_kw = postback.parse_postback_data(linebot_event.postback.data)
    logger.info(f"Got postback event: {postback_command=} {postback_args=} {postback_kw=}")
    logger.warning("Ignored postback event")

    # with ApiClient(linebot_configuration) as _:
    #     try:
    #         pass
    #     except Exception:
    #         logger.exception("Failed handling postback event")


@linebot_handler.add(JoinEvent)
def handle_joined(event: JoinEvent):
    _, _, reply_token, _, _ = _parse_linebot_event(event)
    logger.info("Got joined event")

    with ApiClient(linebot_configuration) as api_client:
        try:
            line_api.reply_message(api_client, reply_token, messages=[flex_message_direct_message_only()])
        except Exception:
            logger.exception("Failed handling joined event")


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
    # In Room
    #     "source": {
    #     "type": "room",
    #     "roomId": "Ra8dbf4673c...",
    #     "userId": "U4af4980629..."
    #   }
    # }
    if linebot_event.source is None:
        msg = f"Line event source is None, cannot process the event. {linebot_event=}"
        raise ValueError(msg)
    
    if linebot_event.reply_token is None:
        msg = f"Line event reply_token is None, cannot process the event. {linebot_event=}"
        raise ValueError(msg)

    source_dict = linebot_event.source.to_dict()
    user_id: str = source_dict["userId"]
    source_type = EventSourceType(linebot_event.source.type)
    reply_token: str = linebot_event.reply_token
    group_id: str | None = getattr(linebot_event.source, "group_id", None)
    room_id: str | None = getattr(linebot_event.source, "room_id", None)

    logger.info(f"Got event: {user_id=} {source_type=} {group_id=} {room_id=}")
    return user_id, source_type, reply_token, group_id, room_id


def _parse_user_message_text(linebot_event: MessageEvent):
    message_dict = linebot_event.message.to_dict()
    return str(message_dict["text"]), str(message_dict["quoteToken"])
