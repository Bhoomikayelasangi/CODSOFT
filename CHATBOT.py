def simple_chatbot():
    # Dictionary of predefined rules and responses
    responses = {
        "hello": ["Hi there!", "Hello!", "Greetings!"],
        "how are you": ["I'm doing well, thank you!", "I'm great, how are you?", "All good, thanks for asking!"],
        "bye": ["Goodbye!", "See you later!", "Have a great day!"],
        "name": ["I'm ChatBot, nice to meet you!", "You can call me ChatBot.", "I go by ChatBot!"],
        "help": ["I can help with basic conversation. Try saying hello, asking how I am, or asking my name!",
                "I'm a simple chatbot. I can chat about basic topics!"],
        "weather": ["I can't actually check the weather, but I hope it's nice outside!",
                   "I'm not connected to weather services, but maybe look outside?"],
        "time": ["I don't have access to the current time.",
                "I can't tell you the exact time, sorry!"]
    }

    # Keywords for different types of questions
    question_keywords = {
        "what": ["what", "what's", "whats"],
        "how": ["how", "how's", "hows"],
        "when": ["when", "when's", "whens"],
        "where": ["where", "where's", "wheres"],
        "who": ["who", "who's", "whos"],
        "why": ["why", "why's", "whys"]
    }

    import random

    print("ChatBot: Hello! I'm a simple chatbot. Type 'quit' to exit.")
    
    while True:
        # Get user input and convert to lowercase
        user_input = input("You: ").lower().strip()
        
        # Check if user wants to quit
        if user_input == 'quit':
            print("ChatBot: Goodbye! Have a nice day!")
            break
        
        # Flag to track if we found a matching response
        response_found = False
        
        # Check for exact matches in our responses dictionary
        for key in responses:
            if key in user_input:
                print("ChatBot:", random.choice(responses[key]))
                response_found = True
                break
        
        # If no exact match was found, check for question types
        if not response_found:
            for q_type, keywords in question_keywords.items():
                if any(keyword in user_input for keyword in keywords):
                    print(f"ChatBot: That's an interesting {q_type} question! "
                          "I'm still learning and can't answer complex questions yet.")
                    response_found = True
                    break
        
        # Default response if no pattern is matched
        if not response_found:
            default_responses = [
                "I'm not sure I understand. Could you rephrase that?",
                "That's interesting, but I'm not sure how to respond.",
                "I'm still learning and don't know how to answer that yet.",
                "Could you try asking that in a different way?"
            ]
            print("ChatBot:", random.choice(default_responses))

if __name__ == "__main__":
    simple_chatbot()