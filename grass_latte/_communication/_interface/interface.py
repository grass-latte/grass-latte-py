from typing import List, Optional, Union, Literal, Annotated
from pydantic import BaseModel, Field


class Node(BaseModel):
    card: bool

class Text(BaseModel):
    text: str
    card: bool

class Progress(BaseModel):
    text: Optional[str]
    progress: float
    card: bool

class Button(BaseModel):
    text: str
    card: bool


class WidgetNode(BaseModel):
    type: Literal["node"]
    data: Node

class WidgetText(BaseModel):
    type: Literal["text"]
    data: Text

class WidgetProgress(BaseModel):
    type: Literal["progress"]
    data: Progress

class WidgetButton(BaseModel):
    type: Literal["button"]
    data: Button

Widget = Annotated[
    Union[WidgetNode, WidgetText, WidgetProgress, WidgetButton],
    Field(discriminator='type')
]

class WidgetPacket(BaseModel):
    path: List[str]
    widget: Widget

class DeletePacket(BaseModel):
    path: List[str]

class HandledPacket(BaseModel):
    path: List[str]


class SendWidget(BaseModel):
    type: Literal["widget"]
    data: WidgetPacket

class SendDelete(BaseModel):
    type: Literal["delete"]
    data: DeletePacket

class SendClear(BaseModel):
    type: Literal["clear"]

class SendHandled(BaseModel):
    type: Literal["handled"]
    data: HandledPacket

SendTypes = Annotated[
    Union[SendWidget, SendDelete, SendClear, SendHandled],
    Field(discriminator='type')
]

class Click(BaseModel):
    pass

class EventClick(BaseModel):
    type: Literal["click"]
    data: Click

EventTypes = Annotated[
    EventClick,
    Field(discriminator='type')
]


class Event(BaseModel):
    path: List[str]
    data: EventTypes

    def into_data(self):
        return self.data
