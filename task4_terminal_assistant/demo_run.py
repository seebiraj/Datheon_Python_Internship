"""
Demonstration runner for Task 4: Rule-Based Interactive Terminal Assistant.
Simulates realistic conversational queries across multi-intent taxonomy, fallbacks, and exit.
"""

from chatbot import RuleBasedChatbot, DialogueState


def run_chatbot_demo():
    print("\n--- Running Rule-Based Terminal Chatbot Simulation ---")
    bot = RuleBasedChatbot()

    test_conversations = [
        ("Hello there!", "greeting"),
        ("What are your business operating hours?", "business_hours"),
        ("Tell me about the Datheon Python internship and certification", "datheon_internship"),
        ("How much does the program cost?", "pricing_discounts"),
        ("What is your refund policy?", "refund_returns"),
        ("My python code has an error and crashed", "technical_support"),
        ("Can I talk to a human agent?", "contact_agent"),
        ("Can you bake a chocolate cake on Mars?", "fallback"),
        ("Show me the topics menu", "help_topics"),
        ("Thank you, bye!", "goodbye")
    ]

    for user_query, expected_intent in test_conversations:
        tag, response = bot.match_intent(user_query)
        print(f"User : {user_query}")
        print(f"Intent Recognized: [{tag}] (Expected: [{expected_intent}])")
        print(f"Bot  : {response}\n")
        assert tag == expected_intent, f"Expected intent '{expected_intent}', but got '{tag}'"

    assert bot.state == DialogueState.EXIT, "Chatbot should be in EXIT state after 'bye' query."
    print("Multi-intent recognition, dialogue state machine, and fallback handling validated successfully!")


if __name__ == "__main__":
    run_chatbot_demo()
