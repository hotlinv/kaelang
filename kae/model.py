from pydantic import BaseModel, Field

from typing import List

class Word(BaseModel):
        """词"""
        name: str = Field(title="文本")
        wordclass: str = Field(title="词性")

class Sentence(BaseModel):
        """句式"""
        name: str = Field(title="文本")
        parts: List[str] = Field(title="组成")

class Intention(BaseModel):
        """意图"""
        name: str = Field(title="文本")
        foo: str = Field(title="可执行方法")
        model: str = Field(title="模块")

