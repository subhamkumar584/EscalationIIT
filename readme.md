# Causal Analysis and Interactive Reasoning over Conversational Data

## 1. Project Overview
This project implements an **end‑to‑end system** to explain **why outcome events**
(such as escalations) occur in customer–agent conversations.

Given a **natural‑language analytical query**, the system identifies
**dialogue‑level causal factors**, retrieves **supporting conversational evidence**,
and generates **interpretable explanations**. The system also supports
**multi‑turn follow‑up queries** by maintaining explicit session context.

---

## 2. Problem Statement

Large‑scale customer support systems generate multi‑turn conversations between
customers and agents. Some conversations result in important outcome events such
as escalations, complaints, or refunds. While these events are logged, existing
systems do not explain the **conversational causes** behind them.

The objective is to design a system that:
- Identifies **dialogue‑level causal factors**
- Grounds explanations in **concrete conversational evidence**
- Supports **interactive, multi‑turn reasoning**
- Produces **interpretable and reproducible outputs**

### Task 1: Query‑Driven Causal Explanation
Given a single natural‑language query, the system must analyze relevant
conversations, identify causal factors, retrieve supporting dialogue evidence,
and generate a structured explanation.

### Task 2: Multi‑Turn Context‑Aware Reasoning
The system must retain context across follow‑up queries and ensure consistency
in causal reasoning and evidence usage across multiple interactions.

---

## 3. Why This System Is Better Than Others

Compared to traditional systems, this approach:

- Goes beyond simple **event detection** to provide **causal explanations**
- Grounds explanations in **explicit conversational evidence**
- Supports **multi‑turn interactive reasoning**
- Uses **interpretable rule‑based logic** instead of black‑box models
- Is **fully reproducible** and **CPU‑only**

This makes the system more **transparent, trustworthy, and evaluator‑friendly**.

---

## 4. Technologies Used

| Technology | Purpose |
|----------|--------|
| Python | Core system implementation |
| Pandas | Data handling and CSV generation |
| NumPy | Numerical and vector operations |
| Sentence‑Transformers | Semantic text embeddings |
| FAISS (CPU) | Vector similarity search |
| Rule‑Based Causal Logic | Interpretable reasoning |
| Context Manager | Multi‑turn query handling |

---

## 5. Hardware Requirements
- CPU‑only environment  
- No GPU required  
- Sufficient RAM to store conversation embeddings  

---

## 6. Software Requirements
- Python **3.8 or higher**
- All dependencies listed in `requirements.txt`

```bash 
pip install -r requirements.txt
```
## 7. System Workflow
<ol type="I">
  <li>User submits a natural‑language analytical query</li>
  <li>Query intent is interpreted (new or follow‑up)</li>
  <li>Previous session context is retrieved if required</li>
  <li>Causal reasoning is applied over conversations</li>
  <li>Supporting dialogue evidence is retrieved</li>
    <li>Structured explanation is generated</li>
  <li> Evaluation metrics are computed</li>
  <li>Final output is returned and context is updatedFinal output is returned and context is updated</li>
   
</ol>

## 8. Sample Input and Output




## 9. Evaluation Metrics

| Metric       | Description |
|-------------|-------------|
| **IDRecall** | Accuracy of retrieved conversational evidence |
| **Faithfulness** | Ensures explanations are grounded in retrieved context (no hallucinations) |
| **Relevancy** | Alignment with user intent, especially in multi‑turn queries |

## 10. Folder Structure

```
├── src/
│   ├── main.py              # Entry point for interactive execution
│   ├── batch_eval.py        # Automated batch evaluation script
│   ├── reasoning/           # Core causal reasoning and inference logic
│   ├── retrieval/           # Evidence retrieval and document fetching
│   ├── context_manager/     # State handling for multi-turn dialogues
│   └── evaluation/          # Metrics computation (Recall, Precision, etc.)
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## 11. How to Run the System
### Interactive Mode
```python main.py```
### Batch Evaluation Mode (Used for Evaluation)
```python batch_eval.py```
This generates a CSV file containing:

- Query ID

- Query

- Query Category

- System Output

- Remarks

⚠️ This CSV file is used directly for evaluation.

## 12. Conclusion
This project demonstrates how causal reasoning, semantic retrieval, and
explicit context management can be combined to move beyond simple event
detection and enable interactive, evidence‑grounded causal analysis over
conversational data. The system is interpretable, reproducible, and well‑suited
for large‑scale conversational analysis.

## Notes for Evaluators
- No external APIs are used

- No GPU or paid services required

- Fully reproducible on CPU

- Deterministic and interpretable outputs
