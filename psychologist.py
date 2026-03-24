#!/usr/bin/env python3
"""
AI Psychologist Agent - CLI Application
A conversational AI that simulates a psychological consultation session.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()


class PsychologicalConsultation:
    """
    Manages the structure and flow of a psychological consultation session.
    Follows professional psychological counseling stages.
    """

    STAGES = {
        1: {
            "name": "Initial Rapport & Introduction",
            "description": "Building trust and explaining the process",
            "prompt": "Welcome to our session. I'm here to help you explore your thoughts and feelings in a safe, confidential space. Before we begin, I'd like to explain how our sessions work: everything you share is confidential. This is a space where you can speak freely without judgment. Take a moment to settle in, and when you're ready, please tell me what's on your mind or what brought you here today. How are you feeling right now?"
        },
        2: {
            "name": "Problem Assessment",
            "description": "Understanding the patient's primary concerns",
            "prompt": "Thank you for sharing that with me. I'd like to understand more about what you're experiencing. Can you tell me more about this? When did you first notice these feelings or situations? How has it been affecting your daily life, relationships, or well-being?"
        },
        3: {
            "name": "Exploration & Deep Understanding",
            "description": "Diving deeper into the root causes and patterns",
            "prompt": "I appreciate your openness. Let's explore this further. Can you help me understand more about what triggers these feelings? Are there specific situations, memories, or thoughts that come up? How have you been coping with these challenges so far?"
        },
        4: {
            "name": "Insight & Reflection",
            "description": "Helping patient gain new perspectives",
            "prompt": "What you've shared is very important. I'd like to reflect some things back to you. [INSIGHT] As you describe this, I'm noticing some patterns. What are your thoughts on how these experiences might be connected? What have you learned about yourself through all of this?"
        },
        5: {
            "name": "Goal Setting",
            "description": "Defining what the patient wants to achieve",
            "prompt": "As we work together, it helps to have a sense of direction. What would you like to achieve from our sessions? What would your life look like if things were better? What changes would you like to see, and what feels most important to address first?"
        },
        6: {
            "name": "Intervention & Guidance",
            "description": "Providing therapeutic techniques and strategies",
            "prompt": "Based on what you've shared, I'd like to offer some perspectives and techniques that might help. [INTERVENTION] I'd also like to suggest some things you might try between now and our next session. Would you be open to exploring some coping strategies or ways to address these challenges?"
        },
        7: {
            "name": "Session Conclusion",
            "description": "Summarizing and planning next steps",
            "prompt": "As we begin to wrap up our session today, I'd like to summarize what we've discussed. [SUMMARY] How are you feeling about what we covered today? Is there anything else you'd like to share before we conclude? Remember, you can reach out anytime before our next session if you need support."
        }
    }

    def __init__(self):
        self.current_stage = 1
        self.conversation_history = []
        self.patient_name = None
        self.concerns = []
        self.goals = []

    def get_stage_prompt(self) -> str:
        """Get the prompt for the current consultation stage."""
        return self.STAGES[self.current_stage]["prompt"]

    def get_stage_name(self) -> str:
        """Get the name of the current stage."""
        return self.STAGES[self.current_stage]["name"]

    def advance_stage(self):
        """Move to the next consultation stage."""
        if self.current_stage < 7:
            self.current_stage += 1
            return True
        return False

    def can_advance(self) -> bool:
        """Check if we can advance to the next stage."""
        return self.current_stage < 7


class AIPsychologist:
    """
    AI Psychologist using Claude API for therapeutic conversations.
    """

    # Anthropic API Key - Sonnet 4.6 model
    # IMPORTANT: Set ANTHROPIC_API_KEY environment variable before running
    # Get your API key from: https://console.anthropic.com/
    API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    MODEL = "claude-sonnet-4-20250514"

    SYSTEM_PROMPT = """You are a compassionate, professional psychologist with many years of clinical experience. Your approach combines evidence-based therapeutic techniques with genuine empathy and warmth.

Your core values and practices:
1. ACTIVE LISTENING - Pay close attention to what the patient says, including emotions behind words
2. EMPATHIC RESPONSE - Validate feelings and show understanding
3. NON-JUDGMENTAL - Create a safe space without judgment
4. PROFESSIONAL BOUNDARIES - Maintain appropriate therapeutic boundaries
5. EVIDENCE-BASED - Use proven psychological techniques (CBT, mindfulness, person-centered therapy)
6. PATIENT-CENTERED - Follow the patient's pace and lead the conversation appropriately

Communication guidelines:
- Use warm, conversational language
- Ask thoughtful follow-up questions
- Reflect back what you hear to show understanding
- Don't rush to give advice - explore first
- Acknowledge emotions before problem-solving
- Use silence when appropriate - give patient time to think
- Be genuine and human in your responses

Remember: Your role is to help patients explore their thoughts and feelings, gain insights, and develop coping strategies. You are a guide and support, not a doctor prescribing medication."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=self.API_KEY)
        self.consultation = PsychologicalConsultation()
        self.conversation_history = []

    def _build_context(self, user_message: str) -> str:
        """Build the context for the AI response."""
        # Include consultation stage info
        stage_info = f"""
CURRENT CONSULTATION STAGE: {self.consultation.get_stage_name()}

Stage-specific guidance: {self.consultation.STAGES[self.consultation.current_stage]['description']}

Stage prompt to incorporate: {self.consultation.get_stage_prompt()}
"""

        # Build conversation context
        context = stage_info + "\n\nCONVERSATION HISTORY:\n"
        for msg in self.conversation_history[-10:]:  # Last 10 exchanges
            context += f"{msg['role'].upper()}: {msg['content']}\n\n"

        context += f"\nPATIENT'S LATEST MESSAGE: {user_message}"

        return context

    def _generate_response(self, user_message: str) -> str:
        """Generate a therapeutic response using Claude."""
        context = self._build_context(user_message)

        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=1024,
            system=self.SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": context
                }
            ]
        )

        return response.content[0].text

    def _should_advance_stage(self, user_message: str, ai_response: str) -> bool:
        """
        Determine if the consultation should advance to the next stage.
        Advance when:
        - Patient has shared significant information
        - Current stage's purpose seems fulfilled
        - Natural transition point in conversation
        """
        combined_text = (user_message + " " + ai_response).lower()

        # Stage advancement indicators
        stage_indicators = {
            1: ["thank", "welcome", "ready", "here because", "came to", "want to talk"],
            2: ["started", "began", "when", "first", "affect", "impact", "feelings"],
            3: ["trigger", "why", "because", "remember", "think", "cope", "deal with"],
            4: ["understand", "realize", "notice", "pattern", "connection", "insight"],
            5: ["want to", "goal", "hope", "would like", "wish", "change", "improve"],
            6: ["try", "will", "practice", "work on", "implement", "strategy"]
        }

        current_indicators = stage_indicators.get(self.consultation.current_stage, [])
        matches = sum(1 for indicator in current_indicators if indicator in combined_text)

        # Advance if we have enough indicators and minimum conversation depth
        return matches >= 2 and len(self.conversation_history) >= 2

    def chat(self, user_message: str) -> str:
        """Process a patient message and return therapist response."""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Generate AI response
        ai_response = self._generate_response(user_message)

        # Add AI response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": ai_response
        })

        # Check if we should advance to the next stage
        if self.consultation.can_advance():
            if self._should_advance_stage(user_message, ai_response):
                self.consultation.advance_stage()

        return ai_response

    def get_current_stage(self) -> str:
        """Get the current consultation stage."""
        return self.consultation.get_stage_name()


def print_welcome():
    """Print welcome message and instructions."""
    print("=" * 60)
    print("       🧠 AI PSYCHOLOGIST - Safe Space for Your Mind")
    print("=" * 60)
    print()
    print("Welcome! I'm here to provide a supportive, confidential")
    print("space for you to explore your thoughts and feelings.")
    print()
    print("📋 GUIDELINES:")
    print("  • This is a safe, non-judgmental space")
    print("  • Share as much or as little as you'd like")
    print("  • Type '\\exit' anytime to end the session")
    print("  • There's no right or wrong way to feel")
    print()
    print("-" * 60)
    print()


def print_goodbye():
    """Print goodbye message."""
    print()
    print("=" * 60)
    print("        Thank you for trusting me with your story")
    print("=" * 60)
    print()
    print("Remember: Your feelings are valid, and seeking support")
    print("is a sign of strength. Take care of yourself.")
    print()
    print("Type '\\restart' to begin a new session anytime.")
    print("=" * 60)
    print()


def main():
    """Main CLI loop."""
    print_welcome()

    psychologist = AIPsychologist()

    # Initial greeting from the psychologist
    print("🧠 Psychologist:", psychologist.chat("Start session"))
    print()

    # Main conversation loop
    while True:
        try:
            user_input = input("You: ").strip()

            # Handle exit commands
            if user_input.lower() in ['\\exit', 'exit', 'quit', 'q']:
                print_goodbye()
                break

            # Handle restart
            if user_input.lower() in ['\\restart', 'restart']:
                print("\n" + "=" * 60)
                print("Starting a new session...")
                print("=" * 60 + "\n")
                psychologist = AIPsychologist()
                print("🧠 Psychologist:", psychologist.chat("Start new session"))
                print()
                continue

            # Skip empty input
            if not user_input:
                continue

            # Get psychologist's response
            response = psychologist.chat(user_input)
            print(f"\n🧠 Psychologist: {response}")
            print()

            # Show current stage occasionally
            if len(psychologist.conversation_history) % 6 == 0:
                stage = psychologist.get_current_stage()
                print(f"   [Session Progress: {stage}]")
                print()

        except KeyboardInterrupt:
            print("\n")
            print_goodbye()
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again or type '\\exit' to end the session.\n")


if __name__ == "__main__":
    main()
