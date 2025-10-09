---
title: Dive into automation: n8n learning path
date: 2025-10-09
uuid: 48b1
status: inbox
content-type: # article/video/thread/course
target-audience: # beginner/intermediate/advanced
categories: [category]
image:
  path: /assets/media/k8s/kubernetes-security-mistake.png
---

# 🚀 n8n Mastery Guide: From Basics to Best Practices

## Table of Contents

1. [Understanding n8n Data Flow](#1-understanding-n8n-data-flow)
2. [Workflow Management & Subflows](#2-workflow-management--subflows)
3. [Error Handling & Resilience](#3-error-handling--resilience)
4. [Thinking in Workflows](#4-thinking-in-workflows)
5. [Version Control Strategies](#5-version-control-strategies)

---

## 1. Understanding n8n Data Flow

### 📚 Official Docs

- [Data structure](https://docs.n8n.io/data/data-structure/)
- [Data transformation](https://docs.n8n.io/data/)

### Core Concepts

**n8n processes data in "items"**. Each item is an object with a `json` property:

```javascript
// Single item
{
  json: {
    name: "John",
    email: "john@example.com"
  }
}

// Multiple items (array)
[
  { json: { name: "John", email: "john@example.com" } },
  { json: { name: "Jane", email: "jane@example.com" } }
]
```

### Key Rules

1. **Node Input**: Each node receives an array of items
2. **Node Output**: Each node returns an array of items
3. **Accessing Data**: Use `$json` to access current item's data

### Practical Examples

#### Example 1: Simple Data Flow

```
[Manual Trigger] → [Code Node] → [HTTP Request]
```

**Code Node:**

```javascript
// Access previous node's data
const userName = $json.name;
const userEmail = $json.email;

// Return data for next node
return [
  {
    json: {
      fullName: userName,
      contact: userEmail,
      timestamp: new Date().toISOString(),
    },
  },
];
```

#### Example 2: Processing Multiple Items

```javascript
// When you have multiple items from previous node
const allItems = $input.all(); // Get all items as array

// Process each item
const processed = allItems.map((item) => ({
  json: {
    originalData: item.json,
    processed: true,
    processedAt: Date.now(),
  },
}));

return processed;
```

#### Example 3: Aggregating Data

```javascript
// Combine multiple items into one
const allItems = $input.all();

return [
  {
    json: {
      items: allItems.map((item) => item.json),
      count: allItems.length,
      summary: "Combined " + allItems.length + " items",
    },
  },
];
```

### 🎯 Quick Reference

| Expression          | Purpose            | Example                      |
| ------------------- | ------------------ | ---------------------------- |
| `$json`             | Current item data  | `$json.name`                 |
| `$input.first()`    | First item         | `$input.first().json`        |
| `$input.last()`     | Last item          | `$input.last().json`         |
| `$input.all()`      | All items          | `$input.all()`               |
| `$node["NodeName"]` | Specific node data | `$node["HTTP Request"].json` |

---

## 2. Workflow Management & Subflows

### 📚 Official Docs

- [Execute Workflow node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/)
- [Sub-workflows](https://docs.n8n.io/workflows/create-workflow/#sub-workflows)

### Pattern 1: Simple Subflow Call

**Main Workflow:**

```
[Trigger] → [Process Data] → [Execute Workflow: "Email Sender"] → [Log Result]
```

**Subworkflow ("Email Sender"):**

```
[When called by another workflow] → [Format Email] → [Send Email]
```

**Configuration:**

**Execute Workflow Node:**

- **Source**: Database
- **Workflow**: Select "Email Sender"
- Data automatically passes to subworkflow

**In Subworkflow - Access Parent Data:**

```javascript
// Get data from parent workflow
const parentData = $input.first().json;

// Access specific fields
const articles = parentData.articles;
const metadata = parentData.metadata;
```

### Pattern 2: Subflow with Return Value

**Main Workflow:**

```javascript
// Before calling subworkflow
return [
  {
    json: {
      operation: "processData",
      data: myData,
      config: { timeout: 5000 },
    },
  },
];
```

**Execute Workflow Node** → Returns subworkflow output

**After Execute Workflow:**

```javascript
// Access subworkflow result
const result = $json.result;
const status = $json.status;

console.log("Subworkflow returned:", result);
```

### Pattern 3: Conditional Subflow Execution

```
[Process] → [IF Node] → True: [Execute Workflow: "Success Handler"]
                      → False: [Execute Workflow: "Error Handler"]
```

**IF Node Condition:**

```javascript
{
  {
    $json.status === "success";
  }
}
```

### Pattern 4: Multiple Subflows in Sequence

```
[Data] → [Execute: "Validate"] → [Execute: "Process"] → [Execute: "Notify"]
```

Each subworkflow receives output from previous one.

### Pattern 5: Parallel Subflow Execution

```
                    → [Execute: "Process A"]
[Data] → [Split] →  → [Execute: "Process B"]  → [Merge] → [Combine Results]
                    → [Execute: "Process C"]
```

Use **Split In Batches** or **Item Lists** node.

### 🎯 Best Practices

✅ **DO:**

- Name subworkflows clearly: "Email - Send Digest", "Data - Validate Input"
- Keep subworkflows focused (single responsibility)
- Use descriptive node names
- Add notes to complex subworkflows

❌ **DON'T:**

- Create circular dependencies (A calls B, B calls A)
- Pass huge datasets (>1MB) between workflows
- Nest subworkflows more than 3 levels deep

---

## 3. Error Handling & Resilience

### 📚 Official Docs

- [Error handling](https://docs.n8n.io/workflows/error-handling/)
- [Error Workflow](https://docs.n8n.io/workflows/error-handling/#workflow-error-workflow)

### Strategy 1: Try-Catch Pattern with IF Node

```
[HTTP Request] → [IF: Check for Errors] → Success: [Continue]
                                         → Error: [Handle Error] → [Notify]
```

**IF Node Condition:**

```javascript
{
  {
    $json.error === undefined && $json.statusCode === 200;
  }
}
```

### Strategy 2: Built-in Error Handling

**On any node, click the gear icon → Settings:**

- **Continue On Fail**: ✅ (keeps workflow running)
- **Retry On Fail**: ✅
  - **Max Tries**: 3
  - **Wait Between Tries**: 1000ms (exponential backoff)

**Example: Resilient HTTP Request**

```
Settings:
- Continue On Fail: Yes
- Retry: 3 times
- Wait: 1000ms, 2000ms, 4000ms
```

### Strategy 3: Error Workflow (Global Handler)

**Create dedicated "Error Handler" workflow:**

```
[Error Trigger] → [Parse Error] → [Log to Database] → [Send Alert]
```

**Error Trigger Node:**

```javascript
// Access error details
const errorWorkflow = $json.workflow.name;
const errorNode = $json.node.name;
const errorMessage = $json.error.message;
const errorTime = $json.execution.startedAt;

return [
  {
    json: {
      workflow: errorWorkflow,
      node: errorNode,
      error: errorMessage,
      timestamp: errorTime,
      executionId: $json.execution.id,
    },
  },
];
```

**Set as Global Error Workflow:**

1. Go to Settings → Workflows
2. Set "Error Workflow" to your error handler

### Strategy 4: Defensive Coding

```javascript
// Always validate input
function processData(data) {
  // Validation
  if (!data || typeof data !== "object") {
    console.log("❌ Invalid data received");
    return { error: "Invalid input", success: false };
  }

  // Null checks
  const items = data.items || [];
  const config = data.config || {};

  // Try-catch for risky operations
  try {
    const result = riskyOperation(items);
    return { result, success: true };
  } catch (error) {
    console.log("❌ Error:", error.message);
    return { error: error.message, success: false };
  }
}

// Use it
const result = processData($json);

if (!result.success) {
  // Handle error path
  return [{ json: { status: "error", message: result.error } }];
}

// Continue with success path
return [{ json: { status: "success", data: result.result } }];
```

### Strategy 5: Circuit Breaker Pattern

```javascript
// Track failures
let failureCount = 0;
const MAX_FAILURES = 5;

// In your processing loop
try {
  const result = await externalService.call();
  failureCount = 0; // Reset on success
  return result;
} catch (error) {
  failureCount++;

  if (failureCount >= MAX_FAILURES) {
    console.log("🔴 Circuit breaker triggered - stopping workflow");
    throw new Error("Circuit breaker open: too many failures");
  }

  console.log(`⚠️ Failure ${failureCount}/${MAX_FAILURES}`);
  // Continue or retry
}
```

### 🎯 Resilience Checklist

- [ ] Enable "Continue On Fail" on external API calls
- [ ] Add retry logic with exponential backoff
- [ ] Validate all input data before processing
- [ ] Use try-catch blocks around risky operations
- [ ] Set up global error workflow for monitoring
- [ ] Add timeout limits on long-running operations
- [ ] Log errors with context (node name, input data)
- [ ] Send alerts for critical failures
- [ ] Test failure scenarios regularly

---

## 4. Thinking in Workflows

### 📚 Official Docs

- [Workflow best practices](https://docs.n8n.io/workflows/create-workflow/)
- [Building workflows](https://docs.n8n.io/workflows/)

### The Workflow Mindset

**Think in stages, not steps:**

❌ **Wrong Thinking:** "I need to make an API call, then parse the response, then..."

✅ **Right Thinking:** "I need to: 1) Get Data → 2) Transform → 3) Act → 4) Report"

### Pattern: Start Small, Grow Iteratively

#### Iteration 1: Basic Flow (Hardcoded)

```
[Manual Trigger] → [HTTP Request: Fixed URL] → [Show Result]
```

#### Iteration 2: Add Parameters

```
[Manual Trigger] → [Set Variables] → [HTTP Request: Use Variables] → [Show Result]
```

#### Iteration 3: Add Processing

```
[Trigger] → [Set Vars] → [HTTP Request] → [Filter Data] → [Transform] → [Show]
```

#### Iteration 4: Add Error Handling

```
[Trigger] → [Set] → [HTTP + Retry] → [IF: Success?] → Yes: [Process]
                                                      → No: [Log Error]
```

#### Iteration 5: Make Reusable

```
[Trigger] → [Validate Input] → [Execute Workflow: "API Handler"] → [Format Output]
```

### Decomposition Strategy

**Example: "Send Weekly Security Digest"**

**🔴 Bad Approach:** One massive workflow with 30 nodes

**🟢 Good Approach:** Decompose into logical units

```
Main Workflow: "Security Digest Orchestrator"
├── Subworkflow: "RSS - Fetch Articles"
├── Subworkflow: "AI - Generate Summary"
├── Subworkflow: "Email - Send Digest"
└── Subworkflow: "Slack - Post Notification"
```

Each subworkflow is:

- **Testable** independently
- **Reusable** in other workflows
- **Maintainable** (easier to update)
- **Understandable** (single purpose)

### Design Patterns

#### Pattern 1: Pipeline (Sequential Processing)

```
[Input] → [Validate] → [Transform] → [Enrich] → [Output]
```

**Use When:** Data flows linearly through transformations

#### Pattern 2: Branch (Conditional Logic)

```
[Input] → [Decision] → Path A: [Process A] → [Merge]
                     → Path B: [Process B] → [Merge]
```

**Use When:** Different handling based on conditions

#### Pattern 3: Map-Reduce (Batch Processing)

```
[Input] → [Split Items] → [Process Each] → [Aggregate] → [Output]
```

**Use When:** Processing lists of items

#### Pattern 4: Event-Driven (Trigger-Response)

```
[Webhook Trigger] → [Parse Event] → [Route by Type] → [Multiple Handlers]
```

**Use When:** Reacting to external events

#### Pattern 5: Scheduled Task (Time-Based)

```
[Cron Trigger] → [Fetch Data] → [Process] → [Report]
```

**Use When:** Regular automated tasks

### Workflow Organization Framework

**Use this naming convention:**

```
[Category] - [Purpose] - [Version]

Examples:
- Data - Fetch RSS Articles - v2
- Email - Send Digest - v1
- Integration - Slack Notify - v3
- Utility - Validate JSON - v1
```

**Folder Structure (in your mind/docs):**

```
Workflows/
├── Core/ (main business workflows)
│   ├── Security Digest Orchestrator
│   └── Weekly Report Generator
├── Integrations/ (external services)
│   ├── RSS - Fetch Articles
│   ├── Slack - Post Message
│   └── Email - Send via Gmail
├── Utilities/ (reusable helpers)
│   ├── JSON - Validate
│   ├── Data - Clean HTML
│   └── Text - Truncate
└── Error Handlers/
    └── Global Error Handler
```

### 🎯 Development Workflow

1. **Plan** (5 min):

   - Write down inputs and outputs
   - Identify major stages
   - Sketch on paper

2. **Prototype** (15 min):

   - Build happy path only
   - Use hardcoded test data
   - Get something working

3. **Test** (10 min):

   - Run with real data
   - Check outputs
   - Note failures

4. **Refine** (20 min):

   - Add error handling
   - Parameterize hardcoded values
   - Improve logging

5. **Extract** (15 min):

   - Identify reusable parts
   - Create subworkflows
   - Clean up main flow

6. **Document** (5 min):
   - Add sticky notes
   - Name nodes clearly
   - Update workflow description

---

## 5. Version Control Strategies

### 📚 Official Docs

- [n8n CLI](https://docs.n8n.io/hosting/cli-commands/)
- [Import/Export workflows](https://docs.n8n.io/workflows/share/)

### Strategy 1: Manual Export (Simplest)

**Workflow:**

1. Click **"⋮" (three dots)** on workflow
2. Select **"Download"**
3. Save as: `workflow-name-v1.json`

**Folder Structure:**

```
n8n-workflows/
├── production/
│   ├── security-digest-v2.json
│   └── email-sender-v1.json
├── staging/
│   └── security-digest-v3-beta.json
└── archive/
    ├── security-digest-v1.json
    └── email-sender-v0.json
```

**Naming Convention:**

```
[workflow-name]-v[major].[minor].json

Examples:
- security-digest-v1.0.json
- security-digest-v1.1.json (minor update)
- security-digest-v2.0.json (major rewrite)
```

### Strategy 2: Git-Based Version Control (Recommended)

**Setup:**

```bash
# Create repository
mkdir n8n-workflows
cd n8n-workflows
git init

# Create structure
mkdir -p workflows/{production,staging,development}
mkdir -p subworkflows
mkdir -p docs

# Add .gitignore
cat > .gitignore << 'EOF'
# Sensitive data
*-credentials.json
.env

# Temporary files
*.tmp
*.bak
EOF

# Initial commit
git add .
git commit -m "Initial n8n workflows repository"
```

**Workflow Process:**

```bash
# 1. Start new feature
git checkout -b feature/add-slack-integration

# 2. Export workflow from n8n
# Go to n8n → Download workflow as JSON

# 3. Save to git
cp ~/Downloads/slack-integration.json workflows/development/
git add workflows/development/slack-integration.json
git commit -m "Add: Slack integration workflow

- Sends digest to #security channel
- Includes article count and top stories
- Handles rate limiting"

# 4. Test in development

# 5. Promote to staging
git checkout staging
git merge feature/add-slack-integration
cp workflows/development/slack-integration.json workflows/staging/
git commit -m "Promote: Slack integration to staging"

# 6. Test in staging

# 7. Deploy to production
git checkout main
git merge staging
cp workflows/staging/slack-integration.json workflows/production/
git tag -a v1.2.0 -m "Release: Add Slack integration"
git commit -m "Release: v1.2.0 - Slack integration"
git push origin main --tags
```

### Strategy 3: Automated Backup Script

**Create `backup-workflows.sh`:**

```bash
#!/bin/bash

# Configuration
N8N_URL="http://localhost:5678"
N8N_API_KEY="your-api-key"
BACKUP_DIR="./backups/$(date +%Y-%m-%d)"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Export all workflows
echo "📦 Backing up n8n workflows..."

# Get list of workflows (requires n8n API)
curl -X GET "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  | jq -r '.data[] | .id + "," + .name' \
  | while IFS=, read -r id name; do

    # Download workflow
    echo "  └─ Exporting: $name (ID: $id)"
    curl -X GET "$N8N_URL/api/v1/workflows/$id" \
      -H "X-N8N-API-KEY: $N8N_API_KEY" \
      > "$BACKUP_DIR/${name}-${id}.json"
  done

# Commit to git
cd "$BACKUP_DIR/.."
git add .
git commit -m "Auto-backup: $(date +%Y-%m-%d)"

echo "✅ Backup complete: $BACKUP_DIR"
```

**Add to crontab:**

```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup-workflows.sh
```

### Strategy 4: Changelog and Documentation

**Create `CHANGELOG.md`:**

```markdown
# Changelog

All notable changes to n8n workflows will be documented in this file.

## [2.0.0] - 2025-10-09

### Added

- Advanced filtering with AI-based scoring
- Support for multiple RSS categories
- Automatic retry on failed API calls

### Changed

- Improved email template with better formatting
- Reduced API costs by 40% with smarter filtering

### Fixed

- Bug where empty content caused crashes
- Category mapping not working for new feeds

### Removed

- Deprecated Fever API authentication (replaced with Basic Auth)

## [1.1.0] - 2025-10-01

### Added

- Email digest subworkflow
- Slack notification integration

### Fixed

- Timezone issues in scheduling

## [1.0.0] - 2025-09-25

### Added

- Initial release
- RSS feed fetching
- Basic email sending
```

**Create `README.md` for each workflow:**

````markdown
# Security Digest Workflow

## Overview

Fetches security articles from RSS feeds, filters by relevance, and sends weekly email digest.

## Version

v2.0.0 (2025-10-09)

## Dependencies

- Subworkflow: "Email - Send Digest v1"
- Subworkflow: "RSS - Fetch Articles v2"
- External: CommaFeed RSS reader
- External: Gmail API

## Configuration

### Environment Variables

- `COMMAFEED_URL`: https://commafeed.lab.aminrj.com
- `COMMAFEED_USER`: amine
- `COMMAFEED_PASSWORD`: \*\*\*

### Schedule

- Runs: Every Monday at 9:00 AM
- Timezone: UTC

## Data Flow

1. Fetch categories and feeds from CommaFeed
2. Fetch articles (last 3 days)
3. Filter by relevance score (>3)
4. Select top 12 articles across categories
5. Generate email digest
6. Send via Gmail

## Testing

1. Pin test data from "Fetch Articles" node
2. Test "Advanced Filter" with pinned data
3. Verify output has 10-15 articles
4. Check email formatting in preview

## Rollback

If issues occur, revert to v1.1.0:

```bash
git checkout tags/v1.1.0
# Import workflow-v1.1.0.json to n8n
```
````

## Maintenance

- Update feed URLs quarterly
- Review filter thresholds monthly
- Archive old versions after 6 months

````

### Strategy 5: Release Management

**Use semantic versioning:**

- **Major (1.0.0 → 2.0.0)**: Breaking changes, workflow restructure
- **Minor (1.0.0 → 1.1.0)**: New features, no breaking changes
- **Patch (1.0.0 → 1.0.1)**: Bug fixes, minor tweaks

**Release Checklist:**

```markdown
## Pre-Release Checklist

- [ ] All nodes have clear names
- [ ] Error handling on all API calls
- [ ] Sensitive data in environment variables (not hardcoded)
- [ ] Tested with production data
- [ ] Subworkflows are stable versions
- [ ] Documentation updated
- [ ] Changelog entry added
- [ ] Tagged in git
- [ ] Backup of previous version saved

## Post-Release Checklist

- [ ] Monitor first execution
- [ ] Check logs for errors
- [ ] Verify outputs match expected
- [ ] Update team documentation
- [ ] Schedule review in 1 week
````

### 🎯 Complete Git Workflow Example

```bash
# Initial setup
git init n8n-workflows
cd n8n-workflows

# Create structure
mkdir -p {workflows,subworkflows,docs,scripts}

# Track changes
git add .
git commit -m "Initial structure"

# Feature development
git checkout -b feature/improved-filtering
# ... make changes in n8n ...
# Export workflow
git add workflows/security-digest-v2.json
git commit -m "Improve: Article filtering algorithm

- Add AI-based relevance scoring
- Filter out duplicate articles
- Prioritize recent content"

# Tag release
git tag -a v2.0.0 -m "Release: Improved filtering"
git push origin v2.0.0

# Create changelog
echo "## [2.0.0] - $(date +%Y-%m-%d)" >> CHANGELOG.md
echo "### Improved" >> CHANGELOG.md
echo "- Article filtering with AI scoring" >> CHANGELOG.md
git add CHANGELOG.md
git commit -m "Update changelog for v2.0.0"
```

---

## 🎓 Learning Path: 30-Day Plan

### Week 1: Foundations

- **Day 1-2**: Data flow and expressions
- **Day 3-4**: Build 3 simple workflows
- **Day 5-7**: Error handling practice

### Week 2: Intermediate

- **Day 8-10**: Create first subworkflow
- **Day 11-12**: Refactor existing workflow
- **Day 13-14**: Set up git repository

### Week 3: Advanced

- **Day 15-17**: Build complex multi-subworkflow system
- **Day 18-19**: Implement comprehensive error handling
- **Day 20-21**: Performance optimization

### Week 4: Best Practices

- **Day 22-24**: Documentation and versioning
- **Day 25-26**: Monitoring and alerting
- **Day 27-28**: Code review with another workflow
- **Day 29-30**: Build something from scratch applying all concepts

---

## 📚 Additional Resources

### Official Documentation

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community Forum](https://community.n8n.io/)
- [n8n GitHub](https://github.com/n8n-io/n8n)

### Video Tutorials

- [n8n YouTube Channel](https://www.youtube.com/c/n8nio)
- Search: "n8n tutorials" for community content

### Templates

- [n8n Workflow Templates](https://n8n.io/workflows/)
- Study popular workflows for patterns

### Community

- [Discord Server](https://discord.gg/n8n)
- [Reddit r/n8n](https://www.reddit.com/r/n8n/)

---

## 🚀 Quick Start Checklist

Today, right now:

- [ ] Export your current workflow as JSON
- [ ] Create a git repository
- [ ] Commit your workflow with a meaningful message
- [ ] Add a README.md describing the workflow
- [ ] Identify one subworkflow you can extract
- [ ] Add error handling to one critical node
- [ ] Test a failure scenario

This week:

- [ ] Create your first subworkflow
- [ ] Set up automated backups
- [ ] Write documentation for main workflows
- [ ] Implement retry logic on API calls

This month:

- [ ] Refactor one complex workflow into modular parts
- [ ] Build a global error handler
- [ ] Create a workflow style guide for your team
- [ ] Implement monitoring and alerting

---

**You're now equipped to build professional, maintainable n8n workflows! Start small, iterate often, and always version your work.** 🎉

---

_Created: 2025-10-09 21:24_
[[today-2025-10-09]]
