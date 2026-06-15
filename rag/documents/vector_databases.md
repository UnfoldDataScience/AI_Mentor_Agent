# Vector Databases and Embeddings

## What is an embedding?

An embedding is a list of numbers (a vector) that represents the meaning of a
piece of text. Texts with similar meaning end up with vectors that are close
together in this number space, even if they use completely different words.
For example, "puppy" and "young dog" would have embeddings that are very close,
while "puppy" and "spreadsheet" would be far apart.

Embeddings are produced by a trained model. OpenAI's `text-embedding-3-small`
model, for instance, turns any piece of text into a vector of 1536 numbers.

## What is a vector database?

A vector database (or vector store) stores these embeddings alongside the
original text so they can be searched later. Instead of matching keywords like
a traditional search engine, it finds the stored items whose embeddings are
most *similar* to the embedding of a search query. This is called semantic
search, because it matches meaning rather than exact words.

Popular vector databases include Chroma, Pinecone, Weaviate, and FAISS. For
small projects, a simple in-memory list of vectors with cosine similarity is
often enough — there is no strict requirement to use a dedicated database.

## Cosine similarity

Cosine similarity measures the angle between two vectors rather than their
distance. A score of 1 means the vectors point in exactly the same direction
(very similar meaning), 0 means they are unrelated, and -1 means they point in
opposite directions. It is the most common similarity metric used for text
embeddings because it ignores differences in vector length and focuses purely
on direction, i.e. meaning.

## How retrieval works end to end

1. Split documents into smaller chunks (a paragraph or a few sentences each).
2. Generate an embedding for every chunk and store it.
3. When the user asks a question, generate an embedding for the question too.
4. Compare the question's embedding against every chunk's embedding using
   cosine similarity.
5. Return the top few chunks with the highest similarity scores as context.

This pipeline is the foundation of Retrieval-Augmented Generation (RAG):
retrieving relevant context and handing it to a language model so it can
answer using information it was never trained on.
