# Sample Learning Roadmap: Natural Language Processing (NLP)

This is an example roadmap for a beginner who wants to get into NLP with
around 8-10 hours per week, aiming to build practical projects.

## Phase 1 — Foundations (3-4 weeks)

- **Python basics for text**: strings, regex, file I/O — enough to clean and
  process raw text.
- **Classic NLP concepts**: tokenization, stemming vs lemmatization,
  stopwords, bag-of-words, TF-IDF.
- **Milestone project**: a simple spam classifier using TF-IDF + logistic
  regression on a small dataset.

## Phase 2 — Word Representations and Embeddings (3-4 weeks)

- **Word embeddings**: Word2Vec, GloVe — what they are and why they're better
  than one-hot encoding for capturing meaning.
- **Sentence/document embeddings**: how short pieces of text get turned into
  vectors for similarity search (this connects directly to how this app's
  knowledge base retrieval works).
- **Milestone project**: build a simple semantic search tool over a small set
  of documents using embeddings + cosine similarity.

## Phase 3 — Transformers and Modern NLP (4-6 weeks)

- **Attention and transformers**: the core idea behind models like BERT and
  GPT — why attention lets models weigh which words matter most for a given
  task.
- **Pretrained models and fine-tuning**: using libraries like Hugging Face
  Transformers to apply pretrained models to your own data instead of training
  from scratch.
- **Milestone project**: fine-tune or apply a pretrained model for a task like
  sentiment analysis or text summarization.

## Phase 4 — Applied / LLM-era NLP (ongoing)

- **Prompting and tool use**: how to get useful behaviour out of large
  language models via prompting, few-shot examples, and structured outputs.
- **Retrieval-Augmented Generation (RAG)**: combining your own documents with
  an LLM so it can answer questions about content it wasn't trained on.
- **Capstone project**: an end-to-end app — e.g. a Q&A assistant over a
  personal document collection, similar in spirit to this AI Mentor's
  knowledge base feature.

## Success metrics

You'll know this roadmap is working when you can:
- Explain the difference between keyword search and semantic search to a
  beginner.
- Take a new dataset and produce a working baseline model within a day.
- Read a new NLP paper's abstract and place it within this roadmap (which
  phase/concepts it builds on).
