from pydantic import BaseModel, Field
from typing import List, Optional

class SourceSchema(BaseModel):
    app: str
    type: str

class ScreenshotSchema(BaseModel):
    id: str
    imageUrl: str

class ContentSchema(BaseModel):
    ocrText: str
    title: str
    summary: str

class EntitySchema(BaseModel):
    id: str
    name: str
    type: str

class RelatedMemorySchema(BaseModel):
    memoryId: str
    relationship: str
    similarityScore: Optional[float] = None

class MetadataSchema(BaseModel):
    language: str
    contentType: str
    confidence: float

class MemoryResponse(BaseModel):
    """
    Exact JSON mapping required by the React frontend (Phase 11).
    Maps to `export type Memory` in src/types/memory.ts.
    """
    id: str
    timestamp: str
    source: SourceSchema
    screenshot: ScreenshotSchema
    content: ContentSchema
    entities: List[EntitySchema]
    tags: List[str]
    relatedMemories: List[RelatedMemorySchema]
    metadata: MetadataSchema
