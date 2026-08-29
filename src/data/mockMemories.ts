import { Memory } from '../types/memory';

export const mockMemories: Memory[] = [
  {
    id: 'mem_1827',
    timestamp: '2026-08-29T10:15:00Z',
    source: {
      app: 'VS Code',
      type: 'desktop',
    },
    screenshot: {
      id: 'img_1827',
      imageUrl: 'https://placehold.co/800x450/1e1e1e/FFF?text=VS+Code+CUDA+Error',
    },
    content: {
      ocrText: 'RuntimeError: CUDA out of memory. Tried to allocate 512.00 MiB (GPU 0; 8.00 GiB total capacity; 6.50 GiB already allocated; 120.50 MiB free; 6.80 GiB reserved in total by PyTorch)',
      title: 'CUDA Out of Memory Error',
      summary: 'Encountered a CUDA OOM error while running a PyTorch training script.',
    },
    entities: [
      { id: 'ent_pytorch', name: 'PyTorch', type: 'framework' },
      { id: 'ent_cuda', name: 'CUDA', type: 'technology' },
    ],
    tags: ['error', 'gpu', 'python'],
    relatedMemories: [
      { memoryId: 'mem_1828', relationship: 'same_topic' }
    ],
    metadata: {
      language: 'python',
      contentType: 'code',
      confidence: 0.95,
    },
  },
  {
    id: 'mem_1828',
    timestamp: '2026-08-29T10:20:00Z',
    source: {
      app: 'Chrome',
      type: 'browser',
    },
    screenshot: {
      id: 'img_1828',
      imageUrl: 'https://placehold.co/800x450/2d2d2d/FFF?text=PyTorch+Docs',
    },
    content: {
      ocrText: 'Memory management in PyTorch. torch.cuda.empty_cache(). Releases all unoccupied cached memory currently held by the caching allocator so that those can be used in other GPU applications.',
      title: 'Reading PyTorch Memory Management Docs',
      summary: 'Looking up how to clear CUDA cache in PyTorch using torch.cuda.empty_cache().',
    },
    entities: [
      { id: 'ent_pytorch', name: 'PyTorch', type: 'framework' },
    ],
    tags: ['documentation', 'gpu', 'python', 'fix'],
    relatedMemories: [
      { memoryId: 'mem_1827', relationship: 'related_error' }
    ],
    metadata: {
      language: 'english',
      contentType: 'documentation',
      confidence: 0.92,
    },
  },
  {
    id: 'mem_1829',
    timestamp: '2026-08-29T10:25:00Z',
    source: {
      app: 'Terminal',
      type: 'terminal',
    },
    screenshot: {
      id: 'img_1829',
      imageUrl: 'https://placehold.co/800x450/000000/00FF00?text=nvidia-smi',
    },
    content: {
      ocrText: '+-----------------------------------------------------------------------------------------+\n| NVIDIA-SMI 535.104.05             Driver Version: 535.104.05   CUDA Version: 12.2     |\n|-----------------------------------------+------------------------+----------------------+\n|   0  NVIDIA GeForce RTX 3080 ...    Off |   00000000:01:00.0  On |                  N/A |\n|  0%   45C    P8             17W /  320W |    6500MiB /  10240MiB |     73%      Default |',
      title: 'Checking nvidia-smi in Terminal',
      summary: 'Monitoring GPU memory usage after getting the CUDA out of memory error.',
    },
    entities: [
      { id: 'ent_nvidia', name: 'NVIDIA', type: 'company' },
      { id: 'ent_gpu', name: 'GPU', type: 'technology' },
    ],
    tags: ['terminal', 'gpu', 'monitoring'],
    relatedMemories: [
      { memoryId: 'mem_1827', relationship: 'related_error' }
    ],
    metadata: {
      language: 'bash',
      contentType: 'logs',
      confidence: 0.98,
    },
  },
  {
    id: 'mem_1830',
    timestamp: '2026-08-29T11:00:00Z',
    source: {
      app: 'Figma',
      type: 'desktop',
    },
    screenshot: {
      id: 'img_1830',
      imageUrl: 'https://placehold.co/800x450/f5f5f5/333?text=Figma+UI+Design',
    },
    content: {
      ocrText: 'MemoryLens UI Prototype. Search bar, timeline view, recent memories grid. Typography: Inter, 14px.',
      title: 'Designing MemoryLens UI',
      summary: 'Working on the user interface mockups for the new MemoryLens web app in Figma.',
    },
    entities: [
      { id: 'ent_figma', name: 'Figma', type: 'tool' },
      { id: 'ent_memorylens', name: 'MemoryLens', type: 'project' },
    ],
    tags: ['design', 'ui', 'prototype'],
    relatedMemories: [],
    metadata: {
      language: 'english',
      contentType: 'design',
      confidence: 0.9,
    },
  },
  {
    id: 'mem_1831',
    timestamp: '2026-08-29T11:45:00Z',
    source: {
      app: 'Slack',
      type: 'desktop',
    },
    screenshot: {
      id: 'img_1831',
      imageUrl: 'https://placehold.co/800x450/4A154B/FFF?text=Slack+Conversation',
    },
    content: {
      ocrText: 'Alice: Hey Virat, did you push the latest UI changes?\nVirat: Working on them now. Should be ready by end of day.\nAlice: Great, let me know if you need help with the CSS.',
      title: 'Slack Chat with Alice about UI',
      summary: 'Discussing the timeline for the new UI changes with Alice in the #frontend channel.',
    },
    entities: [
      { id: 'ent_alice', name: 'Alice', type: 'person' },
      { id: 'ent_slack', name: 'Slack', type: 'tool' },
    ],
    tags: ['communication', 'team', 'ui'],
    relatedMemories: [
      { memoryId: 'mem_1830', relationship: 'same_project' }
    ],
    metadata: {
      language: 'english',
      contentType: 'chat',
      confidence: 0.99,
    },
  },
  {
    id: 'mem_1832',
    timestamp: '2026-08-29T13:15:00Z',
    source: {
      app: 'Chrome',
      type: 'browser',
    },
    screenshot: {
      id: 'img_1832',
      imageUrl: 'https://placehold.co/800x450/202124/FFF?text=StackOverflow',
    },
    content: {
      ocrText: 'How to center a div in CSS? display: flex; justify-content: center; align-items: center;',
      title: 'StackOverflow: Centering a Div',
      summary: 'Looking up the best practices for centering elements vertically and horizontally in CSS.',
    },
    entities: [
      { id: 'ent_css', name: 'CSS', type: 'technology' },
    ],
    tags: ['css', 'frontend', 'help'],
    relatedMemories: [],
    metadata: {
      language: 'english',
      contentType: 'forum',
      confidence: 0.96,
    },
  },
  {
    id: 'mem_1833',
    timestamp: '2026-08-29T14:00:00Z',
    source: {
      app: 'VS Code',
      type: 'desktop',
    },
    screenshot: {
      id: 'img_1833',
      imageUrl: 'https://placehold.co/800x450/1e1e1e/FFF?text=VS+Code+React',
    },
    content: {
      ocrText: 'import React, { useState, useEffect } from "react";\n\nexport const Timeline = () => {\n  const [data, setData] = useState([]);\n  // TODO: Fetch from memoryService\n};',
      title: 'Writing React Timeline Component',
      summary: 'Implementing the Timeline component for the MemoryLens frontend using React hooks.',
    },
    entities: [
      { id: 'ent_react', name: 'React', type: 'framework' },
      { id: 'ent_memorylens', name: 'MemoryLens', type: 'project' },
    ],
    tags: ['react', 'frontend', 'code'],
    relatedMemories: [
      { memoryId: 'mem_1830', relationship: 'same_project' }
    ],
    metadata: {
      language: 'typescript',
      contentType: 'code',
      confidence: 0.97,
    },
  },
  {
    id: 'mem_1834',
    timestamp: '2026-08-29T15:30:00Z',
    source: {
      app: 'Notion',
      type: 'document',
    },
    screenshot: {
      id: 'img_1834',
      imageUrl: 'https://placehold.co/800x450/FFF/000?text=Notion+Project+Specs',
    },
    content: {
      ocrText: 'Sprint 4 Planning. Goal: Complete the synthetic data layer and UI screens. Tasks: 1. mockMemories.ts 2. memoryService 3. UI Pages.',
      title: 'Reviewing Sprint 4 Goals in Notion',
      summary: 'Checking the project specifications and tasks for Sprint 4 in Notion.',
    },
    entities: [
      { id: 'ent_notion', name: 'Notion', type: 'tool' },
    ],
    tags: ['planning', 'documentation', 'sprint'],
    relatedMemories: [],
    metadata: {
      language: 'english',
      contentType: 'document',
      confidence: 0.95,
    },
  },
  {
    id: 'mem_1835',
    timestamp: '2026-08-29T16:00:00Z',
    source: {
      app: 'Terminal',
      type: 'terminal',
    },
    screenshot: {
      id: 'img_1835',
      imageUrl: 'https://placehold.co/800x450/000000/00FF00?text=Git+Commit',
    },
    content: {
      ocrText: '$ git commit -m "feat: Add mock memory data"\n[main 4f8b2a1] feat: Add mock memory data\n 1 file changed, 150 insertions(+)',
      title: 'Committing Mock Data',
      summary: 'Committing the initial mock memory data to the local Git repository.',
    },
    entities: [
      { id: 'ent_git', name: 'Git', type: 'technology' },
    ],
    tags: ['git', 'version-control', 'terminal'],
    relatedMemories: [],
    metadata: {
      language: 'bash',
      contentType: 'logs',
      confidence: 0.99,
    },
  },
  {
    id: 'mem_1836',
    timestamp: '2026-08-29T16:45:00Z',
    source: {
      app: 'Chrome',
      type: 'browser',
    },
    screenshot: {
      id: 'img_1836',
      imageUrl: 'https://placehold.co/800x450/202124/FFF?text=GitHub+PR',
    },
    content: {
      ocrText: 'Pull Request #42: Feature/frontend-ui-screens. Opened by virat. Reviewers: alice, bob. Checks passed.',
      title: 'Reviewing GitHub Pull Request',
      summary: 'Checking the status of the pull request for the frontend UI screens on GitHub.',
    },
    entities: [
      { id: 'ent_github', name: 'GitHub', type: 'tool' },
      { id: 'ent_alice', name: 'Alice', type: 'person' },
      { id: 'ent_bob', name: 'Bob', type: 'person' },
    ],
    tags: ['github', 'review', 'collaboration'],
    relatedMemories: [
      { memoryId: 'mem_1835', relationship: 'same_topic' }
    ],
    metadata: {
      language: 'english',
      contentType: 'webpage',
      confidence: 0.94,
    },
  },
];
