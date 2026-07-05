# UI_PATTERNS.md

# Evalora UI Patterns

Version 1.0

---

# Purpose

This document defines reusable UI patterns.

Components are the building blocks.

Patterns define how components work together.

AI agents should compose pages using these patterns.

Never invent a new page layout if an existing pattern already solves the problem.

---

# Pattern Philosophy

Pages are compositions.

Example

Jobs Page

=

Page Header

+

Toolbar

+

KPI Section

+

Data Table

+

Pagination

+

Drawer

Instead of designing every page,

assemble existing patterns.

---

# Pattern Catalog

The platform uses the following patterns.

Dashboard Pattern

CRUD Pattern

Master Detail Pattern

Wizard Pattern

Analytics Pattern

AI Report Pattern

Timeline Pattern

Settings Pattern

Knowledge Pattern

Candidate Profile Pattern

Interview Pattern

Evaluation Pattern

Search Pattern

Table Pattern

Card Grid Pattern

Activity Pattern

Empty State Pattern

Modal Pattern

Drawer Pattern

Upload Pattern

AI Assistant Pattern

Notification Pattern

Command Palette Pattern

---

# Dashboard Pattern

Purpose

Display high-level information.

Structure

Header

↓

KPIs

↓

Analytics

↓

Activity

↓

AI Insights

↓

Quick Actions

↓

Recent Items

Dashboard pages never begin with tables.

Examples

Recruitment Dashboard

Executive Dashboard

Learning Dashboard

Analytics Dashboard

---

# CRUD Pattern

Purpose

Manage collections of entities.

Examples

Jobs

Candidates

Employees

Departments

Knowledge

Structure

Header

↓

Toolbar

↓

Table/Grid

↓

Pagination

↓

Drawer

↓

Confirmation Dialog

Every CRUD page should feel identical.

---

# Master Detail Pattern

Purpose

Display overview and detailed information.

Examples

Candidate

Job

Interview

Knowledge Document

Layout

List

↓

Selection

↓

Detail Panel

Never open a new page unless necessary.

---

# Wizard Pattern

Purpose

Guide users through complex workflows.

Examples

Create Job

Generate Interview

Organization Setup

Assessment Creation

Structure

Progress Indicator

↓

Step

↓

Validation

↓

Next

↓

Review

↓

Finish

Never exceed five steps.

---

# Analytics Pattern

Purpose

Present trends and metrics.

Structure

Header

↓

KPIs

↓

Charts

↓

Breakdowns

↓

Detailed Table

↓

Export

Charts support filtering.

---

# AI Report Pattern

Purpose

Present explainable AI outputs.

Structure

Summary

↓

Confidence

↓

Explanation

↓

Evidence

↓

Recommendations

↓

Actions

Every AI report should be understandable by humans.

---

# Candidate Profile Pattern

Structure

Header

↓

Overview

↓

Resume

↓

Timeline

↓

Interviews

↓

Evaluations

↓

Documents

↓

Notes

↓

Activity

Every candidate page uses this structure.

---

# Interview Pattern

Structure

Interview Header

↓

Question Navigation

↓

Question Area

↓

Answer Area

↓

Timer

↓

Progress

↓

Finish

Distractions should be minimized.

---

# Evaluation Pattern

Structure

Overall Score

↓

Category Scores

↓

Strengths

↓

Weaknesses

↓

Evidence

↓

Recommendations

↓

Download Report

Never show only a score.

Always explain.

---

# Knowledge Pattern

Structure

Collections

↓

Documents

↓

Processing

↓

Search

↓

Preview

↓

Metadata

Knowledge is always searchable.

---

# Timeline Pattern

Structure

Time

↓

Event

↓

Actor

↓

Description

↓

Status

Events are ordered chronologically.

---

# Activity Pattern

Purpose

Display recent actions.

Examples

Interview Generated

Candidate Applied

Resume Parsed

Offer Sent

Keep concise.

---

# Search Pattern

Structure

Search Input

↓

Filters

↓

Results

↓

Pagination

↓

Saved Searches

Search should never block users.

---

# Table Pattern

Every table supports

Search

Sort

Filters

Pagination

Bulk Actions

Export

Column Toggle

Selection

Sticky Header

Hover State

Context Menu

Never build static tables.

---

# Card Grid Pattern

Use when visual browsing is preferable.

Examples

Templates

Marketplace

Knowledge Collections

Learning Paths

Cards should align consistently.

---

# Upload Pattern

Structure

Drag Area

↓

Selected Files

↓

Validation

↓

Progress

↓

Success

↓

Processing

↓

Completed

Support multiple uploads.

---

# Modal Pattern

Structure

Title

↓

Description

↓

Content

↓

Primary Action

↓

Secondary Action

↓

Close

Every destructive action requires confirmation.

---

# Drawer Pattern

Purpose

Quick editing.

Never navigate away.

Examples

Edit Candidate

Edit Job

Edit Department

Edit Knowledge

---

# Settings Pattern

Structure

Navigation

↓

Content

↓

Save

↓

Danger Zone

↓

Audit Log

Settings pages should feel calm.

---

# Notification Pattern

Types

Success

Info

Warning

Error

Notifications should never interrupt work unnecessarily.

---

# Command Palette Pattern

Purpose

Fast navigation.

Supports

Search

Actions

Navigation

Create

Recent

Keyboard Shortcut

Available globally.

---

# AI Assistant Pattern

Structure

Conversation

↓

Context

↓

Sources

↓

Suggestions

↓

Actions

Never hide citations.

---

# Pattern Selection Guide

Question:

Is this operational data?

Use

CRUD Pattern

Question:

Is this configuration?

Use

Settings Pattern

Question:

Is this multi-step?

Use

Wizard Pattern

Question:

Is this AI output?

Use

AI Report Pattern

Question:

Is this analytics?

Use

Analytics Pattern

Question:

Is this an entity profile?

Use

Master Detail Pattern

---

# AI Agent Rules

Never invent layouts.

Always compose pages from existing patterns.

If multiple patterns are required,

combine them rather than creating a new one.

Consistency is mandatory.

---

# Final Principle

Pages are compositions.

Patterns are reusable.

Components are implementation details.

Build with patterns,

not pages.
