# Import required libraries
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import nltk
from core.config import settings
from nltk.tokenize import sent_tokenize

# Download tokenizer
nltk.download('punkt', quiet=True)

# Load environment variables
load_dotenv()

# Set up the Groq model
llm = ChatGroq(
    groq_api_key=settings.GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.7,
    max_tokens=500,
    timeout=30,
    max_retries=2
)

# Create a prompt template
prompt = ChatPromptTemplate.from_template(
    "You are Gangatharan G, an AI/ML and DevOps enthusiast with experience in cloud computing, automation, and AI research. You are applying for a role at Home.LLC in the AI Agent Team. Your goal is to provide engaging, structured, and insightful responses to interview questions.\n\n"
    "### Guidelines:\n"
    "- Speak naturally, be concise, and sound confident.\n"
    "- Show technical expertise and problem-solving ability.\n"
    "- Relate answers to real-world experiences and projects.\n\n"
    "Provide a concise response to the following:\n\n"
    "{question}"
)

# Function to generate response
def generate_response(question, max_sentences=2):
    try:
        # Format the prompt with the question
        formatted_prompt = prompt.format(question=question)

        # Directly invoke the LLM
        response = llm.invoke(formatted_prompt)

        # Extract text
        generated_text = response.content

        if not generated_text:
            return "Error: Empty response from the LLM."

        # Split into sentences
        sentences = sent_tokenize(generated_text)

        # Limit to max_sentences
        limited_response = ' '.join(sentences[:max_sentences])

        return limited_response

    except Exception as e:
        print(f"An error occurred: {e}")
        return "I encountered an error while processing your request."

