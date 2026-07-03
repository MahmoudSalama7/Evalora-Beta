# AGENTS.md

# Evalora Engineering Handbook

Version: 1.0

---

# Purpose

This document is the primary source of truth for every AI coding agent working on Evalora.

Before making any code changes, every agent must read this document completely.

This document defines:

- Product vision
- Engineering principles
- UI principles
- Architecture
- Coding standards
- Naming conventions
- Folder organization
- Workflow rules
- AI implementation rules
- Design consistency rules

Every implementation must follow this document.

---

# About Evalora

Evalora is NOT an interview platform.

Evalora is NOT an ATS.

Evalora is NOT an assessment platform.

Evalora is an AI Workforce Intelligence Platform.

Its mission is to help organizations:

• Hire better
• Assess candidates objectively
• Reduce hiring time
• Improve hiring quality
• Develop employees
• Measure workforce capabilities
• Build stronger teams
• Make intelligent hiring decisions

Everything inside the platform must support this mission.

---

# Product Philosophy

Every feature must answer one of these questions:

Does it help companies hire better?

Does it reduce recruiter workload?

Does it improve candidate experience?

Does it improve hiring decisions?

Does it improve employee growth?

If the answer is no,

do not build it.

---

# Platform Philosophy

Evalora is built around reusable platform services.

Never build isolated features.

Everything should become reusable.

Example

GOOD

Knowledge Service

↓

Interview Generator

↓

HR Copilot

↓

Learning Assistant

↓

Employee Assistant

↓

Organization Search

BAD

Interview RAG

Resume RAG

Learning RAG

Policy RAG

Every AI capability should become a shared platform service.

---

# Design Philosophy

The platform should feel like

Linear

Stripe Dashboard

Ashby

Rippling

Vercel

Ramp

Notion

Never imitate consumer applications.

Never imitate gaming interfaces.

Never imitate crypto dashboards.

The product is Enterprise SaaS.

The interface should communicate

Professionalism

Clarity

Confidence

Efficiency

Trust

---

# Product Modules

The platform contains these modules.

Recruitment

ATS

Knowledge Base

Interview

Assessment

Evaluation

Learning

Workforce Intelligence

Analytics

Marketplace

Billing

Settings

Every new feature must belong to one existing module.

Do not create random standalone modules.

---

# Engineering Principles

Always prefer

Simple Architecture

Reusable Components

Reusable Services

Reusable Hooks

Reusable Utilities

Small Functions

Single Responsibility

Dependency Injection

Composition over inheritance

Feature-based organization

Never duplicate logic.

---

# Architecture

The project follows Clean Architecture.

Presentation Layer

↓

Application Layer

↓

Domain Layer

↓

Infrastructure Layer

Business logic never belongs inside UI.

React components should never contain business logic.

Controllers should never contain business logic.

Business logic belongs inside services.

---

# Feature Rule

Every feature must satisfy:

Can this feature be reused elsewhere?

If no,

redesign it.

Example

Instead of

InterviewDocumentUploader

Build

KnowledgeUploader

---

Instead of

InterviewEmbeddingService

Build

EmbeddingService

---

Instead of

InterviewRetriever

Build

RetrievalService

---

# AI Principles

Every AI capability must become a service.

Examples

Resume Parsing Service

Knowledge Service

Embedding Service

Retriever

Question Generator

Evaluation Engine

Recommendation Engine

Prompt Service

Never hardcode prompts inside components.

Never hardcode prompts inside services.

Store prompts separately.

---

# Knowledge Base Philosophy

Knowledge Base is a platform service.

It is NOT a chatbot.

It is NOT a document viewer.

It powers

Interview Generation

Candidate Evaluation

HR Copilot

Learning

Organization Search

Future AI Agents

Everything should use the same Knowledge Service.

---

# Workflow Rule

Never create isolated pages.

Every page belongs inside a workflow.

Example

GOOD

Create Job

↓

Upload Knowledge

↓

Configure Interview

↓

Generate Interview

↓

Candidate Interview

↓

Evaluation

↓

Hiring Decision

BAD

Knowledge Upload Page

Interview Generator Page

Random AI Page

Everything should connect.

---

# User Experience Principles

Users should always understand

Where they are

What they are doing

What happens next

Every page should have

Title

Description

Primary Action

Search

Filters

Main Content

AI Insight (optional)

Activity (optional)

No page should feel empty.

---

# Design Consistency

Never redesign navigation.

Never redesign spacing.

Never redesign layouts.

Use existing page templates.

Use existing components.

Use consistent interactions.

The product should feel like one application.

Not twenty different applications.

---

# Component Rule

Before creating a component

Search for an existing one.

If it exists

Reuse it.

If it almost exists

Extend it.

Only create a new component if absolutely necessary.

---

# Naming Rules

Use clear names.

GOOD

KnowledgeService

InterviewService

EvaluationEngine

CandidateProfile

RecruitmentDashboard

BAD

Helper

Utils2

MagicService

NewComponent

TempHook

---

# File Organization

Organize code by feature.

Example

modules/

recruitment/

interviews/

knowledge/

learning/

analytics/

Never organize by file type only.

---

# API Principles

Every endpoint must

Validate input

Return typed responses

Handle errors

Log failures

Return meaningful messages

Never expose internal exceptions.

---

# Database Rules

Every entity must have

id

createdAt

updatedAt

createdBy

when applicable.

Use UUIDs.

Never use business values as identifiers.

---

# Security Rules

Never trust client input.

Validate everything.

Sanitize uploaded files.

Limit upload size.

Validate MIME types.

Protect every endpoint.

Never expose secrets.

Never expose API keys.

Never commit credentials.

---

# AI Rules

Every AI request should support

Logging

Retries

Timeouts

Monitoring

Fallback

Token usage

Model configuration

Prompt versioning

Never directly call the LLM from UI.

---

# Error Handling

Every feature must support

Loading

Empty

Success

Error

Retry

Offline

Never leave users wondering.

---

# Accessibility

Support

Keyboard navigation

ARIA labels

Focus states

Screen readers

Proper contrast

Semantic HTML

Accessibility is required.

Not optional.

---

# Performance

Prefer

Lazy loading

Pagination

Virtualized tables

Memoization

Caching

Optimistic updates

Avoid unnecessary renders.

---

# Testing

Every feature should include

Unit Tests

Integration Tests

E2E Tests when applicable.

Never merge untested business logic.

---

# Logging

Log

Errors

AI requests

Failures

Processing

Knowledge ingestion

Interview generation

Evaluation

Logs should help debugging.

Not create noise.

---

# Documentation

Every major feature should update

WORKFLOWS.md

FEATURES.md

API.md

DATABASE.md

DECISIONS.md

Documentation is part of development.

Not an afterthought.

---

# Decision Making

Before implementing anything ask

Does this already exist?

Can this be reused?

Can another module benefit?

Is it scalable?

Is it simple?

Would Stripe build it this way?

If not

Redesign.

---

# Definition of Done

A feature is complete only if

✓ Integrated into workflow

✓ Uses shared services

✓ Uses shared components

✓ Responsive

✓ Accessible

✓ Error handled

✓ Loading states

✓ Empty states

✓ Typed

✓ Tested

✓ Logged

✓ Documented

✓ Production ready

Otherwise

The feature is NOT complete.

---

# Final Rule

Evalora is not a collection of pages.

Evalora is a platform.

Every line of code should make the platform stronger.

Whenever there are multiple implementation options,

choose the one that increases

reusability

maintainability

consistency

and long-term scalability.