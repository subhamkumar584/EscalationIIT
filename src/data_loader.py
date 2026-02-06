import json
from typing import List, Dict, Optional
from collections import defaultdict
import config

class ConversationDataset:
    def __init__(self, json_path: str = None):
        if json_path is None:
            json_path = config.DATASET_PATH
        
        print("="*60)
        print("LOADING CONVERSATIONAL DATASET")
        print("="*60)
        print(f"Loading from: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.transcripts = data['transcripts']
        print(f"✓ Loaded {len(self.transcripts)} conversations")
        print("\nBuilding indexes...")
        self.id_to_transcript = self._build_id_index()
        print(f"✓ ID index: {len(self.id_to_transcript)} conversations")
        
        self.domain_index = self._build_domain_index()
        print(f"✓ Domain index: {len(self.domain_index)} domains")
        
        self.intent_index = self._build_intent_index()
        print(f"✓ Intent index: {len(self.intent_index)} intents")
        
        self.outcome_index = self._build_outcome_index()
        print(f"✓ Outcome index: {len(self.outcome_index)} outcome types")
        
        self._print_statistics()
        print("="*60)
        print("✓ Dataset ready!")
        print("="*60)
    
    def _build_id_index(self) -> Dict[str, Dict]:
        return {t['transcript_id']: t for t in self.transcripts}
    
    def _build_domain_index(self) -> Dict[str, List[str]]:
        index = defaultdict(list)
        for t in self.transcripts:
            index[t['domain']].append(t['transcript_id'])
        return dict(index)
    
    def _build_intent_index(self) -> Dict[str, List[str]]:
        index = defaultdict(list)
        for t in self.transcripts:
            index[t['intent']].append(t['transcript_id'])
        return dict(index)
    
    def _build_outcome_index(self) -> Dict[str, List[str]]:
        index = defaultdict(list)
        for outcome, intent_list in config.OUTCOME_MAPPING.items():
            for intent in intent_list:
                if intent in self.intent_index:
                    index[outcome].extend(self.intent_index[intent])
        
        return dict(index)
    
    def _print_statistics(self):
        print("\n" + "-"*60)
        print("DATASET STATISTICS")
        print("-"*60)
    
        print("\nDomains:")
        for domain, ids in sorted(self.domain_index.items(), 
                                  key=lambda x: len(x[1]), 
                                  reverse=True):
            print(f"  {domain}: {len(ids)} conversations")

        print("\nOutcome Events:")
        for outcome, ids in sorted(self.outcome_index.items(), 
                                   key=lambda x: len(x[1]), 
                                   reverse=True):
            print(f"  {outcome}: {len(ids)} conversations")
        
        lengths = [len(t['conversation']) for t in self.transcripts]
        print(f"\nConversation Lengths:")
        print(f"  Min: {min(lengths)} turns")
        print(f"  Max: {max(lengths)} turns")
        print(f"  Avg: {sum(lengths)/len(lengths):.1f} turns")
        print("-"*60)
    
    def get_conversation(self, transcript_id: str) -> Optional[Dict]:
        return self.id_to_transcript.get(transcript_id)
    
    def get_conversations_by_domain(self, domain: str) -> List[Dict]:
        ids = self.domain_index.get(domain, [])
        return [self.id_to_transcript[tid] for tid in ids]
    
    def get_conversations_by_intent(self, intent: str) -> List[Dict]:
        ids = self.intent_index.get(intent, [])
        return [self.id_to_transcript[tid] for tid in ids]
    
    def get_conversations_by_outcome(self, outcome: str) -> List[Dict]:
        ids = self.outcome_index.get(outcome, [])
        return [self.id_to_transcript[tid] for tid in ids]
    
    def get_all_conversations(self) -> List[Dict]:
        return self.transcripts
    
    def get_statistics(self) -> Dict:
        lengths = [len(t['conversation']) for t in self.transcripts]
        
        return {
            'total_conversations': len(self.transcripts),
            'total_domains': len(self.domain_index),
            'total_intents': len(self.intent_index),
            'total_outcome_types': len(self.outcome_index),
            'min_turns': min(lengths),
            'max_turns': max(lengths),
            'avg_turns': sum(lengths) / len(lengths),
            'domain_distribution': {
                domain: len(ids) for domain, ids in self.domain_index.items()
            },
            'outcome_distribution': {
                outcome: len(ids) for outcome, ids in self.outcome_index.items()
            }
        }
if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTING DATA LOADER")
    print("="*60 + "\n")
    dataset = ConversationDataset()
    print("\n" + "="*60)
    print("TEST 1: Get Single Conversation")
    print("="*60)
    all_ids = list(dataset.id_to_transcript.keys())
    sample_id = all_ids[0]
    conv = dataset.get_conversation(sample_id)
    print(f"Call ID: {conv['transcript_id']}")
    print(f"Domain: {conv['domain']}")
    print(f"Intent: {conv['intent']}")
    print(f"Reason: {conv['reason_for_call'][:100]}...")
    print(f"Turns: {len(conv['conversation'])}")
    print("\n" + "="*60)
    print("TEST 2: Get Conversations by Domain")
    print("="*60)
    healthcare_convs = dataset.get_conversations_by_domain('Healthcare Services')
    print(f"Healthcare conversations: {len(healthcare_convs)}")
    print(f"Sample: {healthcare_convs[0]['transcript_id']}")
    print("\n" + "="*60)
    print("TEST 3: Get Conversations by Outcome")
    print("="*60)
    escalations = dataset.get_conversations_by_outcome('ESCALATION')
    print(f"ESCALATION conversations: {len(escalations)}")
    if escalations:
        print(f"Sample escalation:")
        print(f"  ID: {escalations[0]['transcript_id']}")
        print(f"  Intent: {escalations[0]['intent']}")
        print(f"  Reason: {escalations[0]['reason_for_call'][:100]}...")
    print("\n" + "="*60)
    print("TEST 4: Get Statistics")
    print("="*60)
    stats = dataset.get_statistics()
    print(f"Total conversations: {stats['total_conversations']}")
    print(f"Domains: {stats['total_domains']}")
    print(f"Intents: {stats['total_intents']}")
    print(f"Outcome types: {stats['total_outcome_types']}")
    print("\n" + "="*60)
    print("TEST 5: Sample Conversation Content")
    print("="*60)
    sample_conv = escalations[0] if escalations else dataset.transcripts[0]
    print(f"Call ID: {sample_conv['transcript_id']}")
    print(f"\nFirst 5 turns:")
    for i, turn in enumerate(sample_conv['conversation'][:5], 1):
        print(f"\n{i}. [{turn['speaker']}]:")
        print(f"   {turn['text'][:150]}...")
    
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED!")
    print("="*60)