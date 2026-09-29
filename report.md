# Project 1 Report: Intelligent Search Visualizer

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Selected Region:**`, `**Live Deployment URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information 
- **Name:** G Le
- **UID (netID):** gle3
- **UIN:** 665375271

---

## Section 1: Selected City Region
- **Selected Region:** Illinois, USA
---

## Section 2: Map Graph Configuration
- **Total Cities Configured:** 22
- **Total Connection Edges:** 70 directed edges representing 35 selected city pairs
- **Graph Fully Connected:** Yes

---

## Section 3: Local Verification & Search Algorithms
*Check the algorithms you successfully ran and verified on your local development server by placing an `x` in the brackets (e.g., `[x]`):*
- [x] Breadth-First Search (BFS)
- [x] Depth-First Search (DFS)
- [x] Uniform Cost Search (UCS)
- [x] Iterative Deepening Search (IDS)
- [x] Greedy Best-First Search (Greedy)
- [x] A* Search (A*)

---

## Section 4: Deployed and Presentation Information
- **Deployment Platform:** Render
- **Live Deployment URL:** https://cs411-artificial-intelligence-project-1.onrender.com
- **Video Presentation Link:** https://youtu.be/nqfbGLrbDUY

---

## Section 5: Discussion
- **Which search algorithm is best for this route finding problem?** 
    A* because it minimizes the stored road distance and the consistent heuristic meets the implementation requirements. The way is by taking both the accumulated cost and an estimation of the remaining left over distance to the destination. It will always find the lowest cost route with the consistent heuristic.
- **Search Efficiency (Nodes expanded/time taken comparison):**
  In the Greedy & A* records 3 entries from Chicago to Aurora while against the DFS at 8, BFS at 10, UCS at 11 and IDS at 17. It the same result of the 67.76 km route as UCS but with less exploration expanded. Also to note that DFS was the fastest but return the longest route to the destination.
- **Link the idea of search algorithm to today Generative AI.** 
    I think in today new era and generation with Generative AI such as connecting it with like google maps etc. It often succeeds in it given tasks but often doesn't do it correctly such as the search algorithm we use such as A*. It will often be a BFS and DFS methods that are similar on google maps but there are so many xyz factors with the time, distance and more. 

