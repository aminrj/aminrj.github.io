---
title: Evaluating AI Agents, A Practical Guide to Measuring What Matters
date: 2026-02-17
uuid: 202602170000
status: published
content-type: article
target-audience: advanced
categories: [LLM]
image:
  path: /assets/media/ai-security/evaluating-ai-agents.png
description: Scientific approach to testing LLM agents. Precision, recall, F1 metrics from 15+ years testing systems in banking, defense, aerospace, and automotive.
---

## Why Evaluating AI Agents Matters ?

After 15+ years writing tests for banking systems, defense software, aerospace applications, and automotive platforms, I thought I understood testing. I'd written unit tests, integration tests, end-to-end tests. I knew how to mock dependencies, write assertions, and catch regressions.

Then I started building LLM agents. And **everything I knew about testing broke**.

Traditional software is deterministic: call `add(2, 3)` and you get `5` every time. When it breaks, you get errors, stack traces, obviously wrong output. But LLM agents? They fail _quietly_. They produce outputs that seem reasonable but are subtly incorrect. You can test a few examples manually, feel confident, ship to production—and discover weeks later your agent has a 35% error rate.

This article documents what I learned building an evaluation framework for AI agents in a real procurement analysis system. Not theoretical best practices, but practical code and metrics that caught actual production issues before they became costly problems.

If you're building AI agents for production—whether they filter data, score content, or make recommendations—you need to know if they actually work. Not "it seems fine" or "the output looks reasonable." You need **quantitative evidence**.

This guide walks through building an evaluation framework for AI agents. We'll cover why evaluation matters, what metrics to use, and how to implement a system that lets you measure performance scientifically. All code examples are production-ready and tested.

**This is Part 4 of the LLM Engineering series.** If you haven't read the earlier parts, start with [Part 1: Building a Procurement Analyst AI](/posts/LLM-engineering-building-a-procurements-analyst-ai/), which covers the initial implementation. [Part 2: Production-Ready LLM Agents](/posts/Build-production-ready-llam-agents/) discusses architecture patterns, and [Part 3: From MVP to Production SaaS](/posts/from-mvp-to-prod/) covers deployment. This article focuses on the evaluation framework that lets you measure and improve agent performance scientifically.

## What You'll Learn

- **Why AI agents fail silently** and how to catch these failures
- **Building test datasets** that reveal actual agent performance
- **Essential metrics**: Precision, Recall, F1, MAE, RMSE, and Calibration
- **Scientific iteration**: Using data to improve agents systematically
- **CI/CD integration**: Preventing quality regressions in production

## Prerequisites

To follow along, you should understand:

- **Python** basics (classes, async/await)
- **Basic statistics** (means, percentages)
- **LLM concepts** (prompts, confidence scores)
- Familiarity with **classification tasks** (yes/no decisions)

No advanced ML knowledge required—we'll explain all the metrics from first principles.

## Context: Why This Matters

**The Problem**: Most AI agent failures are invisible. Your agent might be making wrong decisions 30-40% of the time, but without systematic evaluation, you won't know until customers complain.

**The Solution**: Treat AI agent evaluation like software testing. Create test suites, measure performance, set quality gates, and iterate based on data—not hunches.

## Why AI Agents Need Different Testing Approaches

### Traditional Software: Deterministic Testing

Traditional software testing is **deterministic**: If you call `add(2, 3)`, you expect `5` every time. When something breaks, you get:

- An error message
- A stack trace
- Visibly wrong output (like returning `"hello"` instead of `5`)

### AI Agents: Probabilistic Failures

AI agents don't work this way. They **fail quietly** by producing outputs that _seem_ reasonable but are subtly incorrect.

Consider a simple filter agent:

```python
async def filter_tender(tender: Tender) -> FilterResult:
    prompt = "Is this tender relevant for our company?"
    result = await llm.generate(prompt)
    return result
```

You test it on a few examples and everything looks fine. But here's what you're missing:

**Test 1**: "AI Security Platform" → Relevant (Correct)  
**Test 2**: "Office Furniture" → Not Relevant (Correct)

Great! Ship it to production.

Three weeks later, you analyze 100 real predictions and discover:

- **Precision**: 72% (28% of "relevant" predictions were actually irrelevant)
- **Recall**: 65% (missed 35% of truly relevant opportunities)

The agent _looked_ fine because you only tested obvious cases. You didn't test:

- **Edge cases**: Hardware projects that include software components
- **Ambiguous cases**: Research studies vs. implementation projects
- **Boundary cases**: When does "IT infrastructure" count as software development?

This is the core problem: **manual spot-checking gives you false confidence**. You need systematic evaluation against a known-good test set.

![Evaluation Workflow](diagrams_evaluation/01_evaluation_workflow.md)

**\*Diagram 1**: The scientific evaluation loop that enables data-driven improvements.\*

## The Solution: Build a Measurement System

The approach is straightforward:

1. **Create a test dataset** where you know the correct answers
2. **Run your agent** on this dataset
3. **Calculate metrics** comparing predictions to ground truth
4. **Iterate and improve** based on data, not guesses

**Why This Works:**

This gives you a **scientific loop**: measure baseline → make changes → measure again → decide what to keep.

Instead of guessing "does this prompt change help?", you can prove it with numbers:

- Baseline F1: 0.73
- After change F1: 0.87 (+14%)
- Decision: Keep the change

Let's build this system piece by piece, starting with the foundation.

## Part 1: Creating Your Test Dataset

Your test dataset is the ground truth—cases where you've manually determined the correct answer. This is the most important piece of your evaluation system. Get this wrong, and all your metrics will be meaningless.

### What Makes a Good Test Case

A test case needs three things:

1. **Input data** (what goes into your agent)
2. **Expected output** (what the agent should produce)
3. **Documentation** (why this is the correct answer)

Here's a complete example:

Here's a complete example:

```python
from dataclasses import dataclass
from typing import List

@dataclass
class EvaluationTestCase:
    test_id: str
    title: str
    description: str

    # What the agent should predict
    expected_relevant: bool
    expected_confidence_min: float
    expected_categories: List[str]

    # Why this is the correct answer
    notes: str
    edge_case_reasoning: str = ""
```

Let's look at three types of test cases you need:

**Type 1: Clear Positive (builds confidence)**

```python
EVAL_001 = EvaluationTestCase(
    test_id="EVAL-001",
    title="AI-Powered Threat Detection System",
    description="""
    National Defense Agency requires AI-based cybersecurity
    threat detection with real-time response capabilities.
    Must integrate ML models, behavioral analytics, and
    automated incident response.
    Budget: €2M over 2 years.
    """,
    expected_relevant=True,
    expected_confidence_min=0.9,
    expected_categories=["cybersecurity", "ai", "software"],
    notes="Obvious match: AI + cybersecurity + software development."
)
```

This case is unambiguous. If your agent fails here, you have a serious problem. These cases verify your agent handles obvious scenarios correctly.

**Type 2: Clear Negative (tests specificity)**

```python
EVAL_005 = EvaluationTestCase(
    test_id="EVAL-005",
    title="Office Furniture and Interior Design",
    description="""
    Supply and installation of ergonomic office furniture for
    government building renovation. Includes desks, chairs,
    lighting fixtures, and minor carpentry work.
    Budget: €150K.
    """,
    expected_relevant=False,
    expected_confidence_min=0.9,
    expected_categories=[],
    notes="Clearly not a software/tech project. Tests if agent avoids false positives."
)
```

This verifies your agent doesn't hallucinate relevance where none exists. If it marks this as relevant, you're getting false positives.

**Type 3: Edge Case (finds weaknesses)**

```python
EVAL_009 = EvaluationTestCase(
    test_id="EVAL-009",
    title="Network Infrastructure Upgrade with Management Software",
    description="""
    Hospital network modernization project:
    - Replace 500 switches and routers (€800K)
    - Install fiber cabling across three buildings (€200K)
    - Configure network monitoring software (€50K)
    Total budget: €1.05M
    """,
    expected_relevant=False,
    expected_confidence_min=0.7,
    expected_categories=[],
    edge_case_reasoning="""
    This is tricky because it mentions software (monitoring), but 95% of
    the budget and work is hardware infrastructure. The software component
    is purely configuration, not development. A good agent should recognize
    this is fundamentally a hardware project.
    """,
    notes="Tests if agent correctly weighs primary vs. secondary components."
)
```

This is where agents typically struggle. The presence of "software" might trigger a false positive. Your edge cases should come from real-world ambiguity you expect to encounter.

### How Many Test Cases Do You Need?

**For MVP evaluation**: Start with **15-20 cases** distributed as:

- **4-5 clear positives** (obvious yes)
- **4-5 clear negatives** (obvious no)
- **5-7 edge cases** (ambiguous or tricky)
- **2-3 domain-specific challenges** (unique to your use case)

This gives you enough data for meaningful metrics without requiring weeks of test case creation.

**For production**: Expand to **50-100 cases** covering:

- All known failure modes from production
- Representative sample of real-world data distribution
- Corner cases discovered through user feedback

**Time Investment:**

- Creating 15-20 cases: ~2-3 hours
- Creating 50-100 cases: ~1-2 days
- Maintaining as you discover new failure modes: ongoing

**Pro Tip**: Start small. You'll naturally expand your test set as you discover where your agent fails in production. Your evaluation dataset should be a living document.

## Part 2: Understanding Classification Metrics

Now you have a test dataset. When you run your agent on it, you'll get predictions. How do you measure if these predictions are good?

For a binary classifier (yes/no, relevant/irrelevant), every prediction falls into one of four categories. Understanding these is critical.

### The Confusion Matrix: Foundation of All Metrics

Imagine you run your filter agent on 10 test cases. Here's what might happen:

```bash
Your Test Set:
- 5 cases that SHOULD be relevant
- 5 cases that should NOT be relevant

Your Agent Predicts:
- 6 cases as "relevant"
- 4 cases as "not relevant"
```

Now let's see where predictions matched reality:

```bash
                      AGENT SAID           AGENT SAID
                      "RELEVANT"           "NOT RELEVANT"

ACTUALLY        │        4             │        1
RELEVANT        │  (True Positives)    │  (False Negatives)
(5 cases)       │   Got it right       │   Missed it

ACTUALLY        │        2             │        3
NOT RELEVANT    │  (False Positives)   │  (True Negatives)
(5 cases)       │   Wrong alarm        │   Got it right
```

Let's unpack what each quadrant means:

**True Positives (TP = 4)**: Agent said "relevant" and was correct. Good.

**False Positives (FP = 2)**: Agent said "relevant" but was wrong. Your team will waste time investigating these irrelevant opportunities.

**False Negatives (FN = 1)**: Agent said "not relevant" but was wrong. You missed a real opportunity—potentially costly.

**True Negatives (TN = 3)**: Agent said "not relevant" and was correct. Good.

From these four numbers, we derive all our metrics. Let's see how.

![Confusion Matrix](diagrams_evaluation/02_confusion_matrix.md)

**\*Diagram 2**: Visual breakdown of the confusion matrix showing all four prediction outcomes.\*

### Metric 1: Precision (Quality of YES Predictions)

**Question**: When my agent says "relevant," how often is it actually relevant?

```python
@dataclass
class FilterMetrics:
    true_positives: int = 0
    false_positives: int = 0
    true_negatives: int = 0
    false_negatives: int = 0

    @property
    def precision(self) -> float:
        """What fraction of positive predictions were correct?"""
        denominator = self.true_positives + self.false_positives
        if denominator == 0:
            return 0.0
        return self.true_positives / denominator

# With our example: 4 / (4 + 2) = 0.67 = 67%
```

**Interpretation**: 67% precision means that when your agent flags something as relevant, it's only correct 2/3 of the time. One third of your "relevant" predictions are false alarms.

**When to care**: If following up on false positives is expensive (wastes your team's time), you need high precision. For our procurement use case, if my team investigates every "relevant" tender and 33% turn out to be garbage, that's hours of wasted effort.

**Real-world impact**: Low precision = your team loses trust in the system. They start ignoring its recommendations.

### Metric 2: Recall (Completeness of Detection)

**Question**: Of all the truly relevant cases, how many did my agent find?

```python
@property
def recall(self) -> float:
    """What fraction of actual positives did we detect?"""
    denominator = self.true_positives + self.false_negatives
    if denominator == 0:
        return 0.0
    return self.true_positives / denominator

# With our example: 4 / (4 + 1) = 0.80 = 80%
```

**Interpretation**: 80% recall means you're catching 4 out of 5 relevant opportunities, but missing 1 out of 5.

**When to care**: If missing a relevant case is costly (lost revenue, missed opportunities), you need high recall. For procurement, if you miss a €500K contract because your filter rejected it, that's a real loss.

**Real-world impact**: Low recall = opportunity cost. You're leaving money on the table.

### The Precision-Recall Tradeoff

Here's the challenge: these metrics are usually in tension. You can often increase one by decreasing the other.

**Example: Making your agent more aggressive**

```python
# Current prompt (conservative)
"Only mark as relevant if this clearly matches our expertise"

# New prompt (aggressive)
"Mark as relevant if this might be relevant"
```

What happens:

- **Recall goes up** (90% → 95%): You catch more relevant cases
- **Precision goes down** (67% → 50%): But you also flag more junk

The opposite is true too. Make your agent pickier, and precision increases but recall decreases.

![Precision-Recall Tradeoff](diagrams_evaluation/03_precision_recall_tradeoff.md)

**\*Diagram 3**: Visualizing the precision-recall tradeoff and how agent behavior affects both metrics.\*

### Metric 3: F1 Score (Balanced Measure)

When you have one metric going up and another going down, how do you evaluate overall progress? You need a single number that balances both.

```python
@property
def f1_score(self) -> float:
    """Harmonic mean of precision and recall"""
    p = self.precision
    r = self.recall
    if p + r == 0:
        return 0.0
    return 2 * (p * r) / (p + r)

# With precision=0.67 and recall=0.80:
# F1 = 2 * (0.67 * 0.80) / (0.67 + 0.80) = 0.73 = 73%
```

**Why harmonic mean instead of arithmetic mean?**

Arithmetic mean would be: (0.67 + 0.80) / 2 = 0.735

But harmonic mean (F1) gives us: 0.73

The difference matters more with extreme imbalance:

```bash
Scenario A: Precision = 100%, Recall = 10%
- Arithmetic mean: 55% (looks decent)
- Harmonic mean (F1): 18% (shows the problem)

Scenario B: Precision = 70%, Recall = 70%
- Arithmetic mean: 70%
- Harmonic mean (F1): 70% (same)
```

Harmonic mean penalizes imbalance. If one metric is terrible, F1 stays low even if the other is perfect. This forces you to care about both metrics.

**Interpreting F1 Scores:**

- **F1 > 0.90**: Excellent. Production-ready.
- **F1 = 0.85-0.90**: Good. Acceptable for most use cases.
- **F1 = 0.75-0.85**: Needs improvement. Identify weak spots and iterate.
- **F1 < 0.75**: Significant issues. Don't deploy yet.

### Putting the Metrics Together

Let's implement this as a Python class:

```python
@dataclass
class FilterMetrics:
    true_positives: int = 0
    false_positives: int = 0
    true_negatives: int = 0
    false_negatives: int = 0

    def add_prediction(self, predicted: bool, expected: bool):
        """Add a single prediction and update counts"""
        if predicted and expected:
            self.true_positives += 1
        elif predicted and not expected:
            self.false_positives += 1
        elif not predicted and expected:
            self.false_negatives += 1
        else:
            self.true_negatives += 1

    @property
    def precision(self) -> float:
        denom = self.true_positives + self.false_positives
        return self.true_positives / denom if denom > 0 else 0.0

    @property
    def recall(self) -> float:
        denom = self.true_positives + self.false_negatives
        return self.true_positives / denom if denom > 0 else 0.0

    @property
    def f1_score(self) -> float:
        p, r = self.precision, self.recall
        return 2 * (p * r) / (p + r) if (p + r) > 0 else 0.0

    @property
    def accuracy(self) -> float:
        """Overall correctness"""
        total = (self.true_positives + self.false_positives +
                 self.true_negatives + self.false_negatives)
        correct = self.true_positives + self.true_negatives
        return correct / total if total > 0 else 0.0
```

Now use it:

```python
# Run evaluation
metrics = FilterMetrics()

for test_case in test_cases:
    result = await filter_agent.filter(test_case.tender)
    metrics.add_prediction(
        predicted=result.is_relevant,
        expected=test_case.expected_relevant
    )

# Print results
print(f"Precision: {metrics.precision:.2%}")  # 67%
print(f"Recall:    {metrics.recall:.2%}")     # 80%
print(f"F1 Score:  {metrics.f1_score:.2%}")   # 73%
print(f"Accuracy:  {metrics.accuracy:.2%}")   # 70%
```

## Part 3: Metrics for Scoring Tasks

If your agent produces numerical scores (like rating a tender's value from 0-10), you need different metrics. The question shifts from "is this classification correct?" to "how close is this number to the right answer?"

### Mean Absolute Error (MAE): Average Distance from Truth

MAE tells you: on average, how far off are your predictions?

```python
@dataclass
class RatingMetrics:
    errors: List[float] = field(default_factory=list)
    actual_scores: List[float] = field(default_factory=list)
    predicted_scores: List[float] = field(default_factory=list)

    def add_prediction(self, predicted: float, expected_range: Tuple[float, float]):
        """Add a rating prediction"""
        # Use midpoint of expected range as target
        expected = (expected_range[0] + expected_range[1]) / 2
        error = predicted - expected

        self.errors.append(error)
        self.actual_scores.append(expected)
        self.predicted_scores.append(predicted)

    @property
    def mae(self) -> float:
        """Mean Absolute Error"""
        if not self.errors:
            return 0.0
        return statistics.mean([abs(e) for e in self.errors])
```

**Example:**

```python
metrics = RatingMetrics()

# Test case 1: Expected 7-9, agent predicts 8.0
metrics.add_prediction(predicted=8.0, expected_range=(7.0, 9.0))
# Error:0.0 (perfect!)

# Test case 2: Expected 7-9, agent predicts 5.0
metrics.add_prediction(predicted=5.0, expected_range=(7.0, 9.0))
# Error: -3.0 (too low by 3 points)

# Test case 3: Expected 7-9, agent predicts 9.5
metrics.add_prediction(predicted=9.5, expected_range=(7.0, 9.0))
# Error: +1.5 (too high by 1.5 points)

print(f"MAE: {metrics.mae:.2f}")
# MAE = (0.0 + 3.0 + 1.5) / 3 = 1.5
```

**Interpretation**: On average, predictions are off by 1.5 points. For a 0-10 scale, this is moderate. MAE < 1.0 would be good; MAE > 2.0 would be concerning.

**Why MAE matters**: It's in the same units as your scores. If you're rating tenders on a 10-point scale, an MAE of 1.5 means "typically off by about 1-2 points." Your business stakeholders can understand this directly.

### Root Mean Squared Error (RMSE): Penalizing Large Mistakes

RMSE is similar to MAE but punishes large errors more heavily:

### Root Mean Squared Error (RMSE): Penalizing Large Mistakes

RMSE is similar to MAE but punishes large errors more heavily:

```python
@property
def rmse(self) -> float:
    """Root Mean Squared Error"""
    if not self.errors:
        return 0.0
    return (statistics.mean([e ** 2 for e in self.errors])) ** 0.5
```

**Why squaring matters:**

```
Errors: [0.0, -3.0, +1.5]

MAE calculation:
|0.0| + |-3.0| + |1.5| = 4.5
MAE = 4.5 / 3 = 1.5

RMSE calculation:
0.0² + (-3.0)² + 1.5² = 0 + 9 + 2.25 = 11.25
Mean = 11.25 / 3 = 3.75
RMSE = √3.75 = 1.94
```

RMSE (1.94) is higher than MAE (1.5) because the large error (-3.0) gets amplified when squared.

**When to use RMSE**: If occasional huge mistakes are particularly bad. For example:

- Rating a terrible tender (should be 2/10) as excellent (predicted 9/10) is worse than
- Being consistently off by 1 point on every prediction

RMSE penalizes that first scenario more heavily.

### Correlation: Are You Directionally Correct?

Sometimes absolute accuracy matters less than relative ordering. Correlation measures: "When actual score goes up, does predicted score go up too?"

```python
@property
def correlation(self) -> float:
    """Pearson correlation between actual and predicted"""
    if len(self.actual_scores) < 2:
        return 0.0

    mean_actual = statistics.mean(self.actual_scores)
    mean_pred = statistics.mean(self.predicted_scores)

    numerator = sum(
        (a - mean_actual) * (p - mean_pred)
        for a, p in zip(self.actual_scores, self.predicted_scores)
    )

    denom_actual = sum((a - mean_actual) ** 2 for a in self.actual_scores)
    denom_pred = sum((p - mean_pred) ** 2 for p in self.predicted_scores)
    denominator = (denom_actual * denom_pred) ** 0.5

    return numerator / denominator if denominator > 0 else 0.0
```

**Interpretation:**

- **Correlation = 1.0**: Perfect positive relationship (agent's scores perfectly track reality)
- **Correlation > 0.85**: Excellent (scores track well, minor deviations)
- **Correlation > 0.70**: Good (generally correct ordering, some inconsistencies)
- **Correlation < 0.50**: Poor (predictions don't meaningfully track reality)

**Example:**

```
Actual scores:    [3, 5, 7, 9]
Predicted scores: [2, 4, 8, 10]

Correlation: 0.97 (excellent)
MAE: 0.75 (also good)
```

Even though the predictions aren't perfect, they maintain the correct relative ordering: lowest actual gets lowest prediction, highest actual gets highest prediction.

## Part 4: Confidence Calibration (Advanced)

This is a subtle but critical concept. When your agent says "90% confident," is it actually correct 90% of the time?

Many LLMs are overconfident. They'll say "I'm 95% sure" when they're actually only right 60% of the time. If you build automated decision-making on top of confidence scores, this will bite you.

### Understanding the Problem

```python
# Your agent makes 10 predictions with "high confidence"
predictions = [
    (confidence=0.95, actual_correct=False),  # Wrong
    (confidence=0.92, actual_correct=False),  # Wrong
    (confidence=0.93, actual_correct=True),   # Correct
    (confidence=0.94, actual_correct=False),  # Wrong
    (confidence=0.95, actual_correct=True),   # Correct
    (confidence=0.90, actual_correct=False),  # Wrong
    (confidence=0.91, actual_correct=True),   # Correct
    (confidence=0.96, actual_correct=False),  # Wrong
    (confidence=0.90, actual_correct=True),   # Correct
    (confidence=0.93, actual_correct=False),  # Wrong
]

# Average confidence: ~93%
# Actual accuracy: 4/10 = 40%
# This is DANGEROUS overconfidence!
```

If you write code like `if confidence > 0.90: auto_approve()`, you'll be auto-approving bad predictions 60% of the time.

### Measuring Calibration: Expected Calibration Error

The idea: group predictions into confidence bins and check if accuracy matches confidence.

```python
class ConfidenceCalibration:
    def __init__(self):
        self.predictions: List[Tuple[float, bool]] = []

    def add_prediction(self, confidence: float, is_correct: bool):
        self.predictions.append((confidence, is_correct))

    def get_calibration_curve(self, num_bins: int = 10):
        """Split predictions into confidence bins"""
        sorted_preds = sorted(self.predictions, key=lambda x: x[0])
        bin_size = max(1, len(sorted_preds) // num_bins)

        bins = []
        for i in range(0, len(sorted_preds), bin_size):
            bin_preds = sorted_preds[i:i + bin_size]
            if not bin_preds:
                continue

            confidences = [p[0] for p in bin_preds]
            corrects = [p[1] for p in bin_preds]

            mean_conf = statistics.mean(confidences)
            accuracy = sum(corrects) / len(corrects)

            bins.append({
                'mean_confidence': mean_conf,
                'accuracy': accuracy,
                'calibration_error': abs(mean_conf - accuracy),
                'count': len(bin_preds)
            })

        return bins

    @property
    def expected_calibration_error(self) -> float:
        """Weighted average calibration error across bins"""
        bins = self.get_calibration_curve()
        if not bins:
            return 0.0

        total_predictions = sum(b['count'] for b in bins)
        ece = sum(
            (b['count'] / total_predictions) * b['calibration_error']
            for b in bins
        )
        return ece
```

**How to read the results:**

```python
# Well-calibrated agent
bins = [
    {'mean_confidence': 0.52, 'accuracy': 0.50, 'error': 0.02},  # OK
    {'mean_confidence': 0.71, 'accuracy': 0.70, 'error': 0.01},  # OK
    {'mean_confidence': 0.89, 'accuracy': 0.88, 'error': 0.01},  # OK
]
ECE = 0.013  # Excellent calibration

# Overconfident agent
bins = [
    {'mean_confidence': 0.50, 'accuracy': 0.48, 'error': 0.02},  # OK
    {'mean_confidence': 0.70, 'accuracy': 0.64, 'error': 0.06},  # Slightly off
    {'mean_confidence': 0.90, 'accuracy': 0.65, 'error': 0.25},  # Very overconfident!
]
ECE = 0.18  # Poor calibration
```

**Interpreting ECE:**

- **ECE < 0.05**: Excellently calibrated (confidence matches reality)
- **ECE < 0.10**: Good calibration (minor deviations)
- **ECE < 0.15**: Acceptable (usable with caution)
- **ECE > 0.15**: Overconfident, don't trust confidence scores for automation

**Why this matters**: If your ECE is high, you cannot use confidence thresholds for automated decisions. An agent that says "95% confident" might only be right 70% of the time.

![Confidence Calibration](diagrams_evaluation/04_confidence_calibration.md)

**\*Diagram 4**: Calibration curves showing well-calibrated vs. overconfident agents.\*

**Real-World Impact:**

**Poorly Calibrated** (ECE = 0.25):

- Agent says: "95% confident"
- Actual accuracy: 70%
- Result: Auto-approval systems fail 30% of the time

**Well Calibrated** (ECE = 0.05):

- Agent says: "95% confident"
- Actual accuracy: 93%
- Result: Safe to use confidence thresholds for automation

## Part 5: Building the Complete Evaluator

## Part 5: Building the Complete Evaluator

Now we tie everything together. You have:

- Test cases with known correct answers
- Metrics classes to track performance
- Understanding of what each metric means

The evaluator orchestrates the process: run your agent on each test case, collect results, compute metrics.

```python
from dataclasses import dataclass
from datetime import datetime
import asyncio

@dataclass
class TestCaseResult:
    """Result from evaluating a single test case"""
    test_id: str
    predicted_relevant: bool
    predicted_confidence: float
    expected_relevant: bool
    is_correct: bool
    processing_time: float
    error: str = ""

@dataclass
class EvaluationResult:
    """Complete evaluation results"""
    timestamp: str
    test_cases_count: int
    filter_metrics: FilterMetrics
    rating_metrics: RatingMetrics
    confidence_calibration: ConfidenceCalibration
    total_processing_time: float
    errors_count: int

class Evaluator:
    """Orchestrates evaluation across all test cases"""

    def __init__(self, config):
        self.config = config
        self.llm = LLMService(config)
        self.filter_agent = FilterAgent(self.llm, config)
        self.rating_agent = RatingAgent(self.llm, config)

    async def evaluate_test_case(self, test_case: EvaluationTestCase) -> TestCaseResult:
        """Run one test case through the agent"""
        start_time = datetime.now()

        try:
            # Convert test case to tender format
            tender = Tender(**test_case.to_tender_dict())

            # Run filter agent
            filter_result = await self.filter_agent.filter(tender)

            # Was the prediction correct?
            is_correct = (
                filter_result.is_relevant == test_case.expected_relevant
            )

            # If flagged as relevant, run rating agent
            rating_result = None
            if filter_result.is_relevant:
                rating_result = await self.rating_agent.rate(
                    tender,
                    [c.value for c in filter_result.categories]
                )

            processing_time = (datetime.now() - start_time).total_seconds()

            return TestCaseResult(
                test_id=test_case.test_id,
                predicted_relevant=filter_result.is_relevant,
                predicted_confidence=filter_result.confidence,
                expected_relevant=test_case.expected_relevant,
                is_correct=is_correct,
                processing_time=processing_time,
            )

        except Exception as e:
            # Capture errors without failing the entire evaluation
            return TestCaseResult(
                test_id=test_case.test_id,
                predicted_relevant=False,
                predicted_confidence=0.0,
                expected_relevant=test_case.expected_relevant,
                is_correct=False,
                processing_time=0.0,
                error=str(e),
            )

    async def evaluate_dataset(
        self,
        test_cases: List[EvaluationTestCase],
        max_concurrent: int = 3
    ) -> EvaluationResult:
        """Evaluate complete test dataset"""

        start_time = datetime.now()

        # Initialize all metrics
        filter_metrics = FilterMetrics()
        rating_metrics = RatingMetrics()
        calibration = ConfidenceCalibration()

        # Run evaluations with concurrency control
        # (prevents overwhelming your LLM service)
        semaphore = asyncio.Semaphore(max_concurrent)

        async def evaluate_with_semaphore(tc):
            async with semaphore:
                return await self.evaluate_test_case(tc)

        # Run all test cases
        results = await asyncio.gather(*[
            evaluate_with_semaphore(tc) for tc in test_cases
        ])

        # Aggregate results into metrics
        errors_count = 0
        for result in results:
            if result.error:
                errors_count += 1
                continue

            # Update filter metrics
            filter_metrics.add_prediction(
                predicted=result.predicted_relevant,
                expected=result.expected_relevant
            )

            # Update calibration tracking
            calibration.add_prediction(
                confidence=result.predicted_confidence,
                is_correct=result.is_correct
            )

        total_time = (datetime.now() - start_time).total_seconds()

        return EvaluationResult(
            timestamp=datetime.now().isoformat(),
            test_cases_count=len(test_cases),
            filter_metrics=filter_metrics,
            rating_metrics=rating_metrics,
            confidence_calibration=calibration,
            total_processing_time=total_time,
            errors_count=errors_count,
        )
```

### Using the Evaluator

```python
# Initialize
evaluator = Evaluator(config)

# Run evaluation
result = await evaluator.evaluate_dataset(ALL_TEST_CASES)

# Print results
print(f"Test Cases: {result.test_cases_count}")
print(f"Processing Time: {result.total_processing_time:.1f}s")
print(f"\nFilter Performance:")
print(f"  Precision: {result.filter_metrics.precision:.2%}")
print(f"  Recall:    {result.filter_metrics.recall:.2%}")
print(f"  F1 Score:  {result.filter_metrics.f1_score:.2%}")
print(f"\nCalibration:")
print(f"  ECE: {result.confidence_calibration.expected_calibration_error:.4f}")

if result.errors_count > 0:
    print(f"\nWarning: {result.errors_count} test cases had errors")
```

## Part 6: Using Evaluation to Improve Your Agent

Once you have a working evaluation system, you can iterate scientifically. Here's the workflow:

### Step 1: Establish Baseline

```bash
# Run evaluation and save results
python -m evaluation.run --save-baseline
```

This gives you numbers to beat:

```
Baseline Results (2026-02-14):
  F1 Score: 0.73
  Precision: 0.67
  Recall: 0.80
  ECE: 0.18
```

### Step 2: Hypothesize an Improvement

Look at your metrics and identify weaknesses. In this example:

- Precision is low (67%) → Too many false positives
- ECE is high (0.18) → Overconfident

**Hypothesis**: Adding few-shot examples to the prompt will help the agent recognize edge cases, reducing false positives.

### Step 3: Make the Change

```python
# Before: criteria-only prompt
FILTER_PROMPT = """
Determine if this tender is relevant for a software company.

Criteria:
- Must involve software development or AI/ML
- Must not be primarily hardware or construction
- …
"""

# After: added examples
FILTER_PROMPT = """
Determine if this tender is relevant for a software company.

Criteria:
- Must involve software development or AI/ML
- Must not be primarily hardware or construction
- …

Examples:

RELEVANT:
"AI cybersecurity platform with ML threat detection"
→ Yes, this is software + AI development

NOT RELEVANT:
"Network hardware upgrade with monitoring software setup"
→ No, primarily hardware (95% of budget), software is just configuration

Now evaluate this tender:
"""
```

### Step 3: Re-evaluate

```bash
python -m evaluation.run --output new_version.json
```

Results:

```
New Version Results:
  F1 Score: 0.87 (+14% vs baseline)
  Precision: 0.88 (+21% vs baseline)
  Recall: 0.86 (+6% vs baseline)
  ECE: 0.12 (-33% vs baseline)
```

### Step 4: Decide Based on Data

Improvements across the board:

- F1 jumped from 0.73 to 0.87 (crossed into "good" territory)
- Precision improved dramatically (false positives cut in half)
- ECE dropped (better calibrated confidence)
- Minor recall improvement

**Decision: Keep the change.** The data proves it works.

### What If Results Were Mixed?

Sometimes you'll see tradeoffs:

```
Experiment: Lower temperature from 0.1 to 0.05

Results:
  Precision: 0.88 → 0.92 (+4%)
  Recall: 0.86 → 0.78 (-8%)
  F1: 0.87 → 0.84 (-3%)
```

Lower temperature made the agent more conservative (higher precision), but it's now missing more relevant cases (lower recall). The net effect (F1) is negative.

**Decision: Revert the change.** The tradeoff isn't worth it.

Without quantitative evaluation, you'd be guessing. With metrics, you know exactly what each change does.

## Part 7: Preventing Regressions

Once your agent performs well, you want to make sure it stays that way. Set up **automated quality gates** that prevent degraded agents from reaching production.

![CI/CD Quality Gates](diagrams_evaluation/05_cicd_quality_gates.md)

**\*Diagram 5**: Automated quality gates in CI/CD pipeline that catch regressions before deployment.\*

### CI/CD Integration

**Goal**: Make evaluation a required step in your deployment pipeline, just like unit tests.

**How it works:**

1. Developer pushes code changes
2. CI runs evaluation suite automatically
3. Results compared against quality thresholds
4. Build passes or fails based on metrics
5. Only passing builds can be deployed

```bash
#!/bin/bash
# .github/workflows/evaluation.yml

# Run evaluation in CI
python -m evaluation.run --output ci_results.json

# Check quality thresholds
python scripts/check_quality.py ci_results.json
```

The checker script:

```python
# scripts/check_quality.py
import json
import sys

# Define minimum acceptable quality
THRESHOLDS = {
    'f1_score': 0.85,
    'precision': 0.85,
    'recall': 0.80,
    'calibration_ece': 0.15,
}

with open(sys.argv[1]) as f:
    result = json.load(f)

filter_metrics = result['metrics']['filter']
cal_metrics = result['metrics']['calibration']

# Check each threshold
failures = []

if filter_metrics['f1_score'] < THRESHOLDS['f1_score']:
    failures.append(f"F1 too low: {filter_metrics['f1_score']:.2%}")

if filter_metrics['precision'] < THRESHOLDS['precision']:
    failures.append(f"Precision too low: {filter_metrics['precision']:.2%}")

if filter_metrics['recall'] < THRESHOLDS['recall']:
    failures.append(f"Recall too low: {filter_metrics['recall']:.2%}")

if cal_metrics['ece'] > THRESHOLDS['calibration_ece']:
    failures.append(f"Calibration too poor: ECE={cal_metrics['ece']:.4f}")

if failures:
    print("Quality check FAILED:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

print("Quality check passed")
```

Now if someone makes a change that degrades the agent, CI fails. No regressions make it to production.

### Regression Detection

Beyond absolute thresholds, check for drops relative to your baseline:

```python
with open('benchmarks/baseline.json') as f:
    baseline = json.load(f)

baseline_f1 = baseline['metrics']['filter']['f1_score']
current_f1 = filter_metrics['f1_score']

drop = baseline_f1 - current_f1
if drop > 0.02:  # More than 2% drop
    print(f"Performance regression: F1 dropped {drop:.2%}")
    sys.exit(1)
```

This catches subtle degradation that might not hit absolute thresholds but represents a step backward.

## Practical Recommendations

### Start Small (Week 1)

Don't try to build the perfect evaluation system on day one. Start with:

- **10-15 test cases** (2-3 hours to create)
- **Precision, recall, F1 metrics** (basic `FilterMetrics` class)
- **A simple Python script** that prints results
- **Manual execution**: `python evaluate.py`

**Deliverable**: Know your baseline performance (e.g., "F1 = 0.73")

### Expand Strategically (Week 2-3)

Once you see the value, add:

- **More test cases** from production failures (aim for 30-50)
- **Confidence calibration** tracking (ECE metric)
- **JSON output** for tracking over time
- **Comparison script** to show improvements

**Deliverable**: Track improvements over time, prove changes help

### Automate Quality Gates (Week 4+)

Finally, integrate into your workflow:

- **CI/CD integration** (run on every PR)
- **Regression detection** (fail if performance drops)
- **Automated alerting** if production metrics degrade

**Deliverable**: Never ship a regression to production

### Focus on F1 Score

Unless you have specific business requirements (like "false positives are 10x worse than false negatives"), use F1 as your primary metric. It balances both concerns.

### Document Your Test Cases

Future you will thank past you. Write down _why_ each edge case should pass or fail. When debugging failures months later, this context is invaluable.

### Update Tests Based on Real Failures

When your agent fails in production, add that case to your test set. Your evaluation dataset should evolve to cover real-world scenarios you encounter.

### Set Realistic Thresholds

Don't demand F1 > 0.95 if achieving that would take months. Set thresholds based on:

- Your current baseline
- Cost of errors in your domain
- Effort required to improve

For many use cases, F1 > 0.85 is perfectly acceptable.

## What I Learned Building This Evaluation Framework

Looking back at 6-8 hours invested in building this evaluation system, three insights stand out:

**1. Metrics Reveal What Manual Testing Cannot**

I manually tested the agent on 5-6 examples and thought it worked great. The evaluation framework showed the real story: 67% precision and 80% recall (F1 = 0.73). Manual testing gives you false confidence because you unconsciously pick obvious test cases. A structured test dataset with edge cases shows you where the agent actually struggles. In systems I tested for defense contractors, we saw similar patterns—manual QA caught obvious bugs but missed subtle failure modes that only appeared under systematic testing.

**2. Confidence Scores Are Often Lies**

The agent would predict "relevant" with 95% confidence and be completely wrong. Without calibration metrics like ECE (Expected Calibration Error), I trusted these scores. After measuring, I discovered an ECE of 0.18—meaning the agent was systematically overconfident. This killed my plans for automated decision-making and forced me to add human review. In banking systems, this is why we never trust a model's self-assessment—always validate confidence distributions against ground truth outcomes.

**3. Quality Gates Prevent 3 AM Debugging Sessions**

The CI integration caught three separate regressions before they reached production. One prompt tweak improved readability but dropped recall by 8%. Without automated evaluation in CI, that would have shipped Friday evening and ruined my weekend. In aerospace projects, we learned this lesson the expensive way—manual pre-deployment testing always misses something. Automated quality gates don't get tired or skip steps.

The cost of _not_ having this framework: invisible failures, wasted time on false positives, missed opportunities, production incidents. The cost of building it: 6-8 hours. It paid for itself in the first week.

## Conclusion: From Guesswork to Science

The difference between **hobby AI development** and **professional AI development** is measurement.

### Without Evaluation

- You don't know if your system works
- You can't prove changes help
- Regressions ship to production
- You debug with no data
- Decisions based on "it looks good"

### With Systematic Evaluation

- You know your baseline performance
- You can A/B test changes scientifically
- You catch regressions before they ship
- You make data-driven decisions
- You build trust through transparency

## Real-World Impact

Building the evaluation framework in this guide—**18 test cases, metrics module, evaluator, and CLI**—took about **6-8 hours**. That investment has already paid for itself by:

1. **Identifying precision issues**: Discovered agent was accepting too many irrelevant tenders (67% precision)
2. **Proving improvements**: Showed few-shot prompting improved F1 by 14% (0.73 → 0.87)
3. **Catching overconfidence**: ECE of 0.18 revealed confidence scores couldn't be trusted for automation
4. **Preventing 3 regressions**: CI caught prompt changes that degraded recall
5. **Saving ~10 hours/week**: Team no longer manually reviews obvious false positives

**ROI**: 6 hours invested, 40+ hours saved in first month, plus avoided production issues.

## Your Next Steps

**Day 1** (2-3 hours):

- Create 10-15 test cases
- Implement basic `FilterMetrics` class
- Run first evaluation, record baseline

**Week 1** (4-6 hours):

- Add 10 more test cases from production data
- Implement calibration tracking
- Try one improvement, measure impact

**Week 2-3** (ongoing):

- Integrate into CI/CD
- Set quality thresholds
- Make evaluation part of your development workflow

**Remember**: Start with the basics—10 test cases, precision/recall/F1, and a simple evaluation script. Run it. Analyze results. Iterate. Expand as you find issues.

Your AI agents deserve the same rigor as your traditional software.

---

## Implementation Reference

Complete code for this evaluation framework:

````

**Running the evaluation:**

```bash
# Quick evaluation
python -m procurement_ai.evaluation.run

# Save as baseline for future comparisons
python -m procurement_ai.evaluation.run --save-baseline

# Save results to specific file
python -m procurement_ai.evaluation.run --output results.json --markdown report.md
````

---

This article is based on the evaluation framework built for a real procurement AI system. All code examples are production-ready and tested. The complete implementation is available in `src/procurement_ai/evaluation/`.

---

## Ready to Build Production AI Systems?

This evaluation framework is just one piece of building reliable AI agents. If you're:

- **Deploying LLM agents to production** and need help with testing strategies
- **Building AI systems** for regulated industries (banking, defense, healthcare)
- **Struggling with AI reliability** and want systematic approaches to quality assurance
- **Setting up CI/CD for AI** and need guidance on quality gates and metrics

I offer **technical consulting and security architecture reviews** drawing on 15+ years of experience across banking, defense, aerospace, and automotive systems. Let's discuss your specific challenges.

**[Schedule a consultation](/consultation/)** or connect on [LinkedIn](https://www.linkedin.com/in/aminebennaji/) to explore how I can help.

---

## Continue the LLM Engineering Series

This is Part 4 of a comprehensive series on building production LLM systems:

- **[Part 1: Building a Procurement Analyst AI](/posts/LLM-engineering-building-a-procurements-analyst-ai/)** — Initial implementation, schema design, and basic agent architecture
- **[Part 2: Production-Ready LLM Agents](/posts/Build-production-ready-llam-agents/)** — Architecting for reliability, error handling, and observability patterns
- **[Part 3: From MVP to Production SaaS](/posts/from-mvp-to-prod/)** — Multi-tenancy, database persistence, and deployment strategies
- **Part 4: Evaluating AI Agents** (you are here) — Testing, metrics, and quality assurance

Each article builds on the previous, taking you from prototype to production-ready system.

---

**Thanks for reading.** If you found this valuable, share it with your team or star the repo.
