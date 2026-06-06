from pydantic import BaseModel
from typing import Optional


class ThemeCreate(BaseModel):
    name: str
    icon: Optional[str] = "📌"


class ThemeResponse(BaseModel):
    id: int
    name: str
    icon: str
    date_created: str


class TypeCreate(BaseModel):
    name: str
    icon: Optional[str] = "📄"


class TypeResponse(BaseModel):
    id: int
    name: str
    icon: str
    date_created: str


class KnowledgeItemCreate(BaseModel):
    titre: str
    theme_name: str
    type_name: str
    description: Optional[str] = None
    code: Optional[str] = None
    solution: Optional[str] = None
    tags: Optional[str] = None


class KnowledgeItemUpdate(BaseModel):
    titre: Optional[str] = None
    theme_name: Optional[str] = None
    type_name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    solution: Optional[str] = None
    tags: Optional[str] = None


class KnowledgeItemResponse(BaseModel):
    id: int
    theme_id: Optional[int] = None
    type_id: Optional[int] = None
    titre: str
    description: Optional[str] = None
    code: Optional[str] = None
    solution: Optional[str] = None
    tags: Optional[str] = None
    date_creation: str
    date_modification: str
    theme_name: Optional[str] = None
    theme_icon: Optional[str] = None
    type_name: Optional[str] = None
    type_icon: Optional[str] = None
