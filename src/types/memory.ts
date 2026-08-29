export type Entity = {
  id: string;
  name: string;
  type: 'technology' | 'framework' | 'company' | 'person' | 'project' | 'topic' | 'tool' | 'other';
};

export type RelatedMemory = {
  memoryId: string;
  relationship: 'same_topic' | 'related_error' | 'same_project' | 'entity_overlap' | 'semantic_similarity';
  similarityScore?: number;
};

export type Memory = {
  id: string;
  timestamp: string;
  source: {
    app: string;
    type: 'desktop' | 'browser' | 'terminal' | 'document' | 'other';
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
    confidence: number;
  };
};
