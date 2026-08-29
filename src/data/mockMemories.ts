import { Memory } from '@/types/memory';

export const mockMemories: Memory[] = [
  {
    id: "mem_1827",
    timestamp: "2026-01-14T10:32:00",
    source: { app: "VS Code", type: "desktop" },
    screenshot: { id: "1827", imageUrl: "/synthetic/screenshots/1827.png" },
    content: {
      ocrText: "RuntimeError: CUDA out of memory...",
      title: "CUDA Out of Memory Error",
      summary: "A PyTorch process exceeded available GPU memory."
    },
    entities: [
      { id: "entity_cuda", name: "CUDA", type: "technology" },
      { id: "entity_pytorch", name: "PyTorch", type: "framework" },
      { id: "entity_nvidia", name: "NVIDIA", type: "company" }
    ],
    tags: ["error", "gpu", "python"],
    relatedMemories: [
      { memoryId: "mem_1842", relationship: "same_topic", similarityScore: 0.91 },
      { memoryId: "mem_1809", relationship: "related_error", similarityScore: 0.87 }
    ],
    metadata: { language: "en", contentType: "error", confidence: 0.96 }
  },
  {
    id: "mem_1842",
    timestamp: "2026-01-14T11:15:00",
    source: { app: "Chrome", type: "browser" },
    screenshot: { id: "1842", imageUrl: "/synthetic/screenshots/generic.png" },
    content: {
      ocrText: "Understanding PyTorch Memory Management...",
      title: "PyTorch GPU Optimization",
      summary: "Reading PyTorch documentation on how to optimize GPU memory."
    },
    entities: [
      { id: "entity_pytorch", name: "PyTorch", type: "framework" },
      { id: "entity_gpu", name: "GPU", type: "technology" }
    ],
    tags: ["gpu", "optimization", "learning"],
    relatedMemories: [
      { memoryId: "mem_1827", relationship: "same_topic", similarityScore: 0.91 }
    ],
    metadata: { language: "en", contentType: "documentation", confidence: 0.99 }
  },
  {
    id: "mem_1809",
    timestamp: "2026-01-13T09:42:00",
    source: { app: "Terminal", type: "terminal" },
    screenshot: { id: "1809", imageUrl: "/synthetic/screenshots/generic.png" },
    content: {
      ocrText: "nvidia-smi... Processes: python",
      title: "GPU Configuration Check",
      summary: "Ran nvidia-smi to check which processes are consuming GPU."
    },
    entities: [
      { id: "entity_nvidia", name: "NVIDIA", type: "company" },
      { id: "entity_python", name: "Python", type: "technology" }
    ],
    tags: ["system", "gpu", "debugging"],
    relatedMemories: [
      { memoryId: "mem_1827", relationship: "related_error", similarityScore: 0.87 }
    ],
    metadata: { language: "en", contentType: "terminal_output", confidence: 0.95 }
  },
  {
    id: "mem_1901",
    timestamp: "2026-01-14T14:20:00",
    source: { app: "Figma", type: "desktop" },
    screenshot: { id: "1901", imageUrl: "/synthetic/screenshots/generic.png" },
    content: {
      ocrText: "MemoryLens Dashboard Design...",
      title: "UI Design for Memory Explorer",
      summary: "Designing the grid layout for the MemoryLens explorer screen."
    },
    entities: [
      { id: "entity_figma", name: "Figma", type: "tool" },
      { id: "entity_memorylens", name: "MemoryLens", type: "project" }
    ],
    tags: ["design", "ui", "project planning"],
    relatedMemories: [],
    metadata: { language: "en", contentType: "design", confidence: 0.92 }
  },
  {
    id: "mem_1905",
    timestamp: "2026-01-14T15:00:00",
    source: { app: "Slack", type: "desktop" },
    screenshot: { id: "1905", imageUrl: "/synthetic/screenshots/generic.png" },
    content: {
      ocrText: "Hey Virat, the new Figma designs look great. Can we implement the timeline view next?",
      title: "Team Sync on Timeline Feature",
      summary: "Discussing the implementation of the timeline view with the team."
    },
    entities: [
      { id: "entity_slack", name: "Slack", type: "tool" },
      { id: "entity_memorylens", name: "MemoryLens", type: "project" }
    ],
    tags: ["communication", "project planning"],
    relatedMemories: [
      { memoryId: "mem_1901", relationship: "same_project", similarityScore: 0.85 }
    ],
    metadata: { language: "en", contentType: "chat", confidence: 0.98 }
  },
  {
    id: "mem_1750",
    timestamp: "2026-01-12T10:00:00",
    source: { app: "Jupyter", type: "browser" },
    screenshot: { id: "1750", imageUrl: "/synthetic/screenshots/generic.png" },
    content: {
      ocrText: "import pandas as pd... df = pd.read_csv('dataset.csv')",
      title: "Data Preprocessing Notebook",
      summary: "Writing pandas scripts to clean up the initial training dataset."
    },
    entities: [
      { id: "entity_pandas", name: "Pandas", type: "framework" },
      { id: "entity_python", name: "Python", type: "technology" }
    ],
    tags: ["data science", "python", "research"],
    relatedMemories: [],
    metadata: { language: "en", contentType: "code", confidence: 0.97 }
  },
  {
    id: "mem_1762",
    timestamp: "2026-01-12T11:30:00",
    source: { app: "Chrome", type: "browser" },
    screenshot: { id: "1762", imageUrl: "/synthetic/screenshots/generic.png" },
    content: {
      ocrText: "StackOverflow: How to handle NaN values in pandas...",
      title: "Pandas NaN Handling",
      summary: "Searching for best practices on dropping vs imputing missing values."
    },
    entities: [
      { id: "entity_pandas", name: "Pandas", type: "framework" },
      { id: "entity_stackoverflow", name: "StackOverflow", type: "tool" }
    ],
    tags: ["research", "data science"],
    relatedMemories: [
      { memoryId: "mem_1750", relationship: "same_topic", similarityScore: 0.88 }
    ],
    metadata: { language: "en", contentType: "web_page", confidence: 0.94 }
  },
  {
    id: "mem_1920",
    timestamp: "2026-01-15T09:10:00",
    source: { app: "VS Code", type: "desktop" },
    screenshot: { id: "1920", imageUrl: "/synthetic/screenshots/generic.png" },
    content: {
      ocrText: "export const mockMemories: Memory[] = [...]",
      title: "Implementing Mock Data",
      summary: "Writing the mock data service for MemoryLens Phase 2."
    },
    entities: [
      { id: "entity_typescript", name: "TypeScript", type: "technology" },
      { id: "entity_memorylens", name: "MemoryLens", type: "project" }
    ],
    tags: ["development", "web development"],
    relatedMemories: [],
    metadata: { language: "en", contentType: "code", confidence: 0.99 }
  },
  {
    id: "mem_1921",
    timestamp: "2026-01-15T09:15:00",
    source: { app: "Terminal", type: "terminal" },
    screenshot: { id: "1921", imageUrl: "/synthetic/screenshots/generic.png" },
    content: {
      ocrText: "npm run dev... VITE v5.4.1 ready in 250 ms",
      title: "Starting Dev Server",
      summary: "Booting up the Vite development server."
    },
    entities: [
      { id: "entity_vite", name: "Vite", type: "tool" }
    ],
    tags: ["system", "web development"],
    relatedMemories: [
      { memoryId: "mem_1920", relationship: "same_project", similarityScore: 0.82 }
    ],
    metadata: { language: "en", contentType: "terminal_output", confidence: 0.96 }
  },
  {
    id: "mem_1930",
    timestamp: "2026-01-15T11:00:00",
    source: { app: "PDF Viewer", type: "document" },
    screenshot: { id: "1930", imageUrl: "/synthetic/screenshots/generic.png" },
    content: {
      ocrText: "Attention Is All You Need. Vaswani et al...",
      title: "Reading Transformer Paper",
      summary: "Reviewing the original Transformer architecture for a new feature."
    },
    entities: [
      { id: "entity_ai", name: "AI", type: "topic" }
    ],
    tags: ["research", "learning"],
    relatedMemories: [],
    metadata: { language: "en", contentType: "academic_paper", confidence: 0.91 }
  },
  {
    id: "mem_1935",
    timestamp: "2026-01-15T13:45:00",
    source: { app: "Chrome", type: "browser" },
    screenshot: { id: "1935", imageUrl: "/synthetic/screenshots/generic.png" },
    content: {
      ocrText: "Hugging Face - Models: Transformer...",
      title: "Browsing Hugging Face Models",
      summary: "Looking for pre-trained models to test locally."
    },
    entities: [
      { id: "entity_huggingface", name: "Hugging Face", type: "company" },
      { id: "entity_ai", name: "AI", type: "topic" }
    ],
    tags: ["research", "ai"],
    relatedMemories: [
      { memoryId: "mem_1930", relationship: "same_topic", similarityScore: 0.89 }
    ],
    metadata: { language: "en", contentType: "web_page", confidence: 0.95 }
  },
  {
    id: "mem_1940",
    timestamp: "2026-01-15T15:20:00",
    source: { app: "VS Code", type: "desktop" },
    screenshot: { id: "1940", imageUrl: "/synthetic/screenshots/generic.png" },
    content: {
      ocrText: "function SearchBar() { return <input type='text' /> }",
      title: "Building Search Component",
      summary: "Implementing the UI for the search bar in the application shell."
    },
    entities: [
      { id: "entity_react", name: "React", type: "framework" },
      { id: "entity_typescript", name: "TypeScript", type: "technology" }
    ],
    tags: ["development", "ui"],
    relatedMemories: [
      { memoryId: "mem_1920", relationship: "same_project", similarityScore: 0.90 }
    ],
    metadata: { language: "en", contentType: "code", confidence: 0.98 }
  },
  {
    id: "mem_1945",
    timestamp: "2026-01-15T16:00:00",
    source: { app: "Slack", type: "desktop" },
    screenshot: { id: "1945", imageUrl: "/synthetic/screenshots/generic.png" },
    content: {
      ocrText: "The DevJams presentation is tomorrow at 10 AM.",
      title: "DevJams Presentation Reminder",
      summary: "Team channel update regarding the DevJams Review 1 schedule."
    },
    entities: [
      { id: "entity_devjams", name: "DevJams", type: "project" }
    ],
    tags: ["communication", "planning"],
    relatedMemories: [],
    metadata: { language: "en", contentType: "chat", confidence: 0.99 }
  },
  {
    id: "mem_1950",
    timestamp: "2026-01-15T16:15:00",
    source: { app: "Chrome", type: "browser" },
    screenshot: { id: "1950", imageUrl: "/synthetic/screenshots/generic.png" },
    content: {
      ocrText: "Google Slides - MemoryLens Pitch Deck",
      title: "Editing Pitch Deck",
      summary: "Finalizing the slides for tomorrow's presentation."
    },
    entities: [
      { id: "entity_devjams", name: "DevJams", type: "project" },
      { id: "entity_memorylens", name: "MemoryLens", type: "project" }
    ],
    tags: ["documentation", "planning"],
    relatedMemories: [
      { memoryId: "mem_1945", relationship: "same_project", similarityScore: 0.95 }
    ],
    metadata: { language: "en", contentType: "document", confidence: 0.94 }
  }
];
