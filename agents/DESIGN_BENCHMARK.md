# DESIGN_BENCHMARK.md

# Evalora Design Language

Version 1.0

---

# Purpose

This document defines the visual identity of Evalora.

Every page, every component, every layout, every interaction, and every workflow must follow this design language.

This is the official design benchmark.

If a generated page looks significantly different from the benchmark, it is considered incorrect.

The goal is that users should feel like every page was designed by the same team.

Consistency is more valuable than visual creativity.

---

# Design Philosophy

Evalora is an Enterprise AI SaaS Platform.

The interface should communicate

Professionalism

Trust

Intelligence

Speed

Clarity

Modern engineering

Every design decision should reduce cognitive load.

The interface should disappear behind the user's work.

---

# Inspiration

The product should feel inspired by

Linear

Stripe Dashboard

Vercel

Notion

Ashby

Rippling

GitHub

Slack Admin

The product should NOT feel like

Crypto Dashboard

Gaming UI

Consumer Mobile App

Social Media

E-commerce Website

---

# Golden Reference

The current dashboard implementation is the visual benchmark.

Future pages should inherit

Spacing

Hierarchy

Typography

Navigation

Card Layout

Interaction Patterns

Information Density

Do not redesign existing visual language.

Extend it.

---

# Visual Hierarchy

Every page follows this hierarchy

Navigation

↓

Page Title

↓

Description

↓

Primary Action

↓

KPIs

↓

Toolbar

↓

Content

↓

AI Insights

↓

Activity

Users should immediately understand

Where they are

What this page does

What they should do next

---

# Navigation

Sidebar

Persistent

Fixed

Always visible on desktop

Supports collapse

Supports nested menus

Never redesign sidebar navigation.

---

Top Navigation

Sticky

Always visible

Contains

Organization

Search

AI Assistant

Notifications

Profile

Quick Actions

Every page uses the same navigation.

---

# Content Width

Content should never feel stretched.

Pages should have generous margins.

Whitespace is intentional.

Crowded interfaces reduce usability.

---

# Grid System

Use a 12-column responsive grid.

Dashboard cards align perfectly.

Cards should never appear randomly positioned.

Maintain consistent spacing between all elements.

---

# Spacing Philosophy

Spacing creates hierarchy.

Never rely on borders alone.

Whitespace separates ideas.

Whitespace improves readability.

Use consistent spacing throughout the application.

Never compress layouts to fit more information.

---

# Cards

Cards are the primary building block.

Every card should represent exactly one concept.

Examples

Candidate Card

Interview Card

Analytics Card

AI Insight Card

Knowledge Card

Learning Card

Cards should never contain unrelated information.

---

# Dashboard Composition

A dashboard is composed of

Header

↓

KPIs

↓

Primary Analytics

↓

Secondary Analytics

↓

Recent Activity

↓

AI Recommendations

↓

Quick Actions

Avoid placing large tables at the top.

The most important information should appear first.

---

# KPI Cards

Each KPI card contains

Metric

Label

Trend

Supporting Information

Optional Action

Avoid unnecessary decoration.

The value should remain the focal point.

---

# Tables

Tables are used for operational data.

Every table should support

Search

Sorting

Filtering

Pagination

Bulk Selection

Column Visibility

Responsive Layout

Empty State

Loading State

Error State

Never build static tables.

---

# Forms

Forms should be divided into logical sections.

Each section contains

Title

Description

Fields

Validation

Avoid overwhelming users with long forms.

Use multi-step workflows whenever appropriate.

---

# Wizard Experience

Complex workflows should always use a wizard.

Example

Create Job

↓

Job Information

↓

Knowledge Resources

↓

Interview Configuration

↓

Review

↓

Publish

Each step should have a clear objective.

Users should always know where they are.

---

# Buttons

One primary action per page.

Secondary actions should never compete visually.

Destructive actions should be clearly separated.

Avoid excessive buttons.

---

# Search Experience

Search should always be visible.

Support

Instant Search

Keyboard Shortcut

Recent Searches

Clear Button

Highlight Matching Results

Search is one of the primary navigation methods.

---

# Filters

Filters belong beside Search.

Never hide filters behind multiple clicks.

Support

Multi Select

Saved Filters

Reset

Date Range

Tags

Status

Owner

---

# AI Components

Every AI-generated result should follow a consistent structure.

Title

Confidence

Summary

Detailed Explanation

Recommended Action

Source References

Feedback Controls

Never present AI output without explanation.

---

# AI Transparency

Every AI recommendation should answer

Why?

Where did this information come from?

How confident is the model?

Can the user verify it?

AI should assist decision making,

not replace it.

---

# Detail Pages

Every detail page follows

Header

↓

Overview

↓

Tabs

↓

Timeline

↓

AI Insights

↓

Related Information

Users should never scroll through one extremely long page.

---

# Timeline

Timeline components should display

Time

Actor

Action

Status

Details

Timelines tell the story of an entity.

---

# Empty States

Every empty state should

Explain what happened.

Explain why.

Suggest the next action.

Never leave users confused.

---

# Loading States

Never display blank content.

Use skeleton loaders that resemble the final layout.

Users should immediately understand that content is loading.

---

# Error States

Every error state should include

Problem Description

Retry Action

Support Link

Technical Details (Developer Mode)

Users should never reach a dead end.

---

# Responsive Design

Desktop is the primary experience.

Tablet should preserve functionality.

Mobile should simplify layout without removing features.

Responsive design is adaptation,

not feature removal.

---

# Accessibility

Keyboard Navigation

Screen Reader Support

Focus Indicators

Semantic HTML

ARIA Labels

High Contrast Support

Accessibility is part of the design,

not an optional enhancement.

---

# Animation Principles

Animations should communicate state changes.

Examples

Loading

Expanding

Sorting

Filtering

Navigation

Avoid decorative animations.

Animation should improve understanding.

---

# Feedback

Every user action should receive immediate feedback.

Examples

Save

Delete

Upload

Generate Interview

Evaluate Candidate

Feedback should be clear and timely.

---

# Information Density

Enterprise users work with large amounts of data.

Display enough information to support decisions,

but avoid visual overload.

Group related information.

Progressively disclose advanced details.

---

# Design Consistency

Never introduce a new card style if one already exists.

Never create a new table style.

Never redesign existing buttons.

Never invent a new page layout.

Always reuse existing interaction patterns.

Consistency creates trust.

---

# AI Agent Design Rules

Before creating a new page

1. Search for an existing similar page.

2. Reuse existing layout.

3. Reuse existing components.

4. Reuse spacing.

5. Reuse typography hierarchy.

6. Extend existing patterns.

Never build from scratch unless no suitable pattern exists.

---

# Definition of Good Design

A page is considered complete when

It matches the design language.

It follows the page template.

It uses shared components.

It supports all states.

It feels consistent with every other page.

Users should immediately recognize it as part of Evalora.

If a page looks like it belongs to another application,

it must be redesigned.

---

# Final Principle

Design systems exist to eliminate unnecessary decisions.

When in doubt,

reuse.

When possible,

simplify.

When creating something new,

make sure it can become part of the design system.

Every new page should strengthen the platform's visual identity rather than fragment it.