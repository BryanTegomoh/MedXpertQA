"""
Explore the MedXpertQA dataset from local JSONL files.
"""

import json
import os

def load_jsonl(filepath):
    """Load a JSONL file and return list of dictionaries."""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

def explore_questions():
    # Paths to local data
    base_path = os.path.dirname(os.path.abspath(__file__))
    text_path = os.path.join(base_path, "eval", "data", "medxpertqa", "input", "medxpertqa_text_input.jsonl")
    mm_path = os.path.join(base_path, "eval", "data", "medxpertqa", "input", "medxpertqa_mm_input.jsonl")
    
    print("=" * 70)
    print("MedXpertQA Dataset Explorer")
    print("=" * 70)
    
    # Load data
    print("\n📥 Loading local data...")
    text_questions = load_jsonl(text_path)
    mm_questions = load_jsonl(mm_path)
    
    print(f"   ✅ Text questions: {len(text_questions)}")
    print(f"   ✅ MM (Multimodal) questions: {len(mm_questions)}")
    print(f"   📊 Total: {len(text_questions) + len(mm_questions)} questions")
    
    # Show sample structure
    print("\n" + "=" * 70)
    print("Question Structure (Sample)")
    print("=" * 70)
    
    sample = text_questions[0]
    print(f"\nFields available: {list(sample.keys())}")
    
    # Print one full example
    print("\n" + "-" * 70)
    print("Example Question:")
    print("-" * 70)
    print(f"ID: {sample['id']}")
    print(f"Medical Task: {sample.get('medical_task', 'N/A')}")
    print(f"Body System: {sample.get('body_system', 'N/A')}")
    print(f"Question Type: {sample.get('question_type', 'N/A')}")
    print(f"\nQuestion:\n{sample['question'][:500]}...")
    print(f"\nOptions:")
    for i, opt in enumerate(sample.get('options', [])):
        opt_str = str(opt) if not isinstance(opt, str) else opt
        print(f"   {chr(65+i)}. {opt_str[:100]}{'...' if len(opt_str) > 100 else ''}")
    print(f"\nAnswer: {sample.get('label', 'N/A')}")
    
    # Statistics
    print("\n" + "=" * 70)
    print("Statistics")
    print("=" * 70)
    
    all_questions = text_questions + mm_questions
    
    # By medical task
    tasks = {}
    for q in all_questions:
        task = q.get('medical_task', 'Unknown')
        tasks[task] = tasks.get(task, 0) + 1
    
    print("\n📋 By Medical Task:")
    for task, count in sorted(tasks.items(), key=lambda x: -x[1]):
        print(f"   {task}: {count}")
    
    # By body system
    systems = {}
    for q in all_questions:
        system = q.get('body_system', 'Unknown')
        systems[system] = systems.get(system, 0) + 1
    
    print("\n🫀 By Body System:")
    for system, count in sorted(systems.items(), key=lambda x: -x[1]):
        print(f"   {system}: {count}")
    
    # Export all questions to readable format
    output_file = os.path.join(base_path, "all_questions_readable.txt")
    print(f"\n💾 Exporting all questions to: all_questions_readable.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, q in enumerate(all_questions):
            f.write("=" * 70 + "\n")
            f.write(f"Question {i+1} [{q['id']}]\n")
            f.write(f"Task: {q.get('medical_task', 'N/A')} | System: {q.get('body_system', 'N/A')} | Type: {q.get('question_type', 'N/A')}\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"{q['question']}\n\n")
            f.write("Options:\n")
            for j, opt in enumerate(q.get('options', [])):
                opt_str = str(opt) if not isinstance(opt, str) else opt
                f.write(f"   {chr(65+j)}. {opt_str}\n")
            f.write(f"\nCorrect Answer: {q.get('label', 'N/A')}\n\n\n")
    
    print("   ✅ Done!")
    
    # Also export as JSON for programmatic access
    json_output = os.path.join(base_path, "all_questions.json")
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)
    print(f"💾 JSON export: all_questions.json")
    
    return text_questions, mm_questions

if __name__ == "__main__":
    text_q, mm_q = explore_questions()
    print("\n✨ Exploration complete! Check the output files.")
