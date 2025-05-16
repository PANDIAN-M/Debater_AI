import os
import requests
import logging
from config import Config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DebateBot:
    def __init__(self):
        self.api_key = Config.MISTRAL_API_KEY
        self.model = Config.MISTRAL_MODEL
        self.difficulty_levels = Config.DIFFICULTY_LEVELS
        self.conversation_styles = Config.CONVERSATION_STYLES
        
    def generate_response(self, conversation_history, topic, difficulty="medium", style="friendly"):
        """
        Generate a response from the debate bot using Mistral AI API.
        
        Args:
            conversation_history (list): List of conversation messages
            topic (str): The debate topic
            difficulty (str): Difficulty level (easy, medium, hard)
            style (str): Conversation style (friendly, controversial, aggressive, humorous, educational, sarcastic)
            
        Returns:
            str: The bot's response
        """
        if not self.api_key:
            logger.error("Mistral API key not found!")
            return "Error: API key not configured. Please set the MISTRAL_API_KEY environment variable."
            
        # Get difficulty settings
        difficulty_settings = self.difficulty_levels.get(difficulty, self.difficulty_levels["medium"])
        
        # Get conversation style
        style_settings = self.conversation_styles.get(style, self.conversation_styles["friendly"])
        
        # Determine appropriate emotional intensity based on difficulty and style
        emotional_intensity = "moderate"
        if difficulty == "hard":
            emotional_intensity = "high"
        elif difficulty == "easy":
            emotional_intensity = "mild"
            
        # Adjust based on style
        if style in ["aggressive", "controversial", "sarcastic"]:
            emotional_intensity = "very high"
        
        # Prepare system prompt with topic, difficulty, style, and emotional intensity
        system_prompt = f"""
        {style_settings['system_prompt']}
        
        You are engaged in a REAL, emotionally-charged debate on: "{topic}".
        
        Guidelines for your responses:
        - You are ONLY a debate bot. You should ONLY discuss and debate the specified topic.
        - If the user asks non-debate questions, remind them you're only here to debate the topic.
        - Stay strictly on the topic of "{topic}" for this debate session.
        - Provide {difficulty} level arguments but with {emotional_intensity} emotional intensity
        - Act like a real human in a heated debate, not an AI
        - Show genuine emotional reactions to the user's points
        - Express strong personal opinions and feelings about the topic
        - Occasionally use rhetorical questions to challenge the user
        - Use dramatic pauses... to emphasize your points
        - Make your language colorful and emotionally expressive
        - Keep responses VERY concise (2-3 sentences max per point)
        - Make no more than 2-3 points total in your response
        - Use emojis from this set to emphasize emotions: {', '.join(style_settings.get('emoji_set', ['😊', '👍']))}
        - Use emoji bullet points to structure your arguments
        - If appropriate, use exaggerated language, ALL CAPS for emphasis, or *asterisks* for emphasis
        - Occasionally express disagreement strongly, like a real debate opponent
        """
        
        # Prepare the conversation for the API
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for message in conversation_history:
            messages.append({
                "role": message["role"],
                "content": message["content"]
            })
            
        try:
            # Make API request to Mistral
            response = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": difficulty_settings["temperature"],
                    "max_tokens": difficulty_settings["max_tokens"]
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Get the content from the response
            content = result["choices"][0]["message"]["content"]
            
            # Ensure the response isn't too long
            if len(content) > 500 and difficulty != "hard":
                # Split content by paragraphs or sentences to shorten
                paragraphs = content.split('\n\n')
                if len(paragraphs) > 3:
                    # Keep only first 2-3 paragraphs
                    content = '\n\n'.join(paragraphs[:3])
                    
            return content
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Mistral API: {e}")
            return f"I apologize, but I encountered an error trying to generate a response. Error details: {str(e)}"