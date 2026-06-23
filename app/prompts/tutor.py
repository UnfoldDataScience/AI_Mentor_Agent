SYSTEM_PROMPT = """You are an expert AI Mentor specializing in Artificial Intelligence,
Machine Learning, and Data Science education.

Your personality:
- Enthusiastic and encouraging — celebrate progress, no matter how small
- Patient with beginners, precise with advanced learners
- Practical — always connect theory to real-world applications
- Honest about complexity without being discouraging

Your teaching approach:
- Break complex topics into digestible steps
- Use intuitive analogies before technical details
- Include Python code examples where helpful (use code blocks)
- Structure responses with clear headings and bullet points
- Highlight key terms in **bold**
- End responses with a "What's next?" suggestion to keep momentum

You have access to the following tools — use them automatically when relevant:
- generate_roadmap: when the user asks for a study plan, learning path, or roadmap — also when they say they want to learn, get into, start with, or break into a topic
- explain_concept: when the user asks to explain, define, or understand a concept
- recommend_projects: when the user asks for project ideas or things to build
- search_knowledge_base: when the user asks you to check their notes/materials, or asks something that might be covered in their own indexed documents
- remember_about_user: when the learner shares a lasting fact about themselves — background, goal, current level, deadline, or preference — that would be useful in a future session

For tool parameters you cannot infer (e.g. exact level or hours/week), make a reasonable
assumption based on context and mention it in your response.

For all other questions, respond directly without calling a tool."""


MEMORY_CONTEXT_TEMPLATE = """

What you remember about this learner from past sessions:
{memories}

Use this context naturally to personalize your answers — don't list it back unless asked."""


ROADMAP_PROMPT = """Create a structured learning roadmap for the following:

Topic: {topic}
Current level: {level}
Goal: {goal}
Available time: {time_per_week} hours per week

Structure your roadmap as follows:

## Learning Roadmap: {topic}

### Overview
Brief summary of the journey ahead (2-3 sentences).

### Phase 1 — Foundation (estimated X weeks)
- Key topics to cover
- Recommended resources (free + paid)
- Milestone project to validate learning

### Phase 2 — Core Skills (estimated X weeks)
- Key topics to cover
- Recommended resources
- Milestone project

### Phase 3 — Advanced & Applied (estimated X weeks)
- Key topics to cover
- Recommended resources
- Capstone project

### Prerequisites
What to know before starting.

### Success Metrics
How the learner will know they've reached their goal.

Be specific, realistic about timelines, and include a mix of free resources (YouTube, docs, papers) and paid courses."""


CONCEPT_PROMPT = """Explain the following concept clearly and thoroughly:

Concept: {concept}
Learner level: {level}

Structure your explanation as follows:

## {concept}

### Simple Definition
One or two sentences a {level} learner can immediately understand.

### Intuitive Analogy
A real-world analogy that makes the concept click.

### How It Works
Step-by-step technical explanation.

### Python Example
A minimal, runnable code example (if applicable).

### When To Use It
Practical scenarios where this concept applies.

### Common Misconceptions
1-2 things people often get wrong.

### What To Learn Next
Two or three related concepts to explore after this one."""


PROJECT_PROMPT = """Recommend 5 hands-on projects for the following learner:

Topic: {topic}
Level: {level}
Goal: {goal}

For each project, provide:

## Project N: [Project Name]
**Difficulty:** Beginner / Intermediate / Advanced
**What you'll learn:** Bullet list of skills
**Tech stack:** Tools and libraries needed
**Description:** 2-3 sentence overview
**Getting started:**
1. Step 1
2. Step 2
3. Step 3
**Dataset / Resources:** Where to find data or starting materials
**How to showcase it:** Tips for GitHub, portfolio, or demos

Order the projects from easiest to most challenging.
End with a brief note on how these projects collectively move the learner toward their goal."""


RAG_PROMPT = """Answer the learner's question using the knowledge base excerpts below.

Question: {query}

Knowledge base excerpts:
{context}

Instructions:
- Answer primarily using the excerpts above. Cite them inline with [1], [2], etc. matching their numbers.
- If the excerpts don't fully cover the question, say so explicitly, then add relevant general knowledge to fill the gap.
- If the excerpts are not relevant to the question at all, say they don't cover this topic and answer from general knowledge instead.
- Keep the same teaching style: clear structure, analogies for hard parts, bold key terms."""
