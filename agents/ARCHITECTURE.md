# ARCHITECTURE.md

# Evalora System Architecture

Version: 1.0

---

# Overview

Evalora is built as a modular AI Workforce Intelligence Platform.

The platform follows the principles of

- Clean Architecture
- Modular Monolith (initially)
- Domain Driven Design
- Service Oriented Design
- Event Driven Workflows
- Shared Platform Services

Every feature must integrate into this architecture.

---

# High Level Architecture

                        Browser
                           │
                           ▼
                 Next.js Frontend
                           │
                           ▼
                     API Gateway
                           │
        ┌──────────────────┼────────────────────┐
        ▼                  ▼                    ▼
 Recruitment         Interview Module      Workforce Module
        │                  │                    │
        └──────────────┬───┴────────────────────┘
                       ▼
                 Shared Platform Services
                       │
 ┌────────────┬──────────────┬──────────────┬───────────────┐
 ▼            ▼              ▼              ▼
Knowledge   AI Engine     Notifications   Analytics
Service      Services       Service        Service
                       │
                       ▼
              PostgreSQL + Redis
                       │
                       ▼
                 Object Storage
                       │
                       ▼
                 Vector Database

---

# Architectural Principles

Every module must be

Independent

Reusable

Loosely Coupled

Highly Cohesive

Composable

Never tightly couple two features together.

Always communicate through services.

---

# Platform Layers

The application consists of four layers.

Presentation Layer

↓

Application Layer

↓

Domain Layer

↓

Infrastructure Layer

Business logic never belongs inside Presentation.

---

# Presentation Layer

Responsible for

Pages

Layouts

Components

Forms

Tables

Charts

Navigation

The Presentation Layer never contains business logic.

Its only responsibility is rendering data and handling user interaction.

---

# Application Layer

Contains

Use Cases

Commands

Queries

Application Services

Validation

Authorization

Workflow Orchestration

Example

Create Job

Upload Documents

Generate Interview

Evaluate Candidate

These belong here.

---

# Domain Layer

Contains

Entities

Business Rules

Policies

Aggregates

Repositories

Enums

Domain Events

The Domain Layer never depends on infrastructure.

---

# Infrastructure Layer

Contains

Database

Authentication

Email

Storage

Embeddings

LLMs

Queues

Redis

External APIs

This layer can change without affecting business logic.

---

# Feature Organization

Every feature lives inside its own module.

modules/

    recruitment/

    interviews/

    candidates/

    knowledge/

    workforce/

    learning/

    analytics/

    billing/

Shared functionality belongs inside

platform/

Never duplicate services.

---

# Shared Platform Services

The platform exposes reusable services.

Authentication Service

Authorization Service

Knowledge Service

Embedding Service

Prompt Service

Notification Service

Analytics Service

Logging Service

Storage Service

Search Service

Audit Service

Configuration Service

Every module consumes these services.

---

# Knowledge Service

The Knowledge Service is one of the core platform services.

Responsibilities

Upload documents

Extract text

Clean content

Chunk documents

Generate embeddings

Store vectors

Retrieve context

Manage citations

The Knowledge Service should never know anything about interviews.

It only manages knowledge.

---

# Interview Service

Responsibilities

Generate interviews

Manage interview sessions

Store responses

Manage questions

Track interview progress

The Interview Service depends on the Knowledge Service.

Never the opposite.

---

# Evaluation Service

Responsibilities

Evaluate answers

Generate scores

Generate explanations

Generate feedback

Produce reports

Uses

Knowledge Service

Prompt Service

LLM Service

Analytics Service

---

# AI Service Layer

Every AI capability becomes an isolated service.

Resume Parsing

Job Description Parsing

Question Generation

Evaluation

Summarization

Recommendation

Learning

Classification

No AI code should exist outside these services.

---

# Event Driven Workflow

Modules communicate through events.

Example

JobCreated

↓

KnowledgeProcessingStarted

↓

KnowledgeIndexed

↓

InterviewReady

↓

CandidateApplied

↓

InterviewCompleted

↓

EvaluationCompleted

↓

HiringDecisionCreated

This keeps modules independent.

---

# Create Job Workflow

Recruiter

↓

Create Job

↓

Upload Documents

↓

Documents Stored

↓

Knowledge Processing

↓

Embeddings Generated

↓

Knowledge Ready

↓

Configure Interview

↓

Publish

---

# Candidate Workflow

Candidate Applies

↓

Resume Parsing

↓

Matching

↓

Interview

↓

Evaluation

↓

Hiring Recommendation

↓

Offer

---

# Knowledge Processing Pipeline

Upload

↓

Virus Scan

↓

Text Extraction

↓

Cleaning

↓

Chunking

↓

Embedding Generation

↓

Store Vector

↓

Metadata Indexing

↓

Completed

Each step should be independently retryable.

---

# Interview Generation Pipeline

Job Description

+

Knowledge Retrieval

↓

Prompt Construction

↓

LLM

↓

Question Validation

↓

Interview Generation

↓

Store Questions

Never generate questions without retrieval.

---

# Evaluation Pipeline

Candidate Answer

↓

Retrieve Context

↓

Prompt Construction

↓

LLM Evaluation

↓

Score Calculation

↓

Feedback

↓

Store Report

Every evaluation must reference retrieved knowledge.

---

# Data Ownership

Company

owns

Departments

Teams

Jobs

Candidates

Knowledge

Interviews

Reports

Everything belongs to an Organization.

No global business data.

---

# Storage

Structured Data

↓

PostgreSQL

Temporary Data

↓

Redis

Documents

↓

Object Storage

Vectors

↓

Vector Database

Logs

↓

Logging Platform

Never mix responsibilities.

---

# Security Principles

Every endpoint requires authentication.

Every action requires authorization.

Every upload must be validated.

Every AI request should be logged.

Every document should have ownership.

Every organization is isolated.

No organization can access another organization's data.

---

# Dependency Rules

Allowed

Presentation

↓

Application

↓

Domain

↓

Infrastructure

Forbidden

Infrastructure

↓

Presentation

Domain

↓

Presentation

Feature

↓

Feature

Features communicate through platform services.

---

# Scalability

Initially

Modular Monolith

Future

Microservices

Because modules are isolated,

they can be extracted without major refactoring.

---

# Error Handling

Every service returns

Success

Failure

Validation Error

Authorization Error

Unexpected Error

Never throw raw exceptions to the client.

---

# Observability

Every service should expose

Logs

Metrics

Tracing

Latency

AI Token Usage

Request IDs

Document Processing Time

Interview Duration

Evaluation Duration

---

# Performance

Use

Caching

Pagination

Lazy Loading

Background Jobs

Queue Processing

Optimistic UI

Streaming where applicable

Heavy AI tasks should never block user requests.

---

# AI Design Principles

Every AI feature should support

Model Switching

Prompt Versioning

Fallback Models

Retry Strategy

Token Tracking

Evaluation

Monitoring

Never hardcode providers.

Support multiple LLM providers.

---

# Future Architecture

Future AI agents should consume the same platform services.

Recruiter Agent

Hiring Agent

Learning Agent

Employee Assistant

HR Copilot

Executive Copilot

Career Coach

They should not create duplicate implementations.

Everything should reuse the platform architecture.

---

# Architecture Goal

Evalora should evolve by adding new modules,

not by rewriting existing ones.

Every architectural decision should increase

Reusability

Scalability

Maintainability

Consistency

Developer Productivity

Long-Term Flexibility

Architecture should make future development easier,

not harder.