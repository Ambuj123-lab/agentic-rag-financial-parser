<div align="center">

<!-- Animated Header -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,16,18,20&height=200&section=header&text=Agentic%20Financial%20Parser&fontSize=42&fontColor=ffffff&fontAlignY=35&desc=8-Node%20LangGraph%20StateGraph%20•%20Production-Grade%20Agentic%20RAG&descSize=16&descAlignY=55&animation=fadeIn" width="100%"/>

<br/>

[![Live Demo](https://img.shields.io/badge/🚀_LIVE_DEMO-Visit_App-D4A574?style=for-the-badge&logoColor=white)](https://agentic-rag-financial-parser.onrender.com)
[![RAG Docs](https://img.shields.io/badge/📖_RAG_DOCS-Technical_Docs-4A90D9?style=for-the-badge)](https://ambuj-rag-docs.netlify.app/)
[![Portfolio](https://img.shields.io/badge/👤_PORTFOLIO-Ambuj_Tripathi-34A853?style=for-the-badge)](https://ambuj-portfolio-v2.netlify.app/)

<br/>

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![LangGraph](https://img.shields.io/badge/LangGraph-StateGraph-FF6B35?style=flat-square)](https://langchain-ai.github.io/langgraph/)
[![Docker](https://img.shields.io/badge/Docker-Multi--Stage-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com)

</div>

---

## ⚡ What Is This?

An **autonomous, 8-node Agentic RAG pipeline** that parses and queries complex Indian financial & legal documents — Union Budget, Finance Bill, Tax Laws, PF/Pension Schemes, RBI KYC, and Constitution of India — using a purpose-built state machine that **thinks before it answers**.

Unlike traditional RAG (retrieve → generate), this system employs an **agentic flow** where each query passes through specialized nodes that classify intent, cross-question vague queries, guard against hallucinations, and verify answer grounding — all orchestrated via **LangGraph StateGraph**.

---

## 🏗️ System Architecture

<!-- Animated SVG Architecture Diagram -->
<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 860" width="100%" height="auto" style="display:block; border-radius:12px; max-width:1280px;">
<defs>
  <radialGradient id="masterBG" cx="38%" cy="35%" r="70%">
    <stop offset="0%" stop-color="#0e0e1f"/>
    <stop offset="55%" stop-color="#080810"/>
    <stop offset="100%" stop-color="#030306"/>
  </radialGradient>
  <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#c9a84c"/>
    <stop offset="50%" stop-color="#e8c96d"/>
    <stop offset="100%" stop-color="#b8922e"/>
  </linearGradient>
  <linearGradient id="goldLine" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#c9a84c" stop-opacity="0"/>
    <stop offset="30%" stop-color="#e8c96d"/>
    <stop offset="70%" stop-color="#c9a84c"/>
    <stop offset="100%" stop-color="#c9a84c" stop-opacity="0"/>
  </linearGradient>

  <linearGradient id="gClassifier" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#1a1040"/><stop offset="100%" stop-color="#2d1b69"/>
  </linearGradient>
  <linearGradient id="gReject" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#2a0808"/><stop offset="100%" stop-color="#4a1212"/>
  </linearGradient>
  <linearGradient id="gGreet" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#082010"/><stop offset="100%" stop-color="#103a20"/>
  </linearGradient>
  <linearGradient id="gCrossQ" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#1e1205"/><stop offset="100%" stop-color="#3a2208"/>
  </linearGradient>
  <linearGradient id="gRetriever" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#051520"/><stop offset="100%" stop-color="#0a2a3a"/>
  </linearGradient>
  <linearGradient id="gGenerator" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#1e1400"/><stop offset="100%" stop-color="#3a2800"/>
  </linearGradient>
  <linearGradient id="gGuard" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#180a2e"/><stop offset="100%" stop-color="#2e1258"/>
  </linearGradient>
  <linearGradient id="gPost" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#051510"/><stop offset="100%" stop-color="#0a2a1a"/>
  </linearGradient>
  <linearGradient id="panelGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#0f0f1e"/><stop offset="100%" stop-color="#080810"/>
  </linearGradient>
  <linearGradient id="dbPinecone" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#0d1f3a"/><stop offset="100%" stop-color="#1a3a6a"/>
  </linearGradient>
  <linearGradient id="dbSupabase" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#0a2010"/><stop offset="100%" stop-color="#154030"/>
  </linearGradient>
  <linearGradient id="dbMongo" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#081808"/><stop offset="100%" stop-color="#103a10"/>
  </linearGradient>
  <linearGradient id="dbRedis" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#200808"/><stop offset="100%" stop-color="#401010"/>
  </linearGradient>
  <linearGradient id="dbLangfuse" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#140820"/><stop offset="100%" stop-color="#281040"/>
  </linearGradient>

  <filter id="softDrop">
    <feDropShadow dx="0" dy="4" stdDeviation="10" flood-color="#000000" flood-opacity="0.8"/>
  </filter>
  <filter id="panelDrop">
    <feDropShadow dx="0" dy="4" stdDeviation="20" flood-color="#c9a84c" flood-opacity="0.08"/>
  </filter>
  <filter id="goldGlow">
    <feGaussianBlur stdDeviation="8" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>

  <marker id="arrGold" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto">
    <path d="M0,0 L0,6 L7,3 z" fill="#c9a84c"/>
  </marker>
  <marker id="arrDim" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
    <path d="M0,0 L0,6 L6,3 z" fill="#6060a0"/>
  </marker>
  <marker id="arrRed" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
    <path d="M0,0 L0,6 L6,3 z" fill="#cc4444"/>
  </marker>
  <marker id="arrGreen" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
    <path d="M0,0 L0,6 L6,3 z" fill="#44cc88"/>
  </marker>
  <marker id="arrAmber" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
    <path d="M0,0 L0,6 L6,3 z" fill="#cc9944"/>
  </marker>

  <!-- animateMotion paths -->
  <path id="p5" d="M120 376 L120 462" fill="none"/>
  <path id="p6" d="M202 498 L345 498" fill="none"/>
  <path id="p7" d="M482 498 L568 498" fill="none"/>
  <path id="p8" d="M738 498 L828 498" fill="none"/>

  <style>
    @keyframes goldPulse {
      0%,100%{ filter: drop-shadow(0 0 5px #c9a84c99) drop-shadow(0 0 12px #c9a84c44); }
      50%{ filter: drop-shadow(0 0 14px #e8c96d) drop-shadow(0 0 28px #c9a84c88); }
    }
    @keyframes dimPulse { 0%,100%{ opacity:0.85; } 50%{ opacity:1; } }
    @keyframes titleShimmer { 0%,100%{ opacity:0.9; } 50%{ opacity:1; } }
    .nClassifier { animation: goldPulse 3s ease-in-out infinite; }
    .nRetriever  { animation: goldPulse 3.4s ease-in-out infinite 0.3s; }
    .nGenerator  { animation: goldPulse 2.8s ease-in-out infinite 0.6s; }
    .nGuard      { animation: goldPulse 3.2s ease-in-out infinite 0.9s; }
    .nPost       { animation: dimPulse 3s ease-in-out infinite; }
    .titleText   { animation: titleShimmer 4s ease-in-out infinite; }
  </style>
</defs>

<!-- BG -->
<rect width="1280" height="860" fill="url(#masterBG)"/>
<radialGradient id="vignette" cx="50%" cy="50%" r="70%">
  <stop offset="60%" stop-color="transparent"/>
  <stop offset="100%" stop-color="#000000" stop-opacity="0.4"/>
</radialGradient>
<rect width="1280" height="860" fill="url(#vignette)"/>
<g opacity="0.03" stroke="#c9a84c" stroke-width="0.5">
  <line x1="0" y1="100" x2="1280" y2="100"/><line x1="0" y1="200" x2="1280" y2="200"/>
  <line x1="0" y1="300" x2="1280" y2="300"/><line x1="0" y1="400" x2="1280" y2="400"/>
  <line x1="0" y1="500" x2="1280" y2="500"/><line x1="0" y1="600" x2="1280" y2="600"/>
  <line x1="0" y1="700" x2="1280" y2="700"/><line x1="0" y1="800" x2="1280" y2="800"/>
  <line x1="120" y1="0" x2="120" y2="860"/><line x1="280" y1="0" x2="280" y2="860"/>
  <line x1="440" y1="0" x2="440" y2="860"/><line x1="600" y1="0" x2="600" y2="860"/>
  <line x1="760" y1="0" x2="760" y2="860"/><line x1="920" y1="0" x2="920" y2="860"/>
  <line x1="1080" y1="0" x2="1080" y2="860"/>
</g>
<rect x="0" y="0" width="1280" height="2" fill="url(#goldLine)" opacity="0.6"/>

<!-- TITLE -->
<text x="640" y="44" text-anchor="middle" class="titleText" font-family="'Segoe UI',sans-serif" font-size="28" font-weight="300" fill="#e8c96d" letter-spacing="6">AGENTIC FINANCIAL PARSER</text>
<text x="640" y="65" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="10" fill="#9090b0" letter-spacing="4">8-NODE LANGGRAPH STATEGRAPH · PRECISION-FIRST · PRODUCTION 2026</text>
<line x1="480" y1="72" x2="800" y2="72" stroke="url(#goldLine)" stroke-width="1" opacity="0.5"/>

<!-- SECTION BANDS -->
<rect x="28" y="82" width="960" height="68" rx="8" fill="#ffffff04" stroke="#c9a84c25" stroke-width="1"/>
<text x="46" y="97" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#c9a84c" letter-spacing="2">FRONTEND &amp; AUTH</text>

<rect x="28" y="162" width="960" height="400" rx="8" fill="#ffffff02" stroke="#c9a84c18" stroke-width="1"/>
<text x="46" y="178" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#c9a84c" letter-spacing="2">8-NODE AGENTIC PIPELINE</text>

<rect x="28" y="574" width="960" height="118" rx="8" fill="#ffffff02" stroke="#c9a84c18" stroke-width="1"/>
<text x="46" y="590" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#c9a84c" letter-spacing="2">INFRASTRUCTURE</text>

<!-- ══ FRONTEND ══ -->
<!-- React SPA -->
<g filter="url(#softDrop)">
  <rect x="48" y="95" width="148" height="42" rx="21" fill="#0e0e22" stroke="#5050a0" stroke-width="1.5"/>
  <circle cx="73" cy="116" r="11" fill="#1a1a3a"/>
  <text x="73" y="120" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#8888dd">⚛</text>
  <text x="138" y="111" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="10" font-weight="700" fill="#aaaaee">React SPA</text>
  <text x="138" y="126" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#8888bb">Vite · Tailwind · SSE</text>
</g>

<path d="M197 116 L246 116" stroke="#6060a0" stroke-width="1.5" marker-end="url(#arrDim)" fill="none"/>
<text x="222" y="110" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#9090c0">HTTPS</text>

<!-- Google OAuth -->
<g filter="url(#softDrop)">
  <rect x="248" y="95" width="155" height="42" rx="21" fill="#1a0808" stroke="#aa3333" stroke-width="1.5"/>
  <text x="275" y="121" text-anchor="middle" font-family="sans-serif" font-size="15" fill="#ee5555">G</text>
  <text x="348" y="111" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="10" font-weight="700" fill="#ee9999">Google OAuth 2.0</text>
  <text x="348" y="126" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#cc7777">JWT · 7-day expiry · HS256</text>
</g>

<path d="M404 116 L452 116" stroke="#aa3333" stroke-width="1.5" marker-end="url(#arrRed)" fill="none"/>

<!-- FastAPI -->
<g filter="url(#softDrop)">
  <rect x="454" y="95" width="158" height="42" rx="21" fill="#05121a" stroke="#2a6080" stroke-width="1.5"/>
  <text x="480" y="121" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#44aacc">⚡</text>
  <text x="555" y="111" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="10" font-weight="700" fill="#66ccee">FastAPI Backend</text>
  <text x="555" y="126" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#4499bb">Async · Docker · Render 512MB</text>
</g>

<!-- Security badge -->
<g filter="url(#softDrop)">
  <rect x="786" y="93" width="175" height="46" rx="6" fill="#0a0a16" stroke="#c9a84c50" stroke-width="1"/>
  <rect x="786" y="93" width="175" height="2" rx="1" fill="url(#goldGrad)" opacity="0.7"/>
  <text x="873" y="112" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8.5" font-weight="700" fill="#e8c96d" letter-spacing="1">🔐 SECURITY</text>
  <text x="873" y="125" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#c0b070">7-Layer Upload Shield</text>
  <text x="873" y="137" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#a09060">SHA-256 · JWT · OAuth 2.0</text>
</g>

<path d="M533 138 L533 170" stroke="#2a6080" stroke-width="1.5" stroke-dasharray="4 3" fill="none"/>

<!-- ══ NODE 1: CLASSIFIER ══ -->
<path d="M120 200 L120 325" stroke="#c9a84c" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arrGold)" fill="none"/>
<text x="132" y="266" font-family="'Segoe UI',sans-serif" font-size="9" font-weight="600" fill="#c9a84c">query</text>

<circle r="3.5" fill="#e8c96d" opacity="0.9">
  <animateMotion dur="2s" repeatCount="indefinite">
    <mpath href="#p5"/>
  </animateMotion>
</circle>

<g class="nClassifier" filter="url(#softDrop)">
  <ellipse cx="120" cy="340" rx="78" ry="36" fill="url(#gClassifier)" stroke="#6644cc" stroke-width="2"/>
  <ellipse cx="120" cy="340" rx="78" ry="36" fill="none" stroke="#c9a84c" stroke-width="0.5" opacity="0.5"/>
  <text x="120" y="328" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#c9a84c" letter-spacing="1">NODE 01</text>
  <text x="120" y="345" text-anchor="middle" font-family="sans-serif" font-size="14">🧠</text>
  <text x="120" y="362" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="12" font-weight="700" fill="#ddccff">Classifier</text>
</g>

<!-- Routing arrows -->
<path d="M192 322 Q270 262 360 252" stroke="#cc4444" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#arrRed)" fill="none"/>
<text x="262" y="272" font-family="'Segoe UI',sans-serif" font-size="9" font-weight="600" fill="#ff8888">abusive</text>

<path d="M198 336 L360 336" stroke="#44cc88" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#arrGreen)" fill="none"/>
<text x="272" y="328" font-family="'Segoe UI',sans-serif" font-size="9" font-weight="600" fill="#88ffbb">greeting</text>

<path d="M192 360 Q270 408 360 418" stroke="#cc9944" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#arrAmber)" fill="none"/>
<text x="258" y="410" font-family="'Segoe UI',sans-serif" font-size="9" font-weight="600" fill="#ffcc77">vague</text>

<path d="M120 376 L120 462" stroke="#c9a84c" stroke-width="2.5" stroke-dasharray="5 3" marker-end="url(#arrGold)" fill="none"/>
<text x="132" y="422" font-family="'Segoe UI',sans-serif" font-size="9" font-weight="700" fill="#e8c96d">rag →</text>

<circle r="3.5" fill="#e8c96d" opacity="0.9">
  <animateMotion dur="1.8s" repeatCount="indefinite" begin="0.3s">
    <mpath href="#p5"/>
  </animateMotion>
</circle>

<!-- NODE 2: REJECT -->
<g filter="url(#softDrop)">
  <rect x="362" y="226" width="120" height="52" rx="26" fill="url(#gReject)" stroke="#cc4444" stroke-width="1.8"/>
  <text x="422" y="244" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#ffaaaa" letter-spacing="1">NODE 02</text>
  <text x="422" y="260" text-anchor="middle" font-family="sans-serif" font-size="13">🚫</text>
  <text x="422" y="273" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="11" font-weight="700" fill="#ff9999">Reject</text>
</g>
<path d="M482 252 L528 252" stroke="#cc4444" stroke-width="1.5" marker-end="url(#arrRed)" fill="none"/>
<rect x="530" y="243" width="40" height="18" rx="9" fill="#2a0808" stroke="#cc4444" stroke-width="1.2"/>
<text x="550" y="256" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#ff8888">END</text>
<text x="582" y="256" font-family="'Segoe UI',sans-serif" font-size="8" fill="#cc8888">0 LLM calls</text>

<!-- NODE 3: GREET -->
<g filter="url(#softDrop)">
  <rect x="362" y="311" width="120" height="52" rx="26" fill="url(#gGreet)" stroke="#44cc88" stroke-width="1.8"/>
  <text x="422" y="329" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#aaffcc" letter-spacing="1">NODE 03</text>
  <text x="422" y="345" text-anchor="middle" font-family="sans-serif" font-size="13">👋</text>
  <text x="422" y="358" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="11" font-weight="700" fill="#66ffaa">Greet</text>
</g>
<path d="M482 337 L528 337" stroke="#44cc88" stroke-width="1.5" marker-end="url(#arrGreen)" fill="none"/>
<rect x="530" y="328" width="40" height="18" rx="9" fill="#082010" stroke="#44cc88" stroke-width="1.2"/>
<text x="550" y="341" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#88ffcc">END</text>
<text x="582" y="341" font-family="'Segoe UI',sans-serif" font-size="8" fill="#66cc99">No VectorDB</text>

<!-- NODE 4: CROSSQUESTIONER -->
<g filter="url(#softDrop)">
  <rect x="362" y="394" width="148" height="52" rx="26" fill="url(#gCrossQ)" stroke="#cc9944" stroke-width="1.8"/>
  <text x="436" y="412" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#ffddaa" letter-spacing="1">NODE 04</text>
  <text x="436" y="428" text-anchor="middle" font-family="sans-serif" font-size="13">❓</text>
  <text x="436" y="441" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="11" font-weight="700" fill="#ffcc77">CrossQuestioner</text>
</g>

<!-- Human-in-the-Loop arrow -->
<path d="M362 420 Q310 420 275 400 Q238 378 198 362" stroke="#cc9944" stroke-width="1.8" stroke-dasharray="4 3" marker-end="url(#arrAmber)" fill="none"/>
<rect x="215" y="408" width="138" height="28" rx="5" fill="#1a1005" stroke="#cc9944" stroke-width="1"/>
<text x="284" y="421" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8.5" font-weight="700" fill="#ffcc77">⟳ HUMAN-IN-THE-LOOP</text>
<text x="284" y="432" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="7.5" fill="#ddaa55">max 2 rounds · clarify query</text>

<!-- NODE 5: RETRIEVER -->
<g class="nRetriever" filter="url(#softDrop)">
  <ellipse cx="120" cy="498" rx="82" ry="36" fill="url(#gRetriever)" stroke="#2288bb" stroke-width="2"/>
  <ellipse cx="120" cy="498" rx="82" ry="36" fill="none" stroke="#c9a84c" stroke-width="0.5" opacity="0.4"/>
  <text x="120" y="484" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#c9a84c" letter-spacing="1">NODE 05</text>
  <text x="120" y="500" text-anchor="middle" font-family="sans-serif" font-size="13">🔍</text>
  <text x="120" y="517" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="10" font-weight="700" fill="#77ccee">PII Shield + Retriever</text>
</g>

<path d="M202 498 L345 498" stroke="#c9a84c" stroke-width="2.5" marker-end="url(#arrGold)" fill="none"/>
<circle r="3.5" fill="#e8c96d" opacity="0.9">
  <animateMotion dur="1.6s" repeatCount="indefinite">
    <mpath href="#p6"/>
  </animateMotion>
</circle>

<!-- NODE 6: GENERATOR -->
<g class="nGenerator" filter="url(#softDrop)">
  <rect x="346" y="470" width="136" height="58" rx="29" fill="url(#gGenerator)" stroke="#bb8822" stroke-width="2"/>
  <rect x="346" y="470" width="136" height="58" rx="29" fill="none" stroke="#c9a84c" stroke-width="0.6" opacity="0.5"/>
  <text x="414" y="487" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#c9a84c" letter-spacing="1">NODE 06</text>
  <text x="414" y="503" text-anchor="middle" font-family="sans-serif" font-size="13">⚡</text>
  <text x="414" y="520" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="11" font-weight="700" fill="#ffdd77">Generator</text>
</g>

<path d="M482 498 L568 498" stroke="#c9a84c" stroke-width="2.5" marker-end="url(#arrGold)" fill="none"/>
<circle r="3.5" fill="#e8c96d" opacity="0.9">
  <animateMotion dur="1.5s" repeatCount="indefinite" begin="0.5s">
    <mpath href="#p7"/>
  </animateMotion>
</circle>

<!-- NODE 7: HALLUCINATION GUARD -->
<g class="nGuard" filter="url(#softDrop)">
  <rect x="570" y="458" width="168" height="76" rx="28" fill="url(#gGuard)" stroke="#8844cc" stroke-width="2"/>
  <rect x="570" y="458" width="168" height="76" rx="28" fill="none" stroke="#c9a84c" stroke-width="0.8" opacity="0.6"/>
  <text x="654" y="475" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#c9a84c" letter-spacing="1">NODE 07 · LLM-AS-JUDGE</text>
  <text x="654" y="491" text-anchor="middle" font-family="sans-serif" font-size="13">🛡️</text>
  <text x="654" y="507" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="11" font-weight="700" fill="#cc99ff">HallucinationGuard</text>
  <text x="654" y="522" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8.5" fill="#bb88ee">same model · adversarial prompt</text>
  <text x="654" y="534" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#9966cc">Hallucinated → Fallback</text>
</g>

<!-- LLM-as-Judge annotation -->
<rect x="578" y="430" width="152" height="22" rx="5" fill="#0e0818" stroke="#c9a84c44" stroke-width="1"/>
<text x="654" y="442" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#e8c96d">⚖ Qwen 2.5 72B · Role Separation</text>
<text x="654" y="453" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="7.5" fill="#bbaa66">Generator vs Fact-Checker</text>

<path d="M738 496 L828 496" stroke="#c9a84c" stroke-width="2.5" marker-end="url(#arrGold)" fill="none"/>
<circle r="3.5" fill="#e8c96d" opacity="0.9">
  <animateMotion dur="1.4s" repeatCount="indefinite" begin="0.8s">
    <mpath href="#p8"/>
  </animateMotion>
</circle>

<!-- NODE 8: POSTPROCESS -->
<g class="nPost" filter="url(#softDrop)">
  <rect x="830" y="470" width="134" height="58" rx="29" fill="url(#gPost)" stroke="#228855" stroke-width="1.8"/>
  <text x="897" y="487" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#c9a84c" letter-spacing="1">NODE 08</text>
  <text x="897" y="503" text-anchor="middle" font-family="sans-serif" font-size="13">✅</text>
  <text x="897" y="520" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="11" font-weight="700" fill="#66ffaa">PostProcess</text>
</g>

<path d="M964 499 L998 499" stroke="#c9a84c" stroke-width="2" marker-end="url(#arrGold)" fill="none"/>
<g filter="url(#goldGlow)">
  <rect x="1000" y="488" width="44" height="22" rx="11" fill="#1a1200" stroke="#c9a84c" stroke-width="1.5"/>
  <text x="1022" y="503" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="9" font-weight="700" fill="#e8c96d">END</text>
</g>

<!-- Fallback annotation -->
<line x1="654" y1="534" x2="654" y2="558" stroke="#cc444466" stroke-width="1" stroke-dasharray="3 3"/>
<rect x="596" y="558" width="116" height="18" rx="5" fill="#1a0808" stroke="#cc4444" stroke-width="1"/>
<text x="654" y="571" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8.5" font-weight="600" fill="#ff9999">FALLBACK · null · never fabricates</text>

<!-- ══ INFRASTRUCTURE ══ -->
<!-- Pinecone -->
<g transform="translate(46,598)">
  <ellipse cx="60" cy="14" rx="46" ry="12" fill="#0d1f3a" stroke="#4488cc" stroke-width="1.5"/>
  <rect x="14" y="14" width="92" height="44" fill="url(#dbPinecone)" stroke="#3366aa" stroke-width="1.5"/>
  <ellipse cx="60" cy="58" rx="46" ry="12" fill="#0a1828" stroke="#3366aa" stroke-width="1.5"/>
  <ellipse cx="60" cy="14" rx="46" ry="12" fill="#1a3560" stroke="#5599dd" stroke-width="2"/>
  <text x="60" y="40" text-anchor="middle" font-family="sans-serif" font-size="11">🌲</text>
  <text x="60" y="54" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="9" font-weight="700" fill="#88bbff">Pinecone</text>
  <text x="60" y="74" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#aaccff">3,854 · MRL 256d</text>
</g>

<!-- Supabase -->
<g transform="translate(196,598)">
  <ellipse cx="60" cy="14" rx="46" ry="12" fill="#0a2010" stroke="#33aa66" stroke-width="1.5"/>
  <rect x="14" y="14" width="92" height="44" fill="url(#dbSupabase)" stroke="#228844" stroke-width="1.5"/>
  <ellipse cx="60" cy="58" rx="46" ry="12" fill="#081808" stroke="#228844" stroke-width="1.5"/>
  <ellipse cx="60" cy="14" rx="46" ry="12" fill="#154030" stroke="#44bb77" stroke-width="2"/>
  <text x="60" y="40" text-anchor="middle" font-family="sans-serif" font-size="11">⚡</text>
  <text x="60" y="54" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="9" font-weight="700" fill="#66dd99">Supabase</text>
  <text x="60" y="74" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#88eebb">SHA-256 · Parent Chunks</text>
</g>

<!-- MongoDB -->
<g transform="translate(346,598)">
  <ellipse cx="60" cy="14" rx="46" ry="12" fill="#081008" stroke="#33aa44" stroke-width="1.5"/>
  <rect x="14" y="14" width="92" height="44" fill="url(#dbMongo)" stroke="#228833" stroke-width="1.5"/>
  <ellipse cx="60" cy="58" rx="46" ry="12" fill="#060e06" stroke="#228833" stroke-width="1.5"/>
  <ellipse cx="60" cy="14" rx="46" ry="12" fill="#103018" stroke="#44bb55" stroke-width="2"/>
  <text x="60" y="40" text-anchor="middle" font-family="sans-serif" font-size="11">🍃</text>
  <text x="60" y="54" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="9" font-weight="700" fill="#66dd88">MongoDB</text>
  <text x="60" y="74" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#88eebb">Chat History · 30d TTL</text>
</g>

<!-- Redis -->
<g transform="translate(496,598)">
  <ellipse cx="60" cy="14" rx="46" ry="12" fill="#200808" stroke="#cc4444" stroke-width="1.5"/>
  <rect x="14" y="14" width="92" height="44" fill="url(#dbRedis)" stroke="#aa3333" stroke-width="1.5"/>
  <ellipse cx="60" cy="58" rx="46" ry="12" fill="#180606" stroke="#aa3333" stroke-width="1.5"/>
  <ellipse cx="60" cy="14" rx="46" ry="12" fill="#401010" stroke="#ee5555" stroke-width="2"/>
  <text x="60" y="40" text-anchor="middle" font-family="sans-serif" font-size="11">🔴</text>
  <text x="60" y="54" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="9" font-weight="700" fill="#ff9999">Upstash Redis</text>
  <text x="60" y="74" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#ffbbbb">Cache · &lt;100ms</text>
</g>

<!-- Langfuse -->
<g transform="translate(646,598)">
  <ellipse cx="60" cy="14" rx="46" ry="12" fill="#140820" stroke="#8844bb" stroke-width="1.5"/>
  <rect x="14" y="14" width="92" height="44" fill="url(#dbLangfuse)" stroke="#6633aa" stroke-width="1.5"/>
  <ellipse cx="60" cy="58" rx="46" ry="12" fill="#0e0618" stroke="#6633aa" stroke-width="1.5"/>
  <ellipse cx="60" cy="14" rx="46" ry="12" fill="#281040" stroke="#aa55ee" stroke-width="2"/>
  <text x="60" y="40" text-anchor="middle" font-family="sans-serif" font-size="11">📊</text>
  <text x="60" y="54" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="9" font-weight="700" fill="#cc99ff">Langfuse</text>
  <text x="60" y="74" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#ddbbff">LLM Tracing</text>
</g>

<!-- DB connector lines -->
<line x1="106" y1="598" x2="120" y2="534" stroke="#c9a84c22" stroke-width="1" stroke-dasharray="3 4"/>
<line x1="256" y1="598" x2="414" y2="528" stroke="#c9a84c18" stroke-width="1" stroke-dasharray="3 4"/>
<line x1="406" y1="598" x2="897" y2="528" stroke="#c9a84c15" stroke-width="1" stroke-dasharray="3 4"/>
<line x1="556" y1="598" x2="654" y2="534" stroke="#c9a84c18" stroke-width="1" stroke-dasharray="3 4"/>
<line x1="706" y1="598" x2="897" y2="528" stroke="#c9a84c15" stroke-width="1" stroke-dasharray="3 4"/>

<!-- ══ RIGHT PANEL ══ -->
<g filter="url(#panelDrop)">
  <rect x="1000" y="82" width="256" height="600" rx="10" fill="url(#panelGrad)" stroke="#c9a84c30" stroke-width="1"/>
  <rect x="1000" y="82" width="256" height="2" rx="1" fill="url(#goldGrad)" opacity="0.6"/>
</g>

<text x="1128" y="108" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="9.5" font-weight="700" fill="#e8c96d" letter-spacing="2">SYSTEM METRICS</text>
<line x1="1014" y1="116" x2="1242" y2="116" stroke="#c9a84c30" stroke-width="1"/>

<g font-family="'Segoe UI',sans-serif">
  <text x="1018" y="136" font-size="8" fill="#aaaacc" letter-spacing="1" font-weight="600">RESPONSE LATENCY</text>
  <text x="1238" y="136" text-anchor="end" font-size="16" font-weight="300" fill="#e8c96d">&lt;300ms</text>
  <rect x="1018" y="140" width="208" height="3" rx="1.5" fill="#1a1a2a"/>
  <rect x="1018" y="140" width="150" height="3" rx="1.5" fill="#c9a84c" opacity="0.8"/>

  <text x="1018" y="162" font-size="8" fill="#aaaacc" letter-spacing="1" font-weight="600">CONFIDENCE GATE</text>
  <text x="1238" y="162" text-anchor="end" font-size="14" font-weight="300" fill="#ff9999">&lt;40% → FALLBACK</text>
  <rect x="1018" y="166" width="208" height="3" rx="1.5" fill="#1a1a2a"/>
  <rect x="1018" y="166" width="83" height="3" rx="1.5" fill="#cc4444" opacity="0.8"/>

  <text x="1018" y="188" font-size="8" fill="#aaaacc" letter-spacing="1" font-weight="600">LIVE VECTORS · MRL 256d</text>
  <text x="1238" y="188" text-anchor="end" font-size="16" font-weight="300" fill="#e8c96d">3,854</text>
  <rect x="1018" y="192" width="208" height="3" rx="1.5" fill="#1a1a2a"/>
  <rect x="1018" y="192" width="175" height="3" rx="1.5" fill="#c9a84c" opacity="0.7"/>

  <text x="1018" y="214" font-size="8" fill="#aaaacc" letter-spacing="1" font-weight="600">STORAGE SAVED · MRL</text>
  <text x="1238" y="214" text-anchor="end" font-size="16" font-weight="300" fill="#66ffaa">75%</text>
  <rect x="1018" y="218" width="208" height="3" rx="1.5" fill="#1a1a2a"/>
  <rect x="1018" y="218" width="156" height="3" rx="1.5" fill="#44cc88" opacity="0.7"/>

  <text x="1018" y="240" font-size="8" fill="#aaaacc" letter-spacing="1" font-weight="600">RAM CONSTRAINT</text>
  <text x="1238" y="240" text-anchor="end" font-size="16" font-weight="300" fill="#ff9999">512MB</text>
  <rect x="1018" y="244" width="208" height="3" rx="1.5" fill="#1a1a2a"/>
  <rect x="1018" y="244" width="115" height="3" rx="1.5" fill="#cc4444" opacity="0.7"/>

  <text x="1018" y="266" font-size="8" fill="#aaaacc" letter-spacing="1" font-weight="600">RAM FREED</text>
  <text x="1238" y="266" text-anchor="end" font-size="16" font-weight="300" fill="#e8c96d">900MB+</text>
  <rect x="1018" y="270" width="208" height="3" rx="1.5" fill="#1a1a2a"/>
  <rect x="1018" y="270" width="195" height="3" rx="1.5" fill="#c9a84c" opacity="0.7"/>

  <text x="1018" y="292" font-size="8" fill="#aaaacc" letter-spacing="1" font-weight="600">MONTHLY COST</text>
  <text x="1238" y="292" text-anchor="end" font-size="16" font-weight="300" fill="#66ffaa">$0</text>
  <rect x="1018" y="296" width="208" height="3" rx="1.5" fill="#1a1a2a"/>
  <rect x="1018" y="296" width="208" height="3" rx="1.5" fill="#44cc88" opacity="0.7"/>

  <text x="1018" y="318" font-size="8" fill="#aaaacc" letter-spacing="1" font-weight="600">ACCURACY RETAINED</text>
  <text x="1238" y="318" text-anchor="end" font-size="16" font-weight="300" fill="#66ffaa">~95%</text>
  <rect x="1018" y="322" width="208" height="3" rx="1.5" fill="#1a1a2a"/>
  <rect x="1018" y="322" width="198" height="3" rx="1.5" fill="#44cc88" opacity="0.6"/>
</g>

<line x1="1014" y1="336" x2="1242" y2="336" stroke="#c9a84c25" stroke-width="1"/>

<!-- 3-Layer Hallucination -->
<text x="1128" y="356" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8.5" font-weight="700" fill="#e8c96d" letter-spacing="1.5">3-LAYER TRUTH ENFORCEMENT</text>

<g font-family="'Segoe UI',sans-serif">
  <rect x="1014" y="364" width="228" height="42" rx="5" fill="#0c0c18" stroke="#c9a84c25" stroke-width="1"/>
  <text x="1028" y="380" font-size="8.5" font-weight="700" fill="#e8c96d">LAYER 1 · Confidence Gate</text>
  <text x="1028" y="396" font-size="8" fill="#ccccee">Cosine &lt;40% → Fallback. 0 LLM tokens.</text>

  <rect x="1014" y="412" width="228" height="42" rx="5" fill="#0c0c18" stroke="#c9a84c25" stroke-width="1"/>
  <text x="1028" y="428" font-size="8.5" font-weight="700" fill="#e8c96d">LAYER 2 · Strict System Prompt</text>
  <text x="1028" y="444" font-size="8" fill="#ccccee">MISSING INFO RULE · never invent figures</text>

  <rect x="1014" y="460" width="228" height="52" rx="5" fill="#0e0a18" stroke="#c9a84c40" stroke-width="1.2"/>
  <rect x="1014" y="460" width="228" height="2" rx="1" fill="url(#goldGrad)" opacity="0.4"/>
  <text x="1028" y="477" font-size="8.5" font-weight="700" fill="#e8c96d">LAYER 3 · LLM-as-Judge</text>
  <text x="1028" y="492" font-size="8" fill="#ccbbee">Qwen 2.5 72B · adversarial role</text>
  <text x="1028" y="506" font-size="8" fill="#bbaadd">Hallucinated → Fallback · always</text>
</g>

<line x1="1014" y1="520" x2="1242" y2="520" stroke="#c9a84c22" stroke-width="1"/>

<!-- Quote -->
<text x="1128" y="540" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#c9a84c" letter-spacing="1.5">PRECISION-FIRST PHILOSOPHY</text>
<text x="1128" y="558" text-anchor="middle" font-family="Georgia,serif" font-size="9.5" fill="#ccbb88" font-style="italic">"A Null Response is a success.</text>
<text x="1128" y="573" text-anchor="middle" font-family="Georgia,serif" font-size="9.5" fill="#ccbb88" font-style="italic">A Wrong Response is a disaster."</text>
<text x="1128" y="588" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#998866">— Ambuj Kumar Tripathi · AKT 2026</text>

<line x1="1014" y1="598" x2="1242" y2="598" stroke="#c9a84c22" stroke-width="1"/>

<!-- Tech stack -->
<text x="1128" y="616" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" font-weight="700" fill="#c9a84c" letter-spacing="1.5">TECH STACK</text>
<g font-family="'Segoe UI',sans-serif" font-size="8">
  <rect x="1014" y="624" width="72" height="16" rx="8" fill="#0e0e1a" stroke="#c9a84c44" stroke-width="1"/>
  <text x="1050" y="636" text-anchor="middle" fill="#ddcc88" font-weight="600">LangGraph</text>

  <rect x="1094" y="624" width="62" height="16" rx="8" fill="#0e0e1a" stroke="#c9a84c3a" stroke-width="1"/>
  <text x="1125" y="636" text-anchor="middle" fill="#ccbb77">Pinecone</text>

  <rect x="1164" y="624" width="76" height="16" rx="8" fill="#0e0e1a" stroke="#c9a84c30" stroke-width="1"/>
  <text x="1202" y="636" text-anchor="middle" fill="#bbaa66">Qwen 2.5 72B</text>

  <rect x="1014" y="648" width="74" height="16" rx="8" fill="#0e0e1a" stroke="#c9a84c30" stroke-width="1"/>
  <text x="1051" y="660" text-anchor="middle" fill="#bbaa66">LlamaParse</text>

  <rect x="1096" y="648" width="60" height="16" rx="8" fill="#0e0e1a" stroke="#c9a84c28" stroke-width="1"/>
  <text x="1126" y="660" text-anchor="middle" fill="#bbaa55">FastAPI</text>

  <rect x="1164" y="648" width="76" height="16" rx="8" fill="#0e0e1a" stroke="#c9a84c25" stroke-width="1"/>
  <text x="1202" y="660" text-anchor="middle" fill="#aaa044">Jina v3 MRL</text>

  <rect x="1014" y="672" width="64" height="16" rx="8" fill="#0e0e1a" stroke="#c9a84c22" stroke-width="1"/>
  <text x="1046" y="684" text-anchor="middle" fill="#aa9944">Langfuse</text>

  <rect x="1086" y="672" width="64" height="16" rx="8" fill="#0e0e1a" stroke="#c9a84c20" stroke-width="1"/>
  <text x="1118" y="684" text-anchor="middle" fill="#998833">pybreaker</text>

  <rect x="1158" y="672" width="84" height="16" rx="8" fill="#0e0e1a" stroke="#c9a84c18" stroke-width="1"/>
  <text x="1200" y="684" text-anchor="middle" fill="#887722">Google OAuth</text>
</g>

<!-- ══ 4 EXECUTION PATHS ══ -->
<rect x="28" y="705" width="960" height="72" rx="8" fill="#09091a" stroke="#c9a84c25" stroke-width="1"/>
<rect x="28" y="705" width="960" height="1.5" fill="url(#goldLine)" opacity="0.4"/>
<text x="48" y="721" font-family="'Segoe UI',sans-serif" font-size="8.5" font-weight="700" fill="#e8c96d" letter-spacing="2">4 CONDITIONAL EXECUTION PATHS</text>

<g font-family="'Segoe UI',sans-serif">
  <rect x="44" y="728" width="8" height="8" rx="2" fill="#cc4444"/>
  <text x="58" y="737" font-size="9" fill="#ff9999" font-weight="700">ABUSIVE</text>
  <text x="118" y="737" font-size="8.5" fill="#ddaaaa">Classifier → Reject → END · 0 LLM calls · not saved</text>

  <rect x="44" y="750" width="8" height="8" rx="2" fill="#44cc88"/>
  <text x="58" y="759" font-size="9" fill="#88ffcc" font-weight="700">GREETING</text>
  <text x="122" y="759" font-size="8.5" fill="#aaddcc">Classifier → Greet → PostProcess → END · No VectorDB · 1 LLM call</text>

  <rect x="490" y="728" width="8" height="8" rx="2" fill="#cc9944"/>
  <text x="504" y="737" font-size="9" fill="#ffdd88" font-weight="700">VAGUE</text>
  <text x="548" y="737" font-size="8.5" fill="#ddcc88">Classifier → CrossQuestioner ⟳ HUMAN-IN-THE-LOOP · max 2 rounds</text>

  <rect x="490" y="750" width="8" height="8" rx="2" fill="url(#goldGrad)"/>
  <text x="504" y="759" font-size="9" fill="#e8c96d" font-weight="700">RAG (FULL)</text>
  <text x="560" y="759" font-size="8.5" fill="#ccbb77">Classifier → PII Shield → Retriever → Generator → HallucinationGuard → PostProcess</text>
</g>

<!-- FOOTER -->
<rect x="0" y="800" width="1280" height="60" fill="#040408dd"/>
<rect x="0" y="800" width="1280" height="1" fill="url(#goldLine)" opacity="0.3"/>
<text x="640" y="822" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="9" fill="#aaaacc" letter-spacing="1">
  Ambuj Kumar Tripathi · GenAI Solution Architect · LLMOps · ambuj-portfolio-v2.netlify.app · github.com/Ambuj123-lab
</text>
<text x="640" y="842" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="8" fill="#8888aa" letter-spacing="0.5">
  LangGraph · Pinecone · Jina v3 MRL 256d · Qwen 2.5 72B · LlamaParse · FastAPI · MongoDB · Supabase · Langfuse · pybreaker · $0/month · 2026
</text>
<text x="1120" y="856" text-anchor="end" font-family="'Segoe UI',sans-serif" font-size="16" font-weight="700" fill="#e8c96d">**© 2026 Ambuj Kumar Tripathi**</text>

</svg>

</div>

---

## 🧠 The 8-Node Agentic RAG Pipeline

| Node | Purpose | Key Detail |
|------|---------|------------|
| **1. Classifier** | Intent detection | Categorizes: `abusive` · `greeting` · `vague` · `rag_query` |
| **2. Reject** | Safety guard | Blocks abusive queries with firm, non-engaging response |
| **3. Greet** | Efficiency bypass | Handles greetings **without** hitting vector DB (zero cost) |
| **4. CrossQuestioner** | HITL clarification | Asks clarifying questions for vague queries (max 2 rounds) |
| **5. Retriever** | Dual vector search | Searches **Core Brain** + **Temp User Uploads** in Pinecone with parent-chunk deduplication |
| **6. Generator** | LLM synthesis | OpenRouter (DeepSeek/Gemini) with Langfuse tracing + circuit breaker |
| **7. HallucinationGuard** | Answer verification | Validates answer is **grounded** in retrieved context chunks |
| **8. PostProcess** | Persistence | Saves to MongoDB chat history + Langfuse observability logging |

---

## 🔧 Tech Stack

<table>
<tr>
<td><b>Category</b></td>
<td><b>Technology</b></td>
<td><b>Purpose</b></td>
</tr>
<tr>
<td rowspan="3"><b>RAG Engine</b></td>
<td>LangGraph StateGraph</td>
<td>8-node autonomous state machine orchestration</td>
</tr>
<tr>
<td>Jina v3 (MRL)</td>
<td>Matryoshka Representation Learning embeddings</td>
</tr>
<tr>
<td>LlamaParse</td>
<td>LLM-native 3-tier document parsing</td>
</tr>
<tr>
<td rowspan="2"><b>Backend</b></td>
<td>FastAPI + Uvicorn</td>
<td>Async REST API with SSE streaming</td>
</tr>
<tr>
<td>Authlib + PyJWT</td>
<td>Google OAuth 2.0 + JWT session management</td>
</tr>
<tr>
<td><b>Frontend</b></td>
<td>React 19 + Vite</td>
<td>SPA with lazy loading, dark theme, real-time streaming UI</td>
</tr>
<tr>
<td rowspan="4"><b>Data Layer</b></td>
<td>Pinecone Serverless</td>
<td>3,854 vectors — core brain + ephemeral user uploads</td>
</tr>
<tr>
<td>Supabase (PostgreSQL)</td>
<td>Parent chunk storage + file registry</td>
</tr>
<tr>
<td>MongoDB (Motor)</td>
<td>Async chat history, feedback, user sessions</td>
</tr>
<tr>
<td>Upstash Redis</td>
<td>Semantic caching (<100ms) + rate limiting + analytics</td>
</tr>
<tr>
<td rowspan="3"><b>Reliability</b></td>
<td>Pybreaker</td>
<td>Circuit breaker pattern — 3 failures → auto-open → 30s reset</td>
</tr>
<tr>
<td>Langfuse</td>
<td>Distributed tracing — LLM latency, token usage, cost tracking</td>
</tr>
<tr>
<td>UptimeRobot</td>
<td>GET/HEAD health monitoring — zero cold starts</td>
</tr>
<tr>
<td><b>Deployment</b></td>
<td>Docker (Multi-stage) + Render</td>
<td>Frontend build → backend image → production serve</td>
</tr>
</table>

---

## 📊 Infrastructure Scale

| Metric | Value |
|--------|-------|
| **Total Chunks** | 3,854 (Financial Parser) |
| **Live Vectors** | 3,854 in Pinecone Serverless |
| **Documents Indexed** | 20+ Indian Government Acts & Financial Frameworks |
| **Parent Chunks** | Stored in Supabase for full-context retrieval |
| **Cache Latency** | <100ms (Upstash Redis semantic cache) |
| **Rate Limit** | 10 queries/min per user (Redis sliding window) |
| **Session TTL** | 24h auto-cleanup (MongoDB TTL indexes) |

---

## 📄 Documents Indexed

| Category | Documents |
|----------|-----------|
| **Financial** | Union Budget 2024-25, Finance Bill 2024-25, Income Tax Amendments |
| **Pension/PF** | EPF Scheme 1952, EPS Pension Scheme 1995, PMVVY, APY |
| **Banking** | RBI KYC Master Direction 2016, UPI Guidelines |
| **Legal** | Constitution of India, Consumer Protection Act |

---

## 🔐 Security Architecture

```
7-Layer Upload Security Framework
─────────────────────────────────
Layer 1 │ Frontend Gating     │ .pdf only, 10MB limit, accept='.pdf'
Layer 2 │ Magic Byte Verify   │ %PDF- header validation (anti-spoofing)
Layer 3 │ Rate Limiting       │ 5 uploads/day per user+IP (Redis)
Layer 4 │ SHA-256 Dedup       │ Content-hash prevents re-indexing identical files
Layer 5 │ Session Isolation   │ is_temporary: true — auto-deletes on logout
Layer 6 │ TTL Auto-Cleanup    │ MongoDB 24h TTL on chunks + temp_uploads
Layer 7 │ Auth Guard          │ JWT verification on every API endpoint
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- API Keys: OpenRouter, Pinecone, MongoDB, Supabase, Google OAuth

### Local Development

```bash
# Clone
git clone https://github.com/Ambuj123-lab/agentic-rag-financial-parser.git
cd agentic-rag-financial-parser

# Backend
python -m venv venv && venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env  # Fill in your API keys
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install && npm run dev
```

### Docker (Production)

```bash
docker build -t financial-parser .
docker run -p 8000:8000 --env-file .env financial-parser
```

---

## 📁 Project Structure

```
agentic-rag-financial-parser/
├── app/
│   ├── main.py              # FastAPI app + SPA serving + health check
│   ├── api/
│   │   ├── auth.py           # Google OAuth + JWT + dev-login
│   │   ├── oauth.py          # Authlib Google client config
│   │   └── upload.py         # 7-layer secure file upload
│   ├── core/
│   │   └── config.py         # Pydantic Settings (env vars)
│   ├── db/
│   │   ├── mongodb.py        # Async Motor client + indexes
│   │   ├── pinecone_client.py # Pinecone Serverless init
│   │   └── supabase_client.py # Supabase PostgreSQL client
│   └── rag/
│       ├── graph.py          # ⭐ 8-Node LangGraph StateGraph
│       ├── routes.py         # Chat endpoints + SSE streaming
│       ├── embedder.py       # Jina v3 MRL embeddings
│       └── chunker.py        # Markdown + recursive splitting
├── frontend/
│   ├── src/
│   │   ├── pages/            # Landing, Dashboard, Admin, AuthCallback
│   │   ├── context/          # AuthContext (JWT state)
│   │   └── api/              # Axios client with interceptors
│   └── vite.config.js        # Dev proxy + code splitting
├── Dockerfile                # Multi-stage: Node build → Python serve
├── requirements.txt          # Pinned Python dependencies
└── .dockerignore             # Minimal Docker context
```

---

## 🌐 Live Links

| Resource | URL |
|----------|-----|
| **🚀 Live Application** | [agentic-rag-financial-parser.onrender.com](https://agentic-rag-financial-parser.onrender.com) |
| **📖 RAG Documentation** | [ambuj-rag-docs.netlify.app](https://ambuj-rag-docs.netlify.app/) |
| **👤 Portfolio** | [ambuj-portfolio-v2.netlify.app](https://ambuj-portfolio-v2.netlify.app/) |
| **💻 Source Code** | [GitHub Repository](https://github.com/Ambuj123-lab/agentic-rag-financial-parser) |

---

## 👨‍💻 Author

**Ambuj Kumar Tripathi**
GenAI Engineer & RAG Systems Specialist | LLMOps

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/ambuj-kumar-tripathi/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/Ambuj123-lab)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-34A853?style=flat-square&logo=google-chrome&logoColor=white)](https://ambuj-portfolio-v2.netlify.app/)

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,16,18,20&height=100&section=footer" width="100%"/>

<sub>Built with 🧠 LangGraph • ⚡ FastAPI • ⚛️ React • 🔍 Pinecone • 🐘 Supabase • 🍃 MongoDB • 🔴 Redis</sub>

</div>
<parameter name="Complexity">7
