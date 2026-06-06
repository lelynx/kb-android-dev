from typing import List

from fastapi import APIRouter, HTTPException

from models.kb_models import (
    KnowledgeItemCreate,
    KnowledgeItemResponse,
    KnowledgeItemUpdate,
    ThemeCreate,
    ThemeResponse,
    TypeCreate,
    TypeResponse,
)
from services import kb_service

router = APIRouter(prefix="/api/knowledge")


# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------

@router.get("/themes", response_model=List[ThemeResponse])
def get_themes():
    return kb_service.get_all_themes()


@router.post("/themes", response_model=ThemeResponse, status_code=201)
def create_theme(data: ThemeCreate):
    result = kb_service.create_theme(data.name, data.icon)
    if result is None:
        raise HTTPException(status_code=400, detail="Ce thème existe déjà")
    return result


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

@router.get("/types", response_model=List[TypeResponse])
def get_types():
    return kb_service.get_all_types()


@router.post("/types", response_model=TypeResponse, status_code=201)
def create_type(data: TypeCreate):
    result = kb_service.create_type(data.name, data.icon)
    if result is None:
        raise HTTPException(status_code=400, detail="Ce type existe déjà")
    return result


# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------

@router.get("/tags", response_model=List[str])
def get_tags():
    return kb_service.get_all_tags()


# ---------------------------------------------------------------------------
# Knowledge items
# ---------------------------------------------------------------------------

@router.get("", response_model=List[KnowledgeItemResponse])
def get_knowledge_items():
    return kb_service.get_all_knowledge_items()


@router.post("", response_model=KnowledgeItemResponse, status_code=201)
def create_knowledge_item(data: KnowledgeItemCreate):
    return kb_service.create_knowledge_item(data.dict())


@router.get("/{item_id}", response_model=KnowledgeItemResponse)
def get_knowledge_item(item_id: int):
    item = kb_service.get_knowledge_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Fiche introuvable")
    return item


@router.put("/{item_id}", response_model=KnowledgeItemResponse)
def update_knowledge_item(item_id: int, data: KnowledgeItemUpdate):
    result = kb_service.update_knowledge_item(
        item_id, data.dict(exclude_unset=True)
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Fiche introuvable")
    return result


@router.delete("/{item_id}", status_code=204)
def delete_knowledge_item(item_id: int):
    if not kb_service.delete_knowledge_item(item_id):
        raise HTTPException(status_code=404, detail="Fiche introuvable")
