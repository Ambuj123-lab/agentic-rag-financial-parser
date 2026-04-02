# V2 Agentic Architecture

The V2 branch (`v2-local-heavy`) introduces a massively optimized, heavier execution pipeline running robust vector operations directly on-device.

### Pipeline Upgrades:
- **HyDE Generator (Node 3)**: Introduced to expand search surface area.
- **Hybrid Search (Node 5)**: Utilizing Jina MRL (Matryoshka Representation Learning) truncations + Dense logic.
- **Neural Cohere Reranking (Node 5B)**: Sifting top 15 chunks down to the 10 golden candidates.
- **LLM-as-a-Judge (Node 7)**: Verifying the context directly inside Qwen3 generation.

## Full Agentic StateGraph Execution

```mermaid
%%{init: {'theme': 'dark', 'themeVariables': { 'fontFamily': 'inter, arial, sans-serif', 'lineColor': '#6B7280'}}}%%
flowchart TD
    %% Node Styling (Dark Premium Cyber/AWS Palette)
    classDef user fill:#064E3B,stroke:#10B981,stroke-width:2px,color:#D1FAE5,rx:25,ry:25,font-weight:bold;
    classDef v2Upgrade fill:#78350F,stroke:#F59E0B,stroke-width:3px,color:#FEF3C7,rx:8,ry:8,font-weight:bold;
    classDef core fill:#1E3A8A,stroke:#3B82F6,stroke-width:2px,color:#DBEAFE,rx:8,ry:8;
    classDef cache fill:#7F1D1D,stroke:#EF4444,stroke-width:2px,color:#FEE2E2,rx:8,ry:8;
    classDef router fill:#4C1D95,stroke:#8B5CF6,stroke-width:2px,color:#EDE9FE,rx:8,ry:8;

    subgraph ClientLayer [🌍 CLOUD EDGE & CLIENT LAYER]
        USER(["👤 User Query"]):::user
        RESPONSE(["✨ Streamed Response"]):::user
    end

    subgraph RoutingLayer [🚦 ROUTING & INTENT ENGINE]
        N1["🔍 Node 1: Query Classifier<br/><small>Intent · Act · Ambiguity Detect</small>"]:::core
        N2[("⚡ Node 2: Cache Check<br/><small>Redis L1 / L2 / L3</small>")]:::cache
        N4["🛤️ Node 4: Act Router<br/><small>ITA1961 · ITA2025 · Rules · Budget</small>"]:::router
        N4B{"🔀 Node 4B: Cross-Act Merger<br/><small>Multi-collection Parallel Fetch</small>"}:::router
    end

    subgraph RetrievalLayer [🧠 SEMANTIC RETRIEVAL & RANKING]
        N3["💡 Node 3: HyDE Generator ⭐ V2<br/><small>Hypothetical Doc Embed (Qwen)</small>"]:::v2Upgrade
        N5["📚 Node 5: Hybrid Retriever ⭐ V2<br/><small>BM25 + Jina MRL Sparse/Dense</small>"]:::v2Upgrade
        N5B["🎯 Node 5B: Neural Reranker ⭐ V2<br/><small>Cohere · Top 10 Golden Chunks</small>"]:::v2Upgrade
    end

    subgraph GenerationLayer [⚡ SYNTHESIS & GENERATION]
        N6["⚙️ Node 6: Context Compressor<br/><small>512MB RAM Guard · Chunk Pruning</small>"]:::core
        N7["🧠 Node 7: LLM Generator ⭐ V2<br/><small>Qwen3 · LLM-as-a-Judge · Version-Tagged Prompts</small>"]:::v2Upgrade
        N8["📑 Node 8: Citation Builder<br/><small>Sec · Chap · Page Ref · PDF Data</small>"]:::core
    end

    %% Edges / Data Flow
    USER -->|Raw Text| N1
    N1 -->|Parsed Intent| N2
    N2 -.->|"Hit ⚡ (Cache Return)"| RESPONSE
    N2 ==>|"Miss ❌"| N3
    
    N3 ==>|Hypothetical Context| N4
    N4 -->|"Single Act/DB"| N5
    N4 -->|"Compare Acts"| N4B
    N4B ==>|Parallel Multi-Query| N5
    
    N5 ==>|100+ Candidates| N5B
    N5B ==>|Top 10 Golden Chunks| N6
    N6 -->|Optimized Context| N7
    N7 -->|Generated Markdown| N8
    N8 -.->|"Commit Cache & Stream"| RESPONSE

    %% Subgraph Box Styling
    style ClientLayer fill:none,stroke:#6B7280,stroke-width:2px,stroke-dasharray: 5 5,color:#D1D5DB,font-weight:bold
    style RoutingLayer fill:none,stroke:#6B7280,stroke-width:2px,stroke-dasharray: 5 5,color:#D1D5DB,font-weight:bold
    style RetrievalLayer fill:none,stroke:#6B7280,stroke-width:2px,stroke-dasharray: 5 5,color:#D1D5DB,font-weight:bold
    style GenerationLayer fill:none,stroke:#6B7280,stroke-width:2px,stroke-dasharray: 5 5,color:#D1D5DB,font-weight:bold
```
