# Product Detail Guide

This guide exists to prevent shallow PRDs that sound complete but collapse during design, development, or QA.

## 1. Product detail is not “more words”

A detailed PRD is not longer by accident. It is more specific in the places where ambiguity causes rework.

The most common weak spots are:
- entry point not defined
- role differences not defined
- fields listed but rules missing
- happy path described, edge path missing
- state names mentioned, transitions missing
- backend logic named, but not attached to user behavior

## 2. What must be explicit in product detail

### 2.1 Entry and trigger
- where the user enters
- what condition makes the module appear
- what upstream action leads here

### 2.2 Page and component structure
- visible modules
- component types
- required vs optional content
- ordering and priority

### 2.3 Action rules
- what can be clicked, edited, submitted, filtered, sorted, exported, deleted
- what validation happens before action succeeds
- what blocks action

### 2.4 State design
At minimum consider:
- empty state
- loading state
- success state
- failure state
- disabled state
- expired / unavailable state if relevant

### 2.5 Role and permission differences
Do not write one universal flow if roles differ.

### 2.6 Edge cases
Include abnormal inputs, repeated submission, missing permissions, stale data, deleted entities, and timeout or async delay if relevant.

## 3. A useful test
If QA can derive test cases directly from the PRD, the detail level is usually good enough.
