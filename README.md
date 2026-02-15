# Smart Investor Agent

An agent-based financial analysis system built using modular Python packaging, FastAPI, and containerized deployment workflows.

This project is structured to follow production-ready engineering practices including CI validation, Docker builds, and branch protection rules.

# Architecture Overview

The system consists of:

- Modular Python package (src/)

- FastAPI service layer

- Lock-based dependency management

- CI pipeline with test + Docker validation

- Containerized API image

# High-level flow:

User → FastAPI → Agent logic → Data retrieval + analysis → Response