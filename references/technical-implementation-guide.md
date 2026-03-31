# Technical Implementation Guide for PRDs

This is not a substitute for a full technical design doc. It is the implementation-thinking layer that keeps a PRD grounded.

## 1. What the technical section should do

A useful technical section should help engineering answer:
- what needs to exist
- where logic should live
- how data moves
- what needs to be persisted
- what can fail
- how failures are observed and handled

A useless technical section sounds like this:
- 前后端联调
- 注意性能
- 做好监控

Those are labels, not implementation thinking.

## 2. The minimum technical dimensions

### 2.1 Frontend
- page or module boundaries
- local state vs server state
- form validation
- loading and error handling
- async result presentation

### 2.2 Backend
- service responsibilities
- sync vs async handling
- state transitions
- idempotency if users can retry
- permission checks

### 2.3 Data
- core entities
- key fields
- derived data
- persistence requirements
- audit or operation logs if relevant

### 2.4 API / integration
- input
- output
- failure codes or failure classes
- dependency on third-party systems

### 2.5 Stability and operations
- monitoring
- alerting
- fallback or degradation
- rollout strategy
- rollback strategy

## 3. When to include this section

Include explicit technical thinking when:
- the flow spans multiple systems
- state changes matter
- async jobs or retries matter
- roles and permissions matter
- data consistency matters
- launch risk is non-trivial

## 4. Output style

Write this section in plain product language. It should guide implementation, not imitate an RFC.
