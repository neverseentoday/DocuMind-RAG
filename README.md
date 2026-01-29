📚 Secure RAG-Based PDF Question Answering System

A secure, end-to-end Retrieval-Augmented Generation (RAG) application that allows authenticated users to upload PDF documents and ask natural-language questions based strictly on the document content. The system combines semantic search and local large language models to deliver accurate, context-aware, and privacy-preserving responses.

🚀 Features

1.Secure OTP-based user authentication

2.PDF upload and text extraction

3.Semantic chunking and vector embeddings

4.Fast similarity search using FAISS

5.Context-grounded answers using a local LLM (Ollama)

6.Multi-user data isolation and privacy

7.Simple, intuitive chat-based UI



🧠 How the RAG Pipeline Works (Simple Explanation)

1.User Authentication
Users authenticate using an OTP-based verification system before accessing protected features.

2.PDF Upload
Authenticated users upload PDFs. Text is extracted using PyMuPDF.

3.Text Cleaning & Chunking
Extracted text is cleaned and split into overlapping chunks to preserve context.

4.Embedding Generation
Each chunk is converted into a vector using Sentence-Transformers (MiniLM).

5.Vector Storage (FAISS)
Embeddings are stored in a FAISS vector index for fast semantic retrieval.

6.Query Processing
User queries are embedded and matched against stored vectors using similarity search.

7.Answer Generation
Retrieved chunks are passed to a local LLM (LLaMA 3 via Ollama) to generate accurate, document-grounded answers.


🔐 Authentication & Security

i.OTP-based authentication

ii.JWT-secured backend APIs

iii.Each user can access only their own documents and chat history

iv.Sensitive files, secrets, and vector indexes are excluded using .gitignore

v.Local LLM inference ensures no data leaves the system




📸 Screenshots
🔍 RAG-Based PDF Question Answering
<img width="1906" height="1031" alt="Screenshot 2026-01-24 055648" src="https://github.com/user-attachments/assets/8672dfb9-a606-47f7-9557-4c33452904c7" />
-based question answering using semantic search and LLM reasoning.

🔐 OTP Authentication on questions related to employees.
Demonstrates secure handling of incorrect or expired OTPs.
<img width="1912" height="934" alt="Screenshot 2026-01-30 012842" src="https://github.com/user-attachments/assets/404cad2b-e90a-4850-88e5-4509a7e48fa6" />

Invalid Attempt
<img width="781" height="391" alt="Screenshot 2026-01-24 055832" src="https://github.com/user-attachments/assets/16f76ba2-b446-4203-928f-2b8c3abcd2b3" />


✅ OTP Verification – Success
<img width="806" height="434" alt="Screenshot 2026-01-24 055914" src="https://github.com/user-attachments/assets/32a3ce0a-de4f-40b8-9a99-f125bc54ad42" />


🎯 Why This Project Matters

This project demonstrates:

1.Real-world RAG system design

2.Secure authentication & authorization

3.Efficient vector search

4.Local, privacy-preserving LLM integration

5.Production-ready backend architecture






