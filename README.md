# DocMind
🚀 AI-powered Multi-Agent RAG system for intelligent document querying with fact verification

💡 Key Features:
✅ Multi-Agent System – A Research Agent generates answers, while a Verification Agent fact-checks responses.
✅ Hybrid Retrieval – Uses BM25 and vector search to find the most relevant content.
✅ Handles Multiple Documents – Selects the most relevant document even when multiple files are uploaded.
✅ Scope Detection – Prevents hallucinations by rejecting irrelevant queries.
✅ Fact Verification – Ensures responses are accurate before presenting them to the user.
✅ Web Interface with Gradio – Allowing seamless document upload and question-answering.

A Naïve RAG (Retrieval-Augmented Generation) pipeline is often insufficient for handling long, structured documents due to several limitations:

Limited query understanding: Naïve RAG processes queries at a single level, failing to break down complex questions into multiple reasoning steps. This results in shallow or incomplete answers when dealing with multi-faceted queries.

No hallucination detection or error handling: Traditional RAG pipelines lack a verification step. This means that if a response contains hallucinated or incorrect information, there's no mechanism to detect, correct, or refine the output.

Inability to handle out-of-scope queries: Without a proper scope-checking mechanism, Naïve RAG may attempt to generate answers even when no relevant information exists, leading to misleading or fabricated responses.

Inefficient multi-document retrieval: When multiple documents are uploaded, a Naïve RAG system might retrieve irrelevant or suboptimal passages, failing to select the most relevant content dynamically.

To overcome these challenges, DocChat implements a multi-agent RAG research system, which introduces intelligent agents to enhance retrieval, reasoning, and verification.

How multi-agent RAG solves these issues
Scope checking & routing
A Scope-Checking Agent first determines whether the user's question is relevant to the uploaded documents. If the query is out of scope, DocChat explicitly informs the user instead of generating hallucinated responses.
Dynamic multi-step query processing
For complex queries, an Agent Workflow ensures that the question is broken into smaller sub-steps, retrieving the necessary information before synthesizing a complete response.
For example, if a question requires comparing two sections of a document, an agent-based approach recognizes this need, retrieves both parts separately, and constructs a comparative analysis in the final answer.
Hybrid retrieval for multi-document contexts
When multiple documents are uploaded, the Hybrid Retriever (BM25 + Vector Search) ensures that the most relevant document(s) are selected dynamically, improving accuracy over traditional retrieval pipelines.

Fact verification & self-correction
After an initial response is generated, a Verification Agent cross-checks the output against the retrieved documents.
If any contradictions or unsupported claims are found, the Self-Correction Mechanism refines the answer before presenting it to the user.
Shared global state for context awareness
The Agent Workflow maintains a shared state, allowing each step (retrieval, reasoning, verification) to reference previous interactions and refine responses dynamically.
This enables context-aware follow-up questions, ensuring that users can refine their queries without losing track of previous answers.



