from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


load_dotenv()


def _get_openai_api_key() -> Optional[str]:
	# Try common env var names; `.env` in repo uses OpenAI_API_KEY
	return os.getenv("OpenAI_API_KEY") or os.getenv("OPENAI_API_KEY")


def _make_llm(api_key: Optional[str] = None, model_name: str = "gpt-3.5-turbo", temperature: float = 0.3) -> ChatOpenAI:
	key = api_key or _get_openai_api_key()
	if not key:
		raise RuntimeError(
			"Chave OpenAI não encontrada. Por favor defina OPENAI_API_KEY no ambiente ou no arquivo .env."
		)
	# Ensure common env var is set so downstream code that checks the env will find it
	if "OPENAI_API_KEY" not in os.environ:
		os.environ["OPENAI_API_KEY"] = key

	# Use langchain_openai.ChatOpenAI (compatível com openai>=1.0.0)
	# langchain_openai expects: model, temperature, api_key
	return ChatOpenAI(model=model_name, temperature=temperature, api_key=key)


PROMPT_TEMPLATE = """
Você é um especialista em design instrucional. A partir do tópico, do nível de dificuldade e do número de perguntas,
gere um array JSON de perguntas educacionais. Cada objeto de pergunta deve conter os campos:

- question: o texto da pergunta (string)
- answer: a resposta correta (string)
- explanation: uma explicação curta (string)
- difficulty: o nível de dificuldade fornecido
- topic: o tópico fornecido

Se o `format` for "multiple_choice", inclua também:
- choices: um array com 3-5 opções plausíveis (strings), onde uma delas é igual a `answer`.

Saída: apenas JSON válido (um array JSON). Não adicione nenhum comentário extra.

Tópico: {topic}
Dificuldade: {difficulty}
Número de perguntas: {num_questions}
Formato: {format}
Contexto adicional (RAG):
{rag_context}
"""


def generate_educational_questions(
	topic: str,
	num_questions: int = 5,
	difficulty: str = "medium",
	format: str = "multiple_choice",
	api_key: Optional[str] = None,
	model_name: str = "gpt-3.5-turbo",
	llm_callable: Optional[Any] = None,
	rag_path: Optional[str] = None,
	rag_text: Optional[str] = None,
) -> List[Dict[str, Any]]:
	"""Gera perguntas educacionais usando LangChain + OpenAI.

	Args:
		topic: Tópico para as perguntas (ex.: "fotossíntese").
		num_questions: Quantidade de perguntas a gerar.
		difficulty: Nível de dificuldade (easy/medium/hard).
		format: "multiple_choice" ou "short_answer".
		api_key: Chave OpenAI opcional (se não fornecida, carregada do env/.env).
		model_name: Nome do modelo OpenAI a utilizar.

	Retorna:
		Uma lista de dicionários representando as perguntas, parseadas a partir do JSON retornado pelo modelo.

	Levanta:
		RuntimeError: quando a chave da API não estiver presente.
	"""

	if format not in ("multiple_choice", "short_answer"):
		raise ValueError("format deve ser 'multiple_choice' ou 'short_answer'")

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
			format="multiple_choice",
		)
		print(json.dumps(sample, ensure_ascii=False, indent=2))
	except Exception as e:
		print(f"Erro: {e}")
