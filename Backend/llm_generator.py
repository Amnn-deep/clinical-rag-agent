import os
from groq import Groq

class LLMGenerator:
    @staticmethod
    def generate_response(context, query):
        api_key = os.getenv("GROQ_KEY")
        if not api_key:
            return "Error: GROQ_KEY missing in .env"

        try:
            client = Groq(api_key=api_key)
            model_id = "llama-3.1-8b-instant"

            # STRICTOR PROMPT: Hallucination rokne ke liye
            system_prompt = f"""
            You are a professional Clinical Assistant. 
            Your ONLY source of truth is the provided context.

            STRICT RULES:
            1. If the answer is NOT explicitly mentioned in the CONTEXT, you MUST strictly respond: "I am sorry, but the provided clinical document does not contain information regarding this specific query."
            2. NEVER use your internal training data to answer. Only use the CONTEXT.
            3. If the information is present, provide a detailed 3-4 line medical response.
            4. Do NOT mention "According to the context" or "The document says". Just state the facts or the "not found" message.

            CONTEXT: {context}
            """

            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                model=model_id,
                temperature=0.0  # Zero temperature makes it more factual and less creative
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"LLM Error: {str(e)}"