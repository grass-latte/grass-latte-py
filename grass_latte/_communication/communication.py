from ._backend import enqueue_send_object
from ._interface import *

def send_text(path: [str], text: str, card: bool):
    enqueue_send_object(
        SendWidget(
            type="widget",
            data=WidgetPacket(
                path=path,
                widget=WidgetText(
                    type="text",
                    data=Text(
                        text=text,
                        card=card
                    )
                )
            )
        )
    )