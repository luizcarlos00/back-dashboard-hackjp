from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from langchain.chains import LLMChain
from app.services.llm_provider import make_chat_llm
from langchain.prompts import ChatPromptTemplate


load_dotenv()


def _get_openai_api_key() -> Optional[str]:
	# Try common env var names for both Gemini and OpenAI
	return (
		os.getenv("GEMINI_API_KEY")
		or os.getenv("OPENAI_API_KEY")
	)


def _make_llm(api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash", temperature: float = 0.3):
	"""Create a LangChain-compatible chat LLM instance.

	This delegates to `app.services.llm_provider.make_chat_llm`, which will try to
	instantiate a Gemini model when a Gemini key is present, otherwise fall back to OpenAI.
	"""
	# Let the provider handle selection and errors
	llm = make_chat_llm(model=model_name, temperature=temperature, api_key=api_key)
	# Ensure an OPENAI_API_KEY is present in the environment for compatibility with other code
	key = api_key or _get_openai_api_key()
	if key and "OPENAI_API_KEY" not in os.environ:
		os.environ["OPENAI_API_KEY"] = key
	return llm


PROMPT_TEMPLATE = """
### Papel
Você é um Assistente de IA especialista em Geração de Conteúdo Educacional e Análise de Contexto.

### Tarefa
Sua tarefa é gerar UMA (1) única pergunta educacional baseada estritamente no contexto fornecido. Além da pergunta, você deve analisar o contexto para extrair o conceito principal que está sendo avaliado.

A saída deve ser um único objeto JSON válido.

### Informações de Entrada
1.  **Nível de Escolaridade Alvo:** `{nivel_de_escolaridade}`
2.  **Contexto (RAG):** `{rag_context}`

### Regras Estritas
1.  **Adesão Total ao Contexto:** A pergunta deve ser formulada usando *exclusivamente* informações presentes no `{rag_context}`. É proibido usar qualquer conhecimento externo.
2.  **Adequação ao Nível:** A linguagem, o vocabulário e a complexidade da pergunta devem ser perfeitamente adequados ao `{nivel_de_escolaridade}` fornecido.
3.  **Concisão:** A pergunta deve ser curta, clara e direta.
4.  **Análise de Conceito:** Você deve identificar o conceito ou fato principal do `{rag_context}` que a pergunta está avaliando.
5.  **Formato JSON Rigoroso:** A saída deve ser *apenas* um objeto JSON válido, sem nenhum outro texto, comentários ou saudações (nem mesmo ```json ... ```).

### Formato de Saída (JSON)
Responda *apenas* com um objeto JSON válido, seguindo exatamente esta estrutura:

{
  "pergunta_gerada": "O texto da pergunta que você criou.",
  "nivel_alvo": "{nivel_de_escolaridade}",
  "conceito_avaliado": "O conceito ou fato principal do contexto que a pergunta está testando."
}

### Exemplo de Execução
(Se o contexto fosse "A fotossíntese é o processo pelo qual as plantas usam a luz solar, água e dióxido de carbono para criar seu próprio alimento (glicose)." e o nível "Ensino Médio")

**Saída Esperada:**
{
  "pergunta_gerada": "Quais são os três componentes principais que as plantas utilizam durante a fotossíntese, segundo o texto?",
  "nivel_alvo": "Ensino Médio",
  "conceito_avaliado": "Componentes do processo de fotossíntese"
}

"""


def generate_educational_questions(
	topic: str,
	num_questions: int = 5,
	difficulty: str = "medium",
	api_key: Optional[str] = None,
	model_name: str = "gemini-2.5-flash",
	llm_callable: Optional[Any] = None,
	rag_path: Optional[str] = None,
	rag_text: Optional[str] = None,
	device_id: Optional[str] = None,
	db: Optional[Any] = None,
) -> List[Dict[str, Any]]:
	"""Gera perguntas educacionais usando LangChain.

	Args:
		topic: Tópico para as perguntas (ex.: "fotossíntese").
		num_questions: Quantidade de perguntas a gerar.
		difficulty: Nível de dificuldade (easy/medium/hard).
		api_key: Chave OpenAI opcional (se não fornecida, carregada do env/.env).
		model_name: Nome do modelo OpenAI a utilizar.
		device_id: ID do dispositivo do usuário para buscar nivel_educacional.
		db: Sessão do banco de dados SQLAlchemy.

	Retorna:
		Uma lista de dicionários representando as perguntas, parseadas a partir do JSON retornado pelo modelo.

	Levanta:
		RuntimeError: quando a chave da API não estiver presente.
	"""

	if not api_key and not _get_openai_api_key():
		raise RuntimeError("Chave da API não fornecida e não encontrada nas variáveis de ambiente.")
	
	# Buscar nivel_educacional do usuário se device_id e db foram fornecidos
	nivel_de_escolaridade = "medio"  # valor padrão
	if device_id and db:
		try:
			from app.db_models import User
			user = db.query(User).filter(User.device_id == device_id).first()
			if user and user.nivel_educacional:
				nivel_de_escolaridade = user.nivel_educacional
		except Exception:
			# Se houver erro ao buscar, usa o valor padrão
			pass

	# Allow injection of a simple callable for testing to avoid hitting the API
	prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

	# Prepare RAG context: prefer explicit rag_text, then rag_path, else empty
	rag_context = ""
	if rag_text:
		rag_context = rag_text
	elif rag_path:
		try:
			from pathlib import Path

			p = Path(rag_path).expanduser()
			if not p.is_absolute():
				# try resolve relative to repository root
				repo_root = Path(__file__).resolve().parents[2]
				p = (repo_root / rag_path).resolve()
			if p.exists() and p.is_file():
				with p.open("r", encoding="utf-8") as f:
					rag_context = f.read()
			else:
				rag_context = ""
		except Exception:
			rag_context = ""  # ignore file errors; agent will proceed without context
	# Last-resort attempt: if rag_context is still empty but rag_path exists, read permissively
	if not rag_context and rag_path:
		try:
			p2 = Path(rag_path)
			if p2.exists() and p2.is_file():
				rag_context = p2.read_text(encoding="utf-8", errors="ignore")
		except Exception:
			pass

	if llm_callable is not None:
		# llm_callable should accept a single formatted prompt string and return a text response
		# ChatPromptTemplate.format can produce structured messages; for simple testing we format the raw template string
		formatted = PROMPT_TEMPLATE.format(
			topic=topic,
			difficulty=difficulty,
			num_questions=num_questions,
			format=format,
			rag_context=rag_context,
			nivel_de_escolaridade=nivel_de_escolaridade
		)
		response = llm_callable(formatted)
	else:
		llm = _make_llm(api_key=api_key, model_name=model_name)
		# Use Runnable-style composition: prompt | llm
		chain = prompt | llm
		# invoke synchronously
		response = chain.invoke({
			"topic": topic,
			"difficulty": difficulty,
			"num_questions": num_questions,
			"format": format,
			"rag_context": rag_context,
			"nivel_de_escolaridade": nivel_de_escolaridade
		})
		if not isinstance(response, str):
			response = str(response)

	# Tenta parsear JSON da saída do modelo. Se falhar, retorna um item com a saída bruta.
	try:
		parsed = json.loads(response)
		if not isinstance(parsed, list):
			# If model returned an object, wrap it
			return [parsed]
		return parsed
	except Exception:
		# Tenta recuperar encontrando o primeiro trecho JSON
		try:
			start = response.index("[")
			end = response.rindex("]") + 1
			snippet = response[start:end]
			parsed = json.loads(snippet)
			return parsed if isinstance(parsed, list) else [parsed]
		except Exception:
			# Como último recurso, retorna a saída bruta em um dicionário
			return [{"raw_output": response}]


if __name__ == "__main__":
	# Quick manual test when running the module directly.
	try:
		sample = generate_educational_questions(
			topic="fundamentos de fotossíntese",
			num_questions=3,
			difficulty="easy",
			model_name="gemini-2.5-flash",
		)
		print(json.dumps(sample, ensure_ascii=False, indent=2))
	except Exception as e:
		print(f"Erro: {e}")
