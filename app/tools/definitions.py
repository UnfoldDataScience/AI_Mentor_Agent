TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "generate_roadmap",
            "description": (
                "Generate a structured, phase-by-phase learning roadmap. "
                "Call this when the user asks for a study plan, learning path, curriculum, or roadmap. "
                "Also call this when the user says they want to learn, get into, start with, or break into any AI/ML topic."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The AI/ML topic to learn",
                    },
                    "level": {
                        "type": "string",
                        "enum": ["Beginner", "Intermediate", "Advanced"],
                        "description": "The learner's current skill level",
                    },
                    "goal": {
                        "type": "string",
                        "description": "What the learner wants to achieve",
                    },
                    "time_per_week": {
                        "type": "integer",
                        "description": "Hours the learner can dedicate per week",
                    },
                },
                "required": ["topic", "level", "goal", "time_per_week"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "explain_concept",
            "description": (
                "Explain an AI/ML concept with definition, analogy, technical details, "
                "and a code example. Call this when the user asks to explain, define, "
                "or understand a specific concept or term."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "concept": {
                        "type": "string",
                        "description": "The AI/ML concept to explain",
                    },
                    "level": {
                        "type": "string",
                        "enum": ["Beginner", "Intermediate", "Advanced"],
                        "description": "The learner's level — determines depth of explanation",
                    },
                },
                "required": ["concept", "level"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_projects",
            "description": (
                "Recommend hands-on AI/ML projects ordered by difficulty. "
                "Call this when the user asks for project ideas, portfolio projects, "
                "practice exercises, or things to build."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The AI/ML topic area for the projects",
                    },
                    "level": {
                        "type": "string",
                        "enum": ["Beginner", "Intermediate", "Advanced"],
                        "description": "The learner's current level",
                    },
                    "goal": {
                        "type": "string",
                        "description": "What the learner wants to achieve with these projects",
                    },
                },
                "required": ["topic", "level", "goal"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": (
                "Search the learner's own knowledge base — their notes, cheat sheets, "
                "and course materials that have been indexed into this app. "
                "Call this when the user asks you to check their notes/materials, "
                "or asks a question that may be answered by their own indexed documents."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query — what information to look for in the knowledge base",
                    },
                },
                "required": ["query"],
            },
        },
    },
]
