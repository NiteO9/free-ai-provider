# free-ai-provider
---

# Telegram channel 

Stay updated with project announcements, releases, and development progress.

Official Telegram Channel:

https://t.me/tele_t
Free OpenAI-compatible AI provider for coding agents with streaming and tool calling support.

# ChatSmith OpenAI Provider

A lightweight OpenAI-compatible API provider that bridges ChatSmith models to the OpenAI Chat Completions interface.

The project allows applications designed for the OpenAI API to communicate with ChatSmith models without requiring modifications to the client. It focuses on compatibility with modern AI applications, coding agents, developer tools, and OpenAI-based SDKs.

---

## Overview

ChatSmith OpenAI Provider acts as a protocol translation layer between ChatSmith and the OpenAI Chat Completions API.

It converts incoming OpenAI requests into ChatSmith requests, processes the responses, and returns OpenAI-compatible responses while preserving features such as streaming, tool calling, and agent workflows.

The goal of the project is to provide a stable compatibility layer rather than simply exposing another chatbot endpoint.

---

# Features

| Feature | Status |
|----------|--------|
| OpenAI Chat Completions API | Supported |
| Streaming Responses (SSE) | Supported |
| Tool Calling | Supported |
| Multiple Tool Calls | Supported |
| Function Calling | Supported |
| Tool Choice | Supported |
| JSON Tool Extraction | Supported |
| Automatic JSON Repair | Supported |
| OpenAI Compatible Response Format | Supported |
| Conversation Context Handling | Supported |
| Session Management | Supported |
| Authentication Layer | Supported |
| Request Validation | Supported |
| Error Handling | Supported |
| Automatic Authentication Refresh | Supported |
| Stateless HTTP API | Supported |
| Low Dependency Design | Supported |
| Production Ready Architecture | Supported |
| Compatible with OpenAI SDKs | Supported |
| Compatible with Coding Agents | Supported |
| REST API | Supported |
| CORS Support | Supported |

---

# Supported Clients

The provider is designed to work with software that supports the OpenAI Chat Completions API.

Examples include:

- Claude Code
- Pi Coding Agent
- Continue
- Cline
- Roo Code
- Aider
- OpenCode
- OpenAI Python SDK
- OpenAI JavaScript SDK
- Any OpenAI-compatible client

---

# Architecture

```
                OpenAI Client
                       │
                       ▼
        ChatSmith OpenAI Provider
                       │
        Request Translation Layer
                       │
             Authentication Layer
                       │
           ChatSmith Backend API
                       │
        Response Translation Layer
                       │
                       ▼
                OpenAI Response
```

---

# Request Flow

1. Receive an OpenAI Chat Completions request.
2. Validate the request.
3. Authenticate with ChatSmith.
4. Convert the request into the ChatSmith format.
5. Send the request to the ChatSmith backend.
6. Receive the ChatSmith response.
7. Normalize the response.
8. Convert the response into the OpenAI format.
9. Return the final response to the client.

---

# Tool Calling

The provider supports OpenAI Function Calling / Tool Calling.

Supported capabilities include:

- Tool discovery
- Tool choice
- Single tool execution
- Multiple tool execution
- Tool call identifiers
- JSON argument extraction
- Tool call normalization
- OpenAI-compatible tool responses

---

# Streaming

The provider supports Server-Sent Events (SSE).

Streaming capabilities include:

- Incremental text generation
- Streaming tool calls
- OpenAI chunk format
- Proper finish reasons
- Streaming completion termination

---

# Compatibility

The project is designed to maximize compatibility with existing OpenAI-based tooling.

Supported API endpoints include:

```
GET  /health
GET  /v1/models
POST /v1/chat/completions
```

---

# Technologies

| Technology | Purpose |
|------------|---------|
| Python | Core implementation |
| Flask | HTTP server |
| Requests | Backend communication |
| JSON | Protocol translation |
| Server-Sent Events | Streaming |
| OpenAI Chat Completions API | Client compatibility |

---

# Design Goals

- OpenAI API compatibility
- Clean protocol translation
- Lightweight implementation
- Easy deployment
- Low memory usage
- Extensible architecture
- Reliable streaming
- Robust tool calling
- Production-oriented design
- Minimal external dependencies

---

# Use Cases

- AI Coding Agents
- Local AI Providers
- API Compatibility Layer
- OpenAI SDK Integration
- Custom AI Backends
- Development Tools
- AI IDE Integration
- Automation Systems
- Research Projects
- Experimental Model Gateways

---

# Project Structure

```
.
├── server.py
├── README.md
└── requirements.txt
```

---

# License

This project is provided as-is for educational, research, and interoperability purposes.
