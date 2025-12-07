"""
Conversation Manager

Handles interactive conversations with the user to gather context and insights.
"""

from typing import Dict, Any, List
from shared.llm_interface import LLMInterface
from agent_prompts import AgentPrompts

class ConversationManager:
    """Handles interactive conversations"""

    def __init__(self, llm_interface: LLMInterface, max_questions: int = 5):
        self.llm = llm_interface
        self.prompts = AgentPrompts()
        self.max_questions = max_questions

    def conduct_conversation(self, code_snippet: str, analysis: Dict[str, Any]) -> Dict[str, str]:
        """
        Create and handle user-agent conversation
        
        Returns:
            List of conversation insights (question:answer pairs)
        """

        insights = []
        questions_asked = 0

        while questions_asked < self.max_questions:
            # Generate question
            question = self._generate_question(code_snippet, analysis, insights)

            # Enough info?
            if not question or question.lower() == 'no_more_questions':
                print('I have enough information to proceed.')
                break

            # Ask
            print(f'\nQuestion {questions_asked + 1}: {question}')

            answer = input("You: ").strip()

            # Handle input commands (if any)
            if answer.lower() == 'done':
                print('Finishing conversation...')
                break
            elif answer.lower() == 'skip':
                print('Skipping question...')
                questions_asked += 1
                continue

            # Track record
            insights.append({'question': question, 'answer': answer})
            questions_asked += 1
        return insights

    
    def _generate_question(self, code_snippet: str, analysis: Dict[str, Any], insights: List[Dict[str, str]]) -> str:
        """Generate a new question"""
        try:
            prompt = self.prompts.create_question_prompt(code_snippet, analysis, insights)
            response = self.llm.generate_response(prompt)

            # Parse question
            for line in response.strip().split('\n'):
                if line.startswith('QUESTION:'):
                    return line.split(':', 1)[1].strip()
                
            # Return first non-empty line
            for line in response.strip().split('\n'):
                if line.strip():
                    return line.strip()
                
            return None
        except Exception as e:
            print(f'[Error] Failed to generate question: {str(e)}')
            return None