import { Memory } from '@/types/memory';
import { mockMemories } from '@/data/mockMemories';

class MemoryService {
  private memories: Memory[] = mockMemories;

  async getMemories(): Promise<Memory[]> {
    return Promise.resolve(this.memories.sort((a, b) => 
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    ));
  }

  async getMemoryById(id: string): Promise<Memory | undefined> {
    return Promise.resolve(this.memories.find(m => m.id === id));
  }

  async searchMemories(query: string): Promise<Memory[]> {
    const lowerQuery = query.toLowerCase();
    const results = this.memories.filter(m => {
      const inTitle = m.content.title.toLowerCase().includes(lowerQuery);
      const inOcr = m.content.ocrText.toLowerCase().includes(lowerQuery);
      const inSummary = m.content.summary.toLowerCase().includes(lowerQuery);
      const inTags = m.tags.some(t => t.toLowerCase().includes(lowerQuery));
      const inEntities = m.entities.some(e => e.name.toLowerCase().includes(lowerQuery));
      
      return inTitle || inOcr || inSummary || inTags || inEntities;
    });
    
    return Promise.resolve(results);
  }

  async getInsights() {
    // Return predefined synthetic patterns as requested in Phase 7 docs
    return Promise.resolve([
      {
        id: 'insight_1',
        title: 'GPU Debugging Pattern',
        description: 'Several memories are related to GPU configuration, CUDA errors, and PyTorch optimization.',
        memoryCount: 3,
        type: 'recurring_pattern'
      },
      {
        id: 'insight_2',
        title: 'Project Planning',
        description: 'You have been actively reviewing designs and communicating about MemoryLens.',
        memoryCount: 4,
        type: 'emerging_topic'
      }
    ]);
  }
  
  async getRecentTopics(): Promise<{ topic: string; count: number }[]> {
    return Promise.resolve([
      { topic: 'CUDA', count: 342 },
      { topic: 'PyTorch', count: 287 },
      { topic: 'Python', count: 198 },
      { topic: 'UI Design', count: 156 },
    ]);
  }
  
  async getActivitySummary() {
    return Promise.resolve({
      totalMemories: 1248,
      totalConnections: 386,
      totalTopics: 74,
      activityTimeHrs: 32
    });
  }
}

export const memoryService = new MemoryService();
