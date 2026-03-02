#!/usr/bin/env python3
"""
Evidence Extraction & Evaluator Module
从对话中萃取行为信号并评估员工能力
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional
import re

# ==================== Database ====================

DB_PATH = "/home/jlpeng/.openclaw/workspace/bonus_hunter/data/evidence.db"

def init_db():
    """初始化数据库"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 员工资料表
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT,
        position TEXT,
        cv_summary TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 对话记录表
    c.execute('''CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        role TEXT,
        content TEXT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )''')
    
    # 行为信号萃取表
    c.execute('''CREATE TABLE IF NOT EXISTS evidence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        dimension TEXT,
        inferred_skill TEXT,
        supporting_quote TEXT,
        confidence REAL,
        conversation_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES employees(id),
        FOREIGN KEY (conversation_id) REFERENCES conversations(id)
    )''')
    
    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成")

# ==================== Evidence Extraction ====================

EVIDENCE_EXTRACTION_PROMPT = '''You are an evaluation signal extraction engine. 

Analyze the following conversation between an employee and a companion AI.

Your task: Identify whether the employee demonstrated behavior related to one of these dimensions:
- CONTEXT_JUDGMENT
- EXCEPTION_HANDLING  
- RISK_ANTICIPATION
- COLLABORATION

If relevant behavior exists, extract:
1. dimension (one of the four)
2. inferred_skill (short phrase, max 10 words)
3. supporting_quote (exact quote from employee)
4. confidence (0.0 to 1.0)

If no clear signal exists, return null.

Output strictly in JSON format:
{
  "dimension": "...",
  "inferred_skill": "...",
  "supporting_quote": "...",
  "confidence": 0.0
}

Conversation:
{conversation}

Output only JSON, no other text:'''

def extract_evidence(conversation: str, llm_api_func=None) -> Optional[Dict]:
    """
    从对话中萃取行为信号
    
    Args:
        conversation: 对话内容
        llm_api_func: LLM API 调用函数（如果没有，会返回示例）
    
    Returns:
        Dict with dimension, inferred_skill, supporting_quote, confidence
    """
    prompt = EVIDENCE_EXTRACTION_PROMPT.format(conversation=conversation)
    
    # 如果提供了 LLM API，调用它
    if llm_api_func:
        try:
            result = llm_api_func(prompt)
            return json.loads(result)
        except:
            pass
    
    # 否则返回模拟数据（Demo用）
    return None

# ==================== Employee Management ====================

def add_employee(name: str, department: str = "", position: str = "", cv_summary: str = "") -> int:
    """新增员工"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO employees (name, department, position, cv_summary) VALUES (?, ?, ?, ?)",
        (name, department, position, cv_summary)
    )
    employee_id = c.lastrowid
    conn.commit()
    conn.close()
    return employee_id

def get_employee(employee_id: int) -> Optional[Dict]:
    """获取员工信息"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

# ==================== Conversation ====================

def add_conversation(employee_id: int, role: str, content: str) -> int:
    """新增对话记录"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO conversations (employee_id, role, content) VALUES (?, ?, ?)",
        (employee_id, role, content)
    )
    conv_id = c.lastrowid
    conn.commit()
    conn.close()
    return conv_id

def get_conversations(employee_id: int, limit: int = 10) -> List[Dict]:
    """获取对话记录"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        "SELECT * FROM conversations WHERE employee_id = ? ORDER BY timestamp DESC LIMIT ?",
        (employee_id, limit)
    )
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ==================== Evidence ====================

def add_evidence(employee_id: int, dimension: str, inferred_skill: str, 
                  supporting_quote: str, confidence: float, conversation_id: int) -> int:
    """新增行为信号"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """INSERT INTO evidence 
           (employee_id, dimension, inferred_skill, supporting_quote, confidence, conversation_id) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        (employee_id, dimension, inferred_skill, supporting_quote, confidence, conversation_id)
    )
    evidence_id = c.lastrowid
    conn.commit()
    conn.close()
    return evidence_id

def get_evidence(employee_id: int) -> List[Dict]:
    """获取行为信号"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        "SELECT * FROM evidence WHERE employee_id = ? ORDER BY created_at DESC",
        (employee_id,)
    )
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ==================== Evaluator ====================

EVALUATOR_PROMPT = '''You are a professional employee capability evaluator AI.

You receive:
1. Static employee profile (CV and work history summary)
2. Dynamic behavioral evidence logs extracted from daily interactions

Your goal: Continuously update a structured capability assessment.

Output format (JSON):
{{
  "employee_id": "...",
  "evaluation_date": "...",
  "dimensions": {{
    "context_judgment": {{
      "score": 0-100,
      "evidence_count": N,
      "summary": "..."
    }},
    "exception_handling": {{
      "score": 0-100,
      "evidence_count": N,
      "summary": "..."
    }},
    "risk_anticipation": {{
      "score": 0-100,
      "evidence_count": N,
      "summary": "..."
    }},
    "collaboration": {{
      "score": 0-100,
      "evidence_count": N,
      "summary": "..."
    }}
  }},
  "overall_assessment": "...",
  "strengths": [...],
  "development_areas": [...]
}}

Employee Profile:
{profile}

Evidence Logs:
{evidence_logs}

Output only JSON, no other text:'''

def generate_evaluation(employee_id: int, llm_api_func=None) -> Dict:
    """
    产生员工评估报告
    
    Args:
        employee_id: 员工 ID
        llm_api_func: LLM API 调用函数
    
    Returns:
        评估报告 JSON
    """
    # 获取员工资料
    employee = get_employee(employee_id)
    if not employee:
        return {"error": "Employee not found"}
    
    # 获取行为信号
    evidence = get_evidence(employee_id)
    
    # 构建 prompt
    profile = f"Name: {employee['name']}, Department: {employee['department']}, Position: {employee['position']}, CV: {employee['cv_summary']}"
    
    evidence_logs = "\n".join([
        f"- {e['dimension']}: {e['inferred_skill']} (confidence: {e['confidence']})"
        for e in evidence
    ])
    
    prompt = EVALUATOR_PROMPT.format(profile=profile, evidence_logs=evidence_logs)
    
    # 如果有 LLM，调用它
    if llm_api_func:
        try:
            result = llm_api_func(prompt)
            return json.loads(result)
        except:
            pass
    
    # 否则返回模拟评估
    return generate_mock_evaluation(employee, evidence)

def generate_mock_evaluation(employee: Dict, evidence: List[Dict]) -> Dict:
    """生成模拟评估（Demo用）"""
    
    # 统计各维度的信号数量
    dimensions = {
        "context_judgment": 0,
        "exception_handling": 0,
        "risk_anticipation": 0,
        "collaboration": 0
    }
    
    for e in evidence:
        dim = e.get("dimension", "").lower()
        if dim in dimensions:
            dimensions[dim] += 1
    
    # 计算分数（模拟）
    def calc_score(count):
        return min(50 + count * 15, 95)
    
    return {
        "employee_id": employee["id"],
        "employee_name": employee["name"],
        "evaluation_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "dimensions": {
            "context_judgment": {
                "score": calc_score(dimensions["context_judgment"]),
                "evidence_count": dimensions["context_judgment"],
                "summary": "员工能够清晰分析情况并做出合理决策"
            },
            "exception_handling": {
                "score": calc_score(dimensions["exception_handling"]),
                "evidence_count": dimensions["exception_handling"],
                "summary": "遇到问题时能够快速定位问题根源"
            },
            "risk_anticipation": {
                "score": calc_score(dimensions["risk_anticipation"]),
                "evidence_count": dimensions["risk_anticipation"],
                "summary": "会考虑潜在风险并做好准备"
            },
            "collaboration": {
                "score": calc_score(dimensions["collaboration"]),
                "evidence_count": dimensions["collaboration"],
                "summary": "注重团队协作，有效沟通"
            }
        },
        "overall_assessment": "该员工展现出良好的工作能力和潜力",
        "strengths": [
            "决策清晰",
            "问题解决能力强的"
        ],
        "development_areas": [
            "可以加强风险预判能力"
        ],
        "note": "这是模拟评估，实际使用需要接入 LLM API"
    }

# ==================== Main ====================

if __name__ == "__main__":
    # 初始化数据库
    init_db()
    
    # 测试：新增员工
    emp_id = add_employee("测试员工", "研发部", "工程师", "5年工作经验")
    print(f"✅ 新增员工 ID: {emp_id}")
    
    # 测试：新增对话
    conv_id = add_conversation(emp_id, "user", "我今天处理了一个紧急的客户问题")
    conv_id = add_conversation(emp_id, "assistant", "很好，请问你如何决定的？")
    print(f"✅ 新增对话 ID: {conv_id}")
    
    # 测试：评估
    result = generate_evaluation(emp_id)
    print("\n📊 评估结果：")
    print(json.dumps(result, indent=2, ensure_ascii=False))
