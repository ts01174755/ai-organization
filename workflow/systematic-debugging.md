# Systematic Debugging & Problem Resolution Workflow

## Overview
Methodical investigation and resolution of complex system issues through evidence-based debugging, data flow tracing, and rapid search capabilities.

## Core Debugging Team

### Primary Investigation Agent
**consolidated-fullstack-data-engineer**: Integrated debugging and development specialist
- Systematic root cause analysis with methodical debugging approaches
- Transforms vague symptoms into precise diagnoses through evidence-based investigation
- Handles complex issue isolation including "impossible to reproduce" problems
- Implements fixes with comprehensive testing and validation
- Provides end-to-end problem resolution from investigation to delivery

### Supporting Analysis Agents
**consolidated-fullstack-data-engineer**: Data pipeline analysis specialist
- Traces data movement and transformations through complex systems
- Maps data flow paths and identifies corruption/bottleneck points
- Analyzes data quality issues and pipeline performance problems

**consolidated-analysis-research-specialist** ⚡: Lightning-fast codebase search
- Semantic search with precision scoring
- Rapid pattern detection across massive codebases
- Multi-query decomposition with weighted results

## Debugging Workflow Phases

### Phase 1: Problem Definition & Symptom Analysis
1. **consolidated-fullstack-data-engineer**: Document exact symptoms vs expected behavior with systematic analysis
2. **consolidated-analysis-research-specialist**: Search for similar issues in codebase/logs with semantic search
3. **consolidated-fullstack-data-engineer**: Generate testable hypotheses with evidence-based reasoning

### Phase 2: Evidence Gathering
1. **consolidated-analysis-research-specialist**: Find relevant code patterns and error patterns across codebase
2. **consolidated-fullstack-data-engineer**: Trace data flow paths for data-related issues
3. **consolidated-fullstack-data-engineer**: Apply systematic logging and isolation techniques

### Phase 3: Hypothesis Testing
1. **consolidated-fullstack-data-engineer**: Design minimal test cases for each hypothesis with automated testing
2. **consolidated-fullstack-data-engineer**: Validate data transformations and pipeline integrity
3. **consolidated-fullstack-data-engineer**: Use binary search methodology to isolate root cause

### Phase 4: Root Cause Verification & Fix Implementation
1. **consolidated-fullstack-data-engineer**: Implement targeted fixes with comprehensive testing and validation
2. **consolidated-analysis-research-specialist**: Search for similar patterns that might have same issue
3. **consolidated-fullstack-data-engineer**: Verify fix resolves original symptoms with production-ready delivery

## Specialized Debugging Scenarios

### Performance Issues
- **juvenile-performance-cost-optimizer**: Identify performance bottlenecks with cost analysis
- **consolidated-fullstack-data-engineer**: Systematic performance profiling with optimization implementation
- **consolidated-analysis-research-specialist**: Find optimization patterns in codebase

### Intermittent/Race Condition Issues  
- **consolidated-fullstack-data-engineer**: Design reproducibility strategies with systematic debugging
- **consolidated-fullstack-data-engineer**: Analyze concurrent data flows and race conditions
- **consolidated-analysis-research-specialist**: Find synchronization patterns

### Data Corruption Problems
- **consolidated-fullstack-data-engineer**: Trace data pipeline from source to corruption point with quality analysis
- **consolidated-fullstack-data-engineer**: Validate data invariants and implement fixes at each stage
- **consolidated-analysis-research-specialist**: Find data validation patterns

### Legacy System Issues
- **consolidated-analysis-research-specialist**: Navigate large unfamiliar codebases rapidly
- **consolidated-fullstack-data-engineer**: Understand complex data system interactions
- **consolidated-fullstack-data-engineer**: Methodical analysis and modernization without assumptions

## Usage Examples

```bash
# Complex production issue investigation
task-orchestrator "App crashes intermittently during peak hours, can't reproduce locally" --workflow=systematic-debugging

# Data pipeline corruption analysis
task-orchestrator "Customer data getting corrupted somewhere in 8-stage ETL pipeline" --workflow=data-corruption-debug

# Performance bottleneck identification
task-orchestrator "System slow under load, multiple potential causes" --workflow=performance-debug

# Legacy system issue resolution
task-orchestrator "Critical bug in inherited 50K line monolith" --workflow=legacy-debug
```

## Debugging Principles

### Methodical Approach
- Never dismiss intermittent issues
- Use binary search for isolation
- Document all hypotheses and test results
- Verify fixes resolve original symptoms

### Evidence-Based Analysis
- Collect objective data before theorizing  
- Test assumptions with minimal cases
- Use strategic logging and instrumentation
- Validate data invariants at each stage

### Systematic Coverage
- Search entire codebase for similar patterns
- Trace complete data flow paths
- Consider compound causes and interactions
- Apply domain expertise contextually

## Success Metrics
- Root cause identification rate > 95%
- Average resolution time < 4 hours
- Zero recurring issues after fix
- Complete system understanding documentation