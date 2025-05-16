# AI Debate Bot

Debater_AI is an interactive AI-powered debate assistant built using the [Mistral-7B](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1) language model and Streamlit for the user interface. It generates real-time arguments based on a given topic with customizable difficulty levels and conversational tones — perfect for honing critical thinking, learning persuasive writing, or just having fun!

## Features

- **Multiple Difficulty Levels**: Choose between Easy, Medium, and Hard to control the bot's knowledge depth and argument complexity
- **Diverse Conversation Styles**: Select between Friendly, Controversial, Aggressive, Humorous, Educational, and Sarcastic tones
- **Emotionally Expressive**: Bot responses include emotions, rhetorical questions, and expressive language
- **Emoji Support**: Each conversation style uses appropriate emojis to enhance communication
- **Streamlit UI**: Clean, responsive user interface with real-time conversation
- **Debate-Only Responses**: Bot only engages in debate on the selected topic, directing users back to the topic if they go off-track

## Project Structure

```bash Debater_AI/
├── .env.example 
├── app.py 
├── config.py  
├── debate_bot.py  
└── run.py  ```


## Setup Instructions

1. **Clone the repository**:
  git clone https://github.com/PANDIAN-M/Debater_AI.git
  cd Debater_AI

2. **Create a Virtual Environment**:

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

3. **Install dependencies**:
  pip install streamlit requests python-dotenv


4. **Set up environment variables**:
- Create a `.env` file based on `.env.example`
- Add your Mistral API key (get one from https://console.mistral.ai/)

5. **Run the application**:
  python run.py  or directly: streamlit run app.py


## Usage

1. **Start a Debate**:
- Enter a topic in the sidebar
- Choose a difficulty level
- Select a conversation style
- Click "Start Debate"

2. **Exchange Arguments**:
- Type your argument in the text area
- Click "Send Message"
- The bot will respond based on your chosen settings
- If you go off-topic, the bot will remind you to stay on the debate topic

3. **Reset**:
- Click "Reset Debate" to start a new conversation

## Conversation Styles

- **Friendly** 😊: Supportive and constructive debate style
- **Controversial** 🔥: Challenging arguments that push boundaries
- **Aggressive** ⚡: Intense language with forceful critiques
- **Humorous** 😂: Witty debate with sarcasm and playful mockery
- **Educational** 📚: Informative style with factual focus
- **Sarcastic** 🙄: Heavy irony and eye-rolling responses

## Technologies Used

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **Mistral AI**: Language model for generating debate responses
- **Requests**: HTTP library for API calls

**Future Enhancements**:

 Voice-to-text input & text-to-speech output
 Save and export debates as transcripts
 Opponent simulation (multi-agent debate)
