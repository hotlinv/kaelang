from pydantic import BaseModel, Field

from typing import List,Union, Optional
from kae.common import di

class NextRef(BaseModel):
    """指向下一个"""
    name:str = Field(title="文本")
    src: Optional[int] = Field(title="起始节点")
    tar: int = Field(title="终止节点")

class MayRef(BaseModel):
    """可选的下一个"""
    name:str = Field(title="文本")
    src: Optional[int] = Field(title="起始节点")
    tar: int = Field(title="终止节点")

class MatchRef(BaseModel):
    """语义对应"""
    name:str = Field(title="文本")
    sen: int = Field(title="句式id")
    inte: int = Field(title="意图id")

class Word(BaseModel):
    """词"""
    name: str = Field(title="文本")
    wordclass: str = Field(title="词性")
    next:Optional[Union[NextRef, MayRef, List[Union[NextRef, MayRef]]]] = Field(title="下一个")

class Sentence(BaseModel):
    """句式"""
    name: str = Field(title="文本")
    next: List[Union[NextRef, MayRef]] = Field(title="组成")
    src: Optional[str] = Field(title="来源")
    target: Optional[str] = Field(title="目标")
    action: Optional[str] = Field(title="动作")
    args: Optional[str] = Field(title="参数")
    # _next:Union[NextRef, MayRef] = Field(title="下一个")

class Intention(BaseModel):
    """意图"""
    name: str = Field(title="文本")
    foo: str = Field(title="可执行方法")
    model: str = Field(title="模块")
    src: Optional[str] = Field(title="来源")
    target: Optional[str] = Field(title="目标")
    action: Optional[str] = Field(title="动作")
    args: Optional[str] = Field(title="参数")



