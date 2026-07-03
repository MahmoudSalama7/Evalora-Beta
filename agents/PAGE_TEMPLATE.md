# PAGE_TEMPLATE.md

# Evalora Page Template

Version 1.0

---

# Purpose

This document defines the standard layout for every page inside Evalora.

Every page should feel like it belongs to the same application.

Users should never feel they navigated into another product.

Consistency is more important than creativity.

---

# Core Philosophy

Every page answers three questions immediately.

Where am I?

What can I do here?

What should I do next?

If a page does not answer those questions within the first few seconds,

the design is wrong.

---

# Global Layout

Every page follows this structure.

┌────────────────────────────────────────────────────────────┐
│ Top Navigation                                              │
├───────────────┬────────────────────────────────────────────┤
│               │                                            │
│               │                                            │
│ Sidebar       │ Main Content                               │
│               │                                            │
│               │                                            │
│               │                                            │
└───────────────┴────────────────────────────────────────────┘

The Sidebar is fixed.

The Top Navigation is sticky.

The content scrolls independently.

---

# Sidebar

The sidebar should never change between modules.

It always contains

Dashboard

Recruitment

Jobs

Candidates

Interviews

Assessments

Knowledge Base

Learning

Analytics

Marketplace

Billing

Settings

The active page should always be visible.

Support nested navigation.

Support collapsed mode.

Never redesign the sidebar.

---

# Top Navigation

Always contains

Organization Switcher

Search

AI Assistant

Notifications

Profile

Quick Actions

Never remove these items.

---

# Every Page Must Contain

Page Header

↓

Optional KPIs

↓

Toolbar

↓

Main Content

↓

Optional AI Insights

↓

Optional Activity Feed

---

# Page Header

Every page starts with a hero section.

It contains

Page Title

Short Description

Primary Action

Secondary Action (optional)

Breadcrumb

Example

Jobs

Manage your company's hiring opportunities.

[ Create Job ]

[ Import Jobs ]

Never place filters above the header.

---

# KPI Section

Only dashboard pages use KPIs.

Examples

Total Jobs

Active Candidates

Interviews Today

Hiring Velocity

Average Score

Time To Hire

Cards should have

Icon

Title

Value

Small Trend

Optional Description

Maximum

4-6 KPI cards.

---

# Toolbar

Every data page contains a toolbar.

Toolbar includes

Search

Filters

Sort

View Switch

Bulk Actions

Export

Never hide search.

---

# Search

Search should always be visible.

Support

Instant Search

Keyboard Shortcut

Recent Searches

Clear Button

Search Placeholder

Example

Search candidates...

Search jobs...

Search interviews...

---

# Filters

Filters should appear beside Search.

Examples

Department

Status

Date

Owner

Tags

Interview Type

Candidate Stage

Support

Reset

Save Filter

Multi Select

---

# Primary Action

Every page has exactly one primary action.

Examples

Create Job

Add Candidate

Start Interview

Upload Knowledge

Invite User

Never place multiple competing primary buttons.

---

# Secondary Actions

Examples

Import

Export

Duplicate

Archive

Delete

These should never compete visually with the primary action.

---

# Main Content

Main content depends on page type.

Supported layouts

Dashboard

Table

Kanban

Grid

Wizard

Analytics

Form

Timeline

Master Detail

Choose one.

Do not mix layouts unnecessarily.

---

# Tables

Tables are the default layout for management pages.

Every table supports

Sorting

Filtering

Pagination

Bulk Selection

Column Visibility

Sticky Header

Search

Row Actions

Hover State

Empty State

Loading State

Error State

---

# Cards

Cards should be reusable.

Card structure

Title

Subtitle

Content

Actions

Optional Footer

Never overload cards.

One responsibility per card.

---

# Forms

Every form follows

Section Title

↓

Description

↓

Fields

↓

Validation

↓

Actions

Never create long forms.

Split into logical sections.

---

# Multi-Step Wizards

Use for

Create Job

Organization Setup

Interview Creation

Assessment Creation

Wizard structure

Step 1

General Information

↓

Step 2

Knowledge Resources

↓

Step 3

Configuration

↓

Step 4

Review

↓

Publish

Show progress.

Allow previous step.

Never lose user data.

---

# Empty States

Every page requires one.

Examples

No Jobs Yet

Create your first job.

No Candidates

Import candidates or publish a job.

No Interviews

Generate your first interview.

Every empty state should explain

What happened

Why

Next action

---

# Loading States

Never show blank pages.

Use

Skeleton

Loading Cards

Loading Table

Loading Charts

Loading Buttons

---

# Error States

Every page supports

Retry

Report Error

Help Link

Technical Details (developer mode)

Never leave the user without recovery.

---

# Detail Pages

Every entity has a detail page.

Example

Candidate

Header

↓

Overview

↓

Tabs

↓

Activity

↓

Documents

↓

AI Insights

↓

History

Never place everything on one page.

Use tabs.

---

# Tabs

Tabs should represent categories.

Examples

Overview

Documents

Interviews

Evaluations

Notes

Timeline

Analytics

Do not exceed seven tabs.

---

# Right Side Panel

Optional.

Reserved for

AI Recommendations

Quick Actions

Recent Activity

Notifications

Knowledge References

Should never become wider than the content.

---

# AI Insight Cards

Every AI module uses a common card.

Structure

Title

Confidence

Summary

Explanation

Recommendation

Action Button

Support

Expand

Collapse

Copy

Feedback

---

# AI Confidence

Every AI result displays confidence.

Examples

High

Medium

Low

Never hide uncertainty.

---

# Activity Timeline

Used on detail pages.

Examples

Candidate Applied

Resume Parsed

Interview Generated

Interview Completed

Evaluation Finished

Offer Sent

Display

Time

User

Action

Status

---

# Analytics Pages

Structure

Header

↓

KPIs

↓

Charts

↓

Breakdowns

↓

Table

↓

Export

Charts should always support

Hover

Filters

Date Range

Export

---

# Dashboard Pages

Order

Hero

↓

KPIs

↓

Charts

↓

Recent Activity

↓

Tasks

↓

AI Insights

↓

Calendar

↓

Shortcuts

Never place tables above KPIs.

---

# Settings Pages

Left Navigation

↓

Settings Form

↓

Save Button

↓

Danger Zone

Always isolate destructive actions.

---

# Modal Rules

Every modal contains

Title

Description

Content

Primary Action

Secondary Action

Close Button

Escape Support

Outside Click

Never create fullscreen modals unless necessary.

---

# Notifications

Support

Success

Warning

Error

Information

Notifications disappear automatically.

Errors remain visible.

---

# Responsive Rules

Desktop First

Tablet Supported

Mobile Supported

Sidebar collapses automatically.

Tables become cards on mobile.

Never hide functionality.

---

# Accessibility

Keyboard Navigation

Focus States

ARIA Labels

Screen Reader Support

Semantic HTML

Proper Contrast

Accessibility is mandatory.

---

# Design Consistency Rules

Every page must reuse

Existing Header

Existing Toolbar

Existing Tables

Existing Cards

Existing Buttons

Existing Forms

Never redesign an existing pattern.

---

# AI Agent Rules

Before generating a page

Check whether a similar page already exists.

Reuse

Layout

Spacing

Components

Interactions

Do not invent a new layout.

---

# Final Checklist

Before considering a page complete

✓ Uses global layout

✓ Uses standard header

✓ Uses standard toolbar

✓ Uses existing components

✓ Uses existing spacing

✓ Has loading state

✓ Has empty state

✓ Has error state

✓ Has responsive layout

✓ Has accessibility support

✓ Uses AI cards correctly

✓ Uses reusable patterns

✓ Matches the rest of the application

If any item is missing,

the page is not complete.