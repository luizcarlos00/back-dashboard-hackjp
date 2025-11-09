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
Você é um especialista em design instrucional. A partir do tópico, do nível de dificuldade e do número de perguntas,
gere um array JSON de perguntas educacionais. Cada objeto de pergunta deve conter os campos:

Entradas : 

id_question : {id_question : str}
id_usuario : {id_usuario : str}
question: o texto da pergunta (string)



Saída: apenas JSON válido (um array JSON). Não adicione nenhum comentário extra.


aprovação se a soma notas for maior que 0.6: {aprovação: bool}
Nota da respota de 0 a 1 : {nota}
Tópico: {topic}
Dificuldade: {difficulty}
Número de perguntas: {num_questions}
Contexto adicional (RAG):{rag_context}
Conceitos faltandtes : {concepts_missing}
Contceito indentificado : {concepts_identified}

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
) -> List[Dict[str, Any]]:
	"""Gera perguntas educacionais usando LangChain.

	Args:
		topic: Tópico para as perguntas (ex.: "fotossíntese").
		num_questions: Quantidade de perguntas a gerar.
		difficulty: Nível de dificuldade (easy/medium/hard).
		api_key: Chave OpenAI opcional (se não fornecida, carregada do env/.env).
		model_name: Nome do modelo OpenAI a utilizar.

	Retorna:
		Uma lista de dicionários representando as perguntas, parseadas a partir do JSON retornado pelo modelo.

	Levanta:
		RuntimeError: quando a chave da API não estiver presente.
	"""

	if not api_key and not _get_openai_api_key():
		raise RuntimeError("Chave da API não fornecida e não encontrada nas variáveis de ambiente.")

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
		formatted = PROMPT_TEMPLATE.format(topic=topic, difficulty=difficulty, num_questions=num_questions, format=format, rag_context=rag_context)
		response = llm_callable(formatted)
	else:
		llm = _make_llm(api_key=api_key, model_name=model_name)
		# Use Runnable-style composition: prompt | llm
		chain = prompt | llm
		# invoke synchronously
		response = chain.invoke({"topic": topic, "difficulty": difficulty, "num_questions": num_questions, "format": format, "rag_context": rag_context})
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
