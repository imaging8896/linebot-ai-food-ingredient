from linebot.v3.messaging import QuickReply, QuickReplyItem, CameraAction, CameraRollAction

from .constant import OPEN_CAMERA_TEXT, OPEN_CAMERA_ROLL_TEXT


def quick_reply_general() -> QuickReply:
    return QuickReply(
        items=[
            QuickReplyItem(action=CameraAction(label=OPEN_CAMERA_TEXT)),  # type: ignore
            QuickReplyItem(action=CameraRollAction(label=OPEN_CAMERA_ROLL_TEXT)),  # type: ignore
        ]
    )
