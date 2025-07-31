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

        self.prompt1 = ChatPromptTemplate.from_template(
            """Answer the following question based on the provided context. Be precise and factual """
            +
            """
            Question: {question}
            
            Context:
            {context}
            
            
            
            If the context is insufficient, respond with: "I cannot answer this question based on the provided documents."
            """
        )

        #prompt when verification fails
        self.prompt2 = ChatPromptTemplate.from_template(
            """
            Answer the following question based on the provided context. Be precise and factual.our previous attempt to answer the user's question failed verification. Your task is to generate a new, corrected response based on the feedback provided.
            
            Question : {question}
            Context : {context}
            Feedback : {feedback}
            
            If the context is insufficient, respond with: "I cannot answer this question based on the provided documents."
            """
        )

    def generate(self, question: str, documents: List[Document], verification_report : str) -> Dict:
        """Generate an initial answer using the provided documents."""
        context = "\n\n".join([doc.page_content for doc in documents])

        try:
            # invoke the llm

            if verification_report == "":
                chain = self.prompt1 | self.llm | StrOutputParser()
                answer = chain.invoke({
                    "question": question,
                    "context": context,
                })
            else :
                chain = self.prompt2 | self.llm | StrOutputParser()
                answer = chain.invoke({
                    "question" : question,
                    "context" : context,
                    "feedback" : verification_report
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