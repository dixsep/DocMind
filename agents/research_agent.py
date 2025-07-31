from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, List
from langchain.schema import Document
import logging
from basic import GEMINI_API_KEY

logger = logging.getLogger(__name__)

class ResearchAgent:
    def __init__(self):
        """Initialize the research agent with the OpenAI model."""
        self.model = "gemini-2.5-pro"

        self.llm = ChatGoogleGenerativeAI(
            model = self.model,
            google_api_key = GEMINI_API_KEY
        )

        self.prompt = ChatPromptTemplate.from_template(
            """Answer the following question based on the provided context. Be precise and factual.
            
            Question: {question}
            
            Context:
            {context}
            
            If the context is insufficient, respond with: "I cannot answer this question based on the provided documents."
            """
        )

    def generate(self, question: str, documents: List[Document]) -> Dict:
        """Generate an initial answer using the provided documents."""
        context = "\n\n".join([doc.page_content for doc in documents])

        chain = self.prompt | self.llm | StrOutputParser()
        try:
            # invoke the llm
            answer = chain.invoke({
                "question": question,
                "context": context
            })

            logger.info(f"Generated answer: {answer}")
            logger.info(f"Context used: {context}")

        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise

        return {
            "draft_answer": answer,
            "context_used": context
        }