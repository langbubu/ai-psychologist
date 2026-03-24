# 🤖 AI Psychologist

An AI-powered psychological consultation agent that provides a safe, confidential space for exploring thoughts and feelings. Built with Claude Sonnet 4.6 for empathetic, evidence-based therapeutic conversations.

## Features

- **Professional Consultation Framework**: Follows a structured 7-stage psychological consultation process similar to real therapy sessions
- **Evidence-Based Approach**: Combines CBT, mindfulness, and person-centered therapy techniques
- **Active Listening**: The AI listens attentively and responds with empathy and understanding
- **Safe & Confidential**: Non-judgmental space for open conversation
- **Easy Exit**: Type `\exit` anytime to end the session

## The 7-Stage Consultation Process

1. **Initial Rapport & Introduction** - Building trust and explaining the process
2. **Problem Assessment** - Understanding primary concerns
3. **Exploration & Deep Understanding** - Diving into root causes and patterns
4. **Insight & Reflection** - Helping gain new perspectives
5. **Goal Setting** - Defining what the patient wants to achieve
6. **Intervention & Guidance** - Providing therapeutic techniques
7. **Session Conclusion** - Summarizing and planning next steps

## Requirements

- Python 3.8+
- Anthropic API (Claude Sonnet 4.6)

## Installation

1. Clone or download this repository

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the psychologist agent:

```bash
python psychologist.py
```

### Available Commands

- `\exit` - End the current session
- `\restart` - Start a new consultation session
- `Ctrl+C` - Interrupt and exit

### Example Session

```
============================================================
       🧠 AI PSYCHOLOGIST - Safe Space for Your Mind
============================================================

Welcome! I'm here to provide a supportive, confidential
space for you to explore your thoughts and feelings.

📋 GUIDELINES:
  • This is a safe, non-judgmental space
  • Share as much or as little as you'd like
  • Type '\exit' anytime to end the session
  • There's no right or wrong way to feel

------------------------------------------------------------

🧠 Psychologist: Welcome to our session. I'm here to help you explore your thoughts and feelings in a safe, confidential space. Before we begin, I'd like to explain how our sessions work: everything you share is confidential. This is a space where you can speak freely without judgment. Take a moment to settle in, and when you're ready, please tell me what's on your mind or what brought you here today. How are you feeling right now?

You: I've been feeling very anxious lately
...
```

## Configuration

The AI uses Claude Sonnet 4.6 model with the following settings:

- **API Key**: Pre-configured (sk-ant-api03-...)
- **Model**: claude-sonnet-4-20250514
- **Max Tokens**: 1024 per response

## Important Notes

⚠️ **Disclaimer**: This AI psychologist is for educational and supportive purposes only. It is not a substitute for professional mental health care. If you're experiencing a mental health crisis, please contact:

- **National Suicide Prevention Lifeline**: 988 (US)
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911 (US) or your local emergency number

## Therapeutic Approach

The AI combines multiple evidence-based techniques:

- **Person-Centered Therapy**: Unconditional positive regard
- **Cognitive Behavioral Therapy (CBT)**: Identifying thought patterns
- **Mindfulness**: Present-moment awareness
- **Motivational Interviewing**: Exploring ambivalence
- **Psychodynamic Insights**: Understanding unconscious patterns

## License

MIT License

---

*Remember: Taking care of your mental health is important. You're brave for seeking support.*
