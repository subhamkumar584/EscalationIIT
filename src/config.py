import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATASET_PATH = os.path.join(PROJECT_ROOT, 'dataset', 'Conversational_Transcript_Dataset.json')
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, 'outputs')
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')


EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
EMBEDDING_DIMENSION = 384
TOP_K_RETRIEVE = 50
TOP_K_EVIDENCE = 3


SEMANTIC_WEIGHT = 0.6
KEYWORD_WEIGHT = 0.4

OUTCOME_MAPPING = {
    "ESCALATION": [
        "Escalation - Repeated Service Failures",
        "Escalation - Threat of Legal Action",
        "Escalation - Service Cancellation Threat",
        "Escalation - Unauthorized Account Closure",
        "Escalation - Medical Error Complaint"
    ],
    "CLAIM_DENIAL": ["Claim Denials"],
    "FRAUD": ["Fraud Alert Investigation"],
    "SERVICE_FAILURE": ["Service Interruptions"],
    "DELIVERY_ISSUE": ["Delivery Investigation"],
    "BUSINESS_EVENT": [
        "Business Event - System Outage",
        "Business Event - Product Recall",
        "Business Event - System Conversion Failure"
    ]
}
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

if __name__ == "__main__":
    print("="*60)
    print("CONFIGURATION SETTINGS")
    print("="*60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Dataset Path: {DATASET_PATH}")
    print(f"Dataset Exists: {os.path.exists(DATASET_PATH)}")
    print(f"Outputs Dir: {OUTPUTS_DIR}")
    print(f"Models Dir: {MODELS_DIR}")
    print(f"\nEmbedding Model: {EMBEDDING_MODEL}")
    print(f"Embedding Dimension: {EMBEDDING_DIMENSION}")
    print(f"\nRetrieval Settings:")
    print(f"  Top-K Retrieve: {TOP_K_RETRIEVE}")
    print(f"  Top-K Evidence: {TOP_K_EVIDENCE}")
    print(f"  Semantic Weight: {SEMANTIC_WEIGHT}")
    print(f"  Keyword Weight: {KEYWORD_WEIGHT}")
    print(f"\nOutcome Types: {list(OUTCOME_MAPPING.keys())}")
    print("="*60)