import { Memory } from '../types/memory';
import { mockMemories } from '../data/mockMemories';

class MemoryService {
  private memories: Memory[] = mockMemories;

  async getMemories(): Promise<Memory[]> {
    // Simulate network delay
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([...this.memories].sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()));
      }, 300);
    });
  }

  async getMemoryById(id: string): Promise<Memory | undefined> {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(this.memories.find(m => m.id === id));
      }, 200);
    });
  }

  async searchMemories(query: string): Promise<Memory[]> {
    return new Promise((resolve) => {
      setTimeout(() => {
        const lowerQuery = query.toLowerCase();
        const results = this.memories.filter(m => {
          return (
            m.content.title.toLowerCase().includes(lowerQuery) ||
            m.content.summary.toLowerCase().includes(lowerQuery) ||
            m.content.ocrText.toLowerCase().includes(lowerQuery) ||
            m.tags.some(tag => tag.toLowerCase().includes(lowerQuery)) ||
            m.entities.some(e => e.name.toLowerCase().includes(lowerQuery))
          );
        });
        resolve(results.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()));
      }, 300);
    });
  }

  async getRecentTopics(): Promise<{ name: string; count: number }[]> {
    return new Promise((resolve) => {
      setTimeout(() => {
        const topicCounts: Record<string, number> = {};
        
        this.memories.forEach(memory => {
          memory.tags.forEach(tag => {
            topicCounts[tag] = (topicCounts[tag] || 0) + 1;
          });
        });

        const sortedTopics = Object.entries(topicCounts)
          .map(([name, count]) => ({ name, count }))
          .sort((a, b) => b.count - a.count)
          .slice(0, 5); // Return top 5

        resolve(sortedTopics);
      }, 200);
    });
  }
}

export const memoryService = new MemoryService();
