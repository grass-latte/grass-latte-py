import asyncio
from ._backend import enqueue_send_object
from ._interface import *

def send_text(path: [str], text: str, card: bool):
    enqueue_send_object(
        SendElement(
            type="element",
            data=ElementPacket(
                path=path,
                element=ElementText(
                    type="text",
                    data=Text(
                        text=text,
                        card=card
                    )
                )
            )
        )
    )