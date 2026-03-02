#!/usr/bin/env python3
"""
Report Generator & Web Server
生成评估报告的网页
"""

import json
import os
from flask import Flask, render_template_string, jsonify, request
from datetime import datetime

app = Flask(__name__)

# 读取 HTML 模板
TEMPLATE_PATH = "/home/jlpeng/.openclaw/workspace/bonus_hunter/reports/template.html"

with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    HTML_TEMPLATE = f.read()

# 模拟数据（实际使用时会从数据库读取）
SAMPLE_EVALUATION = {
    "employee_id": 1,
    "employee_name": "王小明",
    "department": "研發部",
    "position": "資深工程師",
    "evaluation_date": "2026-03-01",
    "dimensions": {
        "context_judgment": {
            "score": 85,
            "evidence_count": 5,
            "summary": "員工能夠清晰分析情況並做出合理決策"
        },
        "exception_handling": {
            "score": 78,
            "evidence_count": 3,
            "summary": "遇到問題時能夠快速定位問題根源"
        },
        "risk_anticipation": {
            "score": 72,
            "evidence_count": 2,
            "summary": "會考慮潛在風險並做好準備"
        },
        "collaboration": {
            "score": 88,
            "evidence_count": 4,
            "summary": "注重團隊協作，有效溝通"
        }
    },
    "overall_assessment": "該員工展現出良好的工作能力和潛力，特別在團隊協作方面表現突出。建議給予更多帶領專案的機會。",
    "strengths": [
        "決策清晰果斷",
        "團隊合作積極",
        "善於溝通協調",
        "技術能力強"
    ],
    "development_areas": [
        "可以加強風險預判能力",
        "建議多參與跨部門專案"
    ]
}

SAMPLE_EVIDENCE = [
    {
        "dimension": "CONTEXT_JUDGMENT",
        "dimension_class": "ctx",
        "skill": "優先順序判斷",
        "quote": "我會先看客戶的緊急程度，然後跟老闆確認時程",
        "confidence": 0.85
    },
    {
        "dimension": "EXCEPTION_HANDLING",
        "dimension_class": "exc",
        "skill": "問題根因分析",
        "quote": "我先看 log 找到錯誤訊息，然後 google 解決方案",
        "confidence": 0.78
    },
    {
        "dimension": "COLLABORATION",
        "dimension_class": "collab",
        "skill": "跨部門溝通",
        "quote": "我會先跟 PM 確認需求，然後再跟 RD 開會討論技術細節",
        "confidence": 0.92
    },
    {
        "dimension": "RISK_ANTICIPATION",
        "dimension_class": "risk",
        "skill": "風險評估",
        "quote": "我有考慮到如果 API 壞掉怎麼辦，所以做了 fallback 機制",
        "confidence": 0.75
    }
]

def generate_report_html(evaluation: dict, evidence: list = None) -> str:
    """生成报告 HTML"""
    
    dim = evaluation.get("dimensions", {})
    
    # 准备模板数据
    context = {
        "employee_name": evaluation.get("employee_name", "N/A"),
        "department": evaluation.get("department", "N/A"),
        "position": evaluation.get("position", "N/A"),
        "evaluation_date": evaluation.get("evaluation_date", "N/A"),
        
        # Scores
        "context_score": dim.get("context_judgment", {}).get("score", 0),
        "context_count": dim.get("context_judgment", {}).get("evidence_count", 0),
        
        "exception_score": dim.get("exception_handling", {}).get("score", 0),
        "exception_count": dim.get("exception_handling", {}).get("evidence_count", 0),
        
        "risk_score": dim.get("risk_anticipation", {}).get("score", 0),
        "risk_count": dim.get("risk_anticipation", {}).get("evidence_count", 0),
        
        "collaboration_score": dim.get("collaboration", {}).get("score", 0),
        "collaboration_count": dim.get("collaboration", {}).get("evidence_count", 0),
        
        # Assessment
        "overall": evaluation.get("overall_assessment", ""),
        "strengths": evaluation.get("strengths", []),
        "areas": evaluation.get("development_areas", []),
        
        # Evidence
        "evidence": evidence or SAMPLE_EVIDENCE,
        
        # Generated date
        "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return render_template_string(HTML_TEMPLATE, **context)

# ==================== Routes ====================

@app.route('/')
def index():
    """首页"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>獎金獵人 - Demo</title>
        <style>
            body { font-family: -apple-system, sans-serif; padding: 40px; background: #f5f7fa; }
            .container { max-width: 600px; margin: 0 auto; }
            .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
            h1 { color: #667eea; }
            .btn { display: inline-block; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 8px; margin: 10px 5px; }
            .btn:hover { background: #5568d3; }
            .info { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1>🏆 獎金獵人 Demo</h1>
                <p>AI Employee Capability Evaluation System</p>
                
                <div class="info">
                    <h3>功能展示：</h3>
                    <ul>
                        <li>📱 WhatsApp 對話介面</li>
                        <li>🤖 Companion Agent</li>
                        <li>🔍 Evidence Extraction</li>
                        <li>📊 評估報告</li>
                    </ul>
                </div>
                
                <a href="/report/demo" class="btn">查看 Demo 評估報告</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/report')
@app.route('/report/<name>')
def report(name=None):
    """评估报告页面"""
    # 这里应该从数据库读取真实数据
    # 现在用演示数据
    if name == "demo":
        evaluation = SAMPLE_EVALUATION
        evidence = SAMPLE_EVIDENCE
    else:
        evaluation = SAMPLE_EVALUATION
        evidence = SAMPLE_EVIDENCE
    
    return generate_report_html(evaluation, evidence)

@app.route('/api/employee/<int:employee_id>')
def api_employee(employee_id):
    """获取员工评估数据 API"""
    # 这里应该从数据库读取
    return jsonify(SAMPLE_EVALUATION)

# ==================== Main ====================

if __name__ == "__main__":
    print("=" * 50)
    print("🏆 獎金獵人 - 報告伺服器")
    print("📍 http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
