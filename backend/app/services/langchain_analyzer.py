from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from app.models import AnswerAnalysis
from app.config import OPENAI_API_KEY
from typing import List
import logging

logger = logging.getLogger(__name__)

class LangChainAnalyzer:
    """
    Analyzes user answers using LangChain + GPT-4o-mini.
    Evaluates understanding, identifies concepts, generates feedback.
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,  # More deterministic for consistent evaluation
            api_key=OPENAI_API_KEY
        )
        self.parser = PydanticOutputParser(pydantic_object=AnswerAnalysis)
    
    async def analyze_response(
        self,
        user_response: str,
        video_title: str,
        video_description: str,
        expected_concepts: List[str],
        question_text: str
    ) -> AnswerAnalysis:
        """
        Analyze user's text response to E2E question.
        
        Args:
            user_response: User's answer text
            video_title: Title of the video watched
            video_description: Description of the video
            expected_concepts: Key concepts that should be mentioned
            question_text: The question that was asked
        
        Returns:
            AnswerAnalysis with score, feedback, concepts identified, etc.
        """
        try:
            # Create prompt template
            template = """
Você é um professor avaliando a compreensão de um aluno sobre um conceito educativo.

**Contexto do Vídeo:**
- Título: {video_title}
- Descrição: {video_description}
- Conceitos esperados: {expected_concepts}

**Pergunta feita ao aluno:**
{question_text}

**Resposta do aluno:**
{user_response}

**Sua tarefa:**
1. Avaliar se o aluno demonstrou compreensão do conceito apresentado no vídeo
2. Identificar quais conceitos esperados foram mencionados ou demonstrados
3. Calcular um score de qualidade (0.0 a 1.0):
   - 0.0-0.4: Não entendeu / resposta inadequada / muito superficial
   - 0.5-0.6: Entendimento básico, mas incompleto ou impreciso
   - 0.7-0.8: Bom entendimento, menciona conceitos principais
   - 0.9-1.0: Excelente compreensão profunda e articulada
4. Gerar feedback construtivo, encorajador e específico (2-3 frases)

**Critérios de avaliação:**
- O aluno mencionou ou demonstrou entendimento dos conceitos-chave?
- Usou suas próprias palavras (não decorou)?
- A explicação está clara e coerente?
- Respondeu adequadamente à pergunta feita?

**Importante:**
- Seja encorajador, mesmo se a resposta não for perfeita
- Destaque o que foi bem feito
- Sugira o que pode melhorar, se aplicável
- Score >= 0.6 significa "passou"

{format_instructions}
"""
            
            prompt = ChatPromptTemplate.from_template(template)
            
            # Create chain
            chain = prompt | self.llm | self.parser
            
            # Execute analysis
            result = await chain.ainvoke({
                "video_title": video_title,
                "video_description": video_description or "Sem descrição",
                "expected_concepts": ", ".join(expected_concepts) if expected_concepts else "Conceitos gerais",
                "question_text": question_text,
                "user_response": user_response,
                "format_instructions": self.parser.get_format_instructions()
            })
            
            logger.info(f"Successfully analyzed response with score: {result.quality_score}")
            return result
        
        except Exception as e:
            logger.error(f"Error analyzing response with LangChain: {str(e)}")
            # Return fallback analysis
            return AnswerAnalysis(
                quality_score=0.5,
                passed=False,
                concepts_identified=[],
                missing_concepts=expected_concepts,
                feedback="Não foi possível analisar sua resposta automaticamente. Por favor, tente novamente."
            )

# Global instance
analyzer = LangChainAnalyzer()

