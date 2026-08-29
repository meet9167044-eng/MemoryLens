# DATA SCHEMA

## Core Memory Concept
A Memory represents one captured digital activity. The frontend should use this typed structure.

```typescript
type Memory = {
  id: string;
  timestamp: string; // ISO format
  source: {
    app: string;
    type: "desktop" | "browser" | "terminal" | "document" | "other";
  };
  screenshot: {
    id: string;
    imageUrl: string;
  };
  content: {
    ocrText: string;
    title: string;
    summary: string;
  };
  entities: Entity[];
  tags: string[];
  relatedMemories: RelatedMemory[];
  metadata: {
    language: string;
    contentType: string;
    confidence: number; // 0.0 to 1.0
  };
};
```

## Entity
Represents an extracted concept, tool, or person.

```typescript
type Entity = {
  id: string;
  name: string;
  type: "technology" | "framework" | "company" | "person" | "project" | "topic" | "tool" | "other";
};
```

## RelatedMemory
Represents a connection between the current memory and another memory.

```typescript
type RelatedMemory = {
  memoryId: string;
  relationship: "same_topic" | "related_error" | "same_project" | "entity_overlap" | "semantic_similarity";
  similarityScore?: number; // 0.0 to 1.0
};
```
