# Prompt Engineering Basics

## What is a prompt?

A prompt is the input you give to a language model to get a useful output. It
usually combines an instruction, some context, and sometimes examples of the
desired output format. The quality of a prompt has a huge effect on the
quality of the model's response — this is why "prompt engineering" became its
own skill.

## System prompts vs user prompts

Most chat-based models accept two kinds of messages: a system prompt and user
messages. The system prompt sets the model's persona, tone, and rules for the
entire conversation — for example, "You are a patient AI tutor who explains
things with analogies." User messages are the actual questions or requests.
Separating these lets you keep behaviour consistent across many different
user inputs.

## Few-shot prompting

Few-shot prompting means including a small number of example input/output
pairs directly in the prompt before asking the real question. This helps the
model understand the exact format or style you want, especially for tasks like
classification, structured data extraction, or following a specific template.
Zero-shot prompting, by contrast, gives the model no examples at all and relies
on the instruction alone.

## Chain-of-thought prompting

Chain-of-thought prompting asks the model to reason step by step before giving
a final answer, for example by adding "think through this step by step" to the
prompt. This tends to improve performance on tasks that involve multiple
reasoning steps, such as math problems or multi-part questions, because it
gives the model room to work through intermediate logic instead of jumping
straight to a conclusion.

## Common pitfalls

- **Vague instructions** lead to vague answers — be specific about format,
  length, and tone.
- **Overloading a single prompt** with too many unrelated tasks often reduces
  quality on each one. Splitting work into smaller, focused prompts (or tool
  calls) usually works better.
- **Forgetting constraints** like "only answer using the provided context" can
  cause the model to hallucinate information that sounds plausible but isn't
  actually true.
