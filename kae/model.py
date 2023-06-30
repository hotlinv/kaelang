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
    # next:Optional[Union[NextRef, MayRef, List[Union[NextRef, MayRef]]]] = Field(title="下一个（批）id")

class UserWord(BaseModel):
    """用户定义词（用于调整分词词频和词性）"""
    name: str = Field(title="文本")
    wordclass: str = Field(title="词性")

class UserSpWord(BaseModel):
    """用户定义词（用于调整分词词频和词性）"""
    name: str = Field(title="文本列表")

class SameWord(BaseModel):
    """同义词"""
    name: str = Field(title="文本")
    wordclass: str = Field(title="词性")
    sameas: str = Field(title="同哪个同义")

class UselessWord(BaseModel):
    """鸡肋词（可以删掉不影响意思）"""
    name: str = Field(title="文本")
    wordclass: str = Field(title="词性")

class Sentence(BaseModel):
    """句式"""
    name: str = Field(title="文本")
    edges: List[int] = Field(title="组成id")
    src: Optional[str] = Field(title="来源")
    srcargs: Optional[str] = Field(title="源参数")
    target: Optional[str] = Field(title="目标")
    tarargs: Optional[str] = Field(title="目标参数（文件名等）")
    tartype: Optional[str] = Field(title="目标类型")
    action: Optional[str] = Field(title="动作")
    args: Optional[str] = Field(title="参数")
    # _next:Union[NextRef, MayRef] = Field(title="下一个")

class Expression(BaseModel):
    """表达式"""
    name: str = Field(title="文本")
    edges: List[int] = Field(title="组成id")
    src: Optional[str] = Field(title="来源")
    srcargs: Optional[str] = Field(title="源参数")
    target: Optional[str] = Field(title="目标")
    tarargs: Optional[str] = Field(title="目标参数（文件名等）")
    tartype: Optional[str] = Field(title="目标类型")
    action: Optional[str] = Field(title="动作")
    args: Optional[str] = Field(title="参数")

class Intention(BaseModel):
    """意图"""
    name: str = Field(title="文本")
    foo: str = Field(title="可执行方法")
    model: str = Field(title="模块")
    retcls: Optional[str] = Field(title="返回值类（需要调用）")
    src: Optional[str] = Field(title="来源")
    target: Optional[str] = Field(title="目标")
    tarargs: Optional[str] = Field(title="目标参数（文件名等）")
    tartype: Optional[str] = Field(title="目标类型")
    action: Optional[str] = Field(title="动作")
    args: Optional[str] = Field(title="参数")

class Module(BaseModel):
    '''模块'''
    name : str = Field(title="中文名")
    mod : str = Field(title="模块路径")
