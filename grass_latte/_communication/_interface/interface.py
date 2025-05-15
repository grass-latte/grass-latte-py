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


class ElementNode(BaseModel):
    type: Literal["node"]
    data: Node

class ElementText(BaseModel):
    type: Literal["text"]
    data: Text

class ElementProgress(BaseModel):
    type: Literal["progress"]
    data: Progress

class ElementButton(BaseModel):
    type: Literal["button"]
    data: Button

Element = Annotated[
    Union[ElementNode, ElementText, ElementProgress, ElementButton],
    Field(discriminator='type')
]

class ElementPacket(BaseModel):
    path: List[str]
    element: Element

class DeletePacket(BaseModel):
    path: List[str]

class HandledPacket(BaseModel):
    path: List[str]


class SendElement(BaseModel):
    type: Literal["element"]
    data: ElementPacket

class SendDelete(BaseModel):
    type: Literal["delete"]
    data: DeletePacket

class SendClear(BaseModel):
    type: Literal["clear"]

class SendHandled(BaseModel):
    type: Literal["handled"]
    data: HandledPacket

SendTypes = Annotated[
    Union[SendElement, SendDelete, SendClear, SendHandled],
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
