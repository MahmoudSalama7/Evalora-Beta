# WORKFLOWS.md

# Evalora Workflow Documentation

Version 1.0

---

# Purpose

This document defines every user journey inside Evalora.

Every feature must belong to one workflow.

Never build standalone pages.

Never build isolated AI features.

Everything must connect to an existing workflow.

If a feature does not belong to a workflow,

it should not exist.

---

# Product Workflows

The platform contains the following workflows.

1. Organization Onboarding

2. Team Management

3. Recruitment

4. Candidate Management

5. Knowledge Management

6. Interview Management

7. Candidate Evaluation

8. Hiring Decision

9. Employee Onboarding

10. Learning

11. Workforce Intelligence

12. Analytics

13. Administration

14. Billing

Every workflow may reuse platform services.

---

##############################################################

ORGANIZATION ONBOARDING

##############################################################

Goal

Allow a company to create its workspace.

Flow

Landing Page

↓

Sign Up

↓

Email Verification

↓

Create Organization

↓

Choose Organization Name

↓

Upload Logo

↓

Invite Team Members

↓

Select Subscription

↓

Workspace Ready

Outcome

Organization created.

Owner assigned.

Workspace initialized.

---

##############################################################

TEAM MANAGEMENT

##############################################################

Goal

Allow organizations to collaborate.

Flow

Settings

↓

Users

↓

Invite Member

↓

Assign Role

↓

Email Invitation

↓

Accept Invitation

↓

Join Workspace

Supported Roles

Owner

Admin

Recruiter

Hiring Manager

Interviewer

HR

Viewer

---

##############################################################

RECRUITMENT

##############################################################

Goal

Create and manage hiring opportunities.

Flow

Recruitment Dashboard

↓

Create Job

↓

Job Information

↓

Upload Knowledge Resources

↓

Knowledge Processing

↓

Interview Configuration

↓

Review

↓

Publish Job

↓

Job Appears in Open Positions

Important

Every Job owns its own Knowledge Base.

Knowledge is isolated per job.

---

Create Job Details

Step 1

General Information

Fields

Job Title

Department

Employment Type

Location

Experience Level

Salary (Optional)

Job Description

Validation

Required fields must be completed.

Step cannot continue until valid.

---

Step 2

Knowledge Resources

Recruiter uploads

PDF

DOCX

Markdown

TXT

Engineering Docs

Security Docs

Architecture

Training Manuals

Coding Standards

Internal Documentation

Capabilities

Drag & Drop

Multiple Upload

Delete

Rename

Preview

Validation

Virus Scan

File Size

Supported Formats

---

Step 3

Knowledge Processing

Background Processing

Upload

↓

Extract Text

↓

Normalize

↓

Chunk

↓

Generate Embeddings

↓

Store Vectors

↓

Index Metadata

↓

Completed

UI

Show processing progress.

Allow recruiter to continue after processing completes.

---

Step 4

Interview Configuration

Fields

Interview Type

Difficulty

Question Count

Time Limit

Evaluation Categories

AI Instructions

Knowledge Collections

Generate Sample Questions

---

Step 5

Review

Display

Job Information

Knowledge Summary

Interview Summary

Estimated Processing

Recruiter confirms.

---

Step 6

Publish

Job becomes

Published

Draft

Archived

Private

Workflow complete.

---

##############################################################

CANDIDATE JOURNEY

##############################################################

Goal

Guide a candidate from application to hiring.

Flow

Candidate Visits Job

↓

Apply

↓

Resume Upload

↓

Resume Parsing

↓

Candidate Profile Created

↓

Recruiter Review

↓

Interview Invitation

↓

Interview

↓

Evaluation

↓

Decision

↓

Offer

↓

Accepted

↓

Employee

Every stage should be trackable.

---

##############################################################

RESUME PARSING

##############################################################

Candidate Uploads Resume

↓

Extract Text

↓

Extract Skills

↓

Extract Experience

↓

Extract Education

↓

Extract Projects

↓

Generate Candidate Profile

↓

Store Candidate

↓

Ready for Matching

Platform Service Used

Resume Parsing Service

---

##############################################################

KNOWLEDGE MANAGEMENT

##############################################################

Knowledge belongs to Jobs.

Flow

Job

↓

Knowledge

↓

Documents

↓

Processing

↓

Embeddings

↓

Search

↓

Ready

Knowledge never exists independently.

Future shared collections may be supported,

but the MVP is Job-scoped.

---

##############################################################

INTERVIEW GENERATION

##############################################################

Recruiter

↓

Generate Interview

↓

Read Job Description

↓

Retrieve Relevant Knowledge

↓

Construct Prompt

↓

Generate Questions

↓

Validate Questions

↓

Store Interview

↓

Ready

Question Sources

Job Description

Knowledge Base

Interview Template

Company Policies

Generated interview must always cite supporting knowledge internally.

---

##############################################################

INTERVIEW SESSION

##############################################################

Candidate Starts Interview

↓

Introduction

↓

Question 1

↓

Answer

↓

Next

↓

Question N

↓

Finish

↓

Submission

↓

Evaluation Queue

Progress should auto-save.

Session should survive browser refresh.

---

##############################################################

AI EVALUATION

##############################################################

Interview Submitted

↓

Retrieve Relevant Knowledge

↓

Construct Evaluation Prompt

↓

LLM Evaluation

↓

Category Scores

↓

Evidence Extraction

↓

Feedback

↓

Overall Recommendation

↓

Store Evaluation

Categories

Technical

Problem Solving

Communication

Architecture

Best Practices

Company Knowledge

Critical Thinking

Confidence

Never score without explanation.

---

##############################################################

HIRING DECISION

##############################################################

Recruiter Opens Candidate

↓

Review Resume

↓

Review Interview

↓

Review AI Evaluation

↓

Compare Candidates

↓

Decision

Reject

Shortlist

Offer

Hold

Hire

AI should recommend,

never decide.

---

##############################################################

EMPLOYEE ONBOARDING

##############################################################

Offer Accepted

↓

Employee Profile

↓

Assign Team

↓

Assign Manager

↓

Learning Path

↓

Onboarding Checklist

↓

Completed

Future Module

---

##############################################################

LEARNING

##############################################################

Employee

↓

Skill Assessment

↓

Gap Analysis

↓

Recommendations

↓

Courses

↓

Practice Interviews

↓

Progress Tracking

↓

Reassessment

Learning should integrate with hiring data.

---

##############################################################

WORKFORCE INTELLIGENCE

##############################################################

Executive Dashboard

↓

Organization Analytics

↓

Skill Distribution

↓

Hiring Trends

↓

Department Health

↓

Promotion Readiness

↓

Retention Prediction

↓

Executive Reports

Future AI modules consume this data.

---

##############################################################

NOTIFICATIONS

##############################################################

Events

Job Published

Candidate Applied

Interview Generated

Interview Completed

Evaluation Ready

Offer Accepted

Team Invitation

Notifications

Email

In-App

Future

Slack

Teams

Webhook

---

##############################################################

AUDIT LOG

##############################################################

Every important action should be logged.

Examples

Job Created

Knowledge Uploaded

Interview Generated

Candidate Evaluated

Role Changed

Settings Updated

Audit Logs cannot be modified.

---

##############################################################

ERROR RECOVERY

##############################################################

Every workflow supports

Retry

Resume

Cancel

Rollback (where applicable)

Never force the user to restart an entire workflow.

---

##############################################################

WORKFLOW DESIGN PRINCIPLES

##############################################################

Every workflow should

Reduce clicks.

Reduce cognitive load.

Prevent mistakes.

Auto-save progress.

Provide feedback.

Explain AI decisions.

Allow recovery.

Keep users informed.

---

##############################################################

AI AGENT RULES

##############################################################

Before implementing a feature,

identify which workflow it belongs to.

If none,

the feature is incorrectly designed.

Never create orphan pages.

Never create disconnected functionality.

Always extend an existing workflow.

---

# Final Principle

Users experience products through workflows,

not pages.

Optimize the journey,

not individual screens.

Every improvement should make the complete workflow faster, clearer, and more valuable.