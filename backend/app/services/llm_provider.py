import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

SUPPORTED_GEMINI_CLASS_NAMES = [
    "ChatGoogleGenerativeAI",  # current (langchain-google-genai >= 2.0)
]

def _import_gemini_class():
    """Attempt to import the Gemini chat class from langchain-google-genai.

    Returns the class if found, else None.
    """
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore
        return ChatGoogleGenerativeAI
    except Exception:  # pragma: no cover - best effort
        return None


def make_chat_llm(
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.3,
    api_key: Optional[str] = None,
    provider: Optional[str] = None,
):
    """Factory that returns a LangChain-compatible chat LLM instance.

    Selection order:
    1. Explicit provider argument ("gemini" or "openai")
    2. ENV var LLM_PROVIDER (gemini/openai)
    3. Presence of GEMINI_API_KEY triggers Gemini, else OpenAI

    Parameters
    ----------
    model: str
        Model name (for Gemini e.g. "gemini-1.5-pro" or "gemini-1.5-flash", default openai model)
    temperature: float
        Sampling temperature.
    api_key: Optional[str]
        Explicit API key override.
    provider: Optional[str]
        Force provider selection ignoring heuristic.
    """

    env_provider = (provider or os.getenv("LLM_PROVIDER", "")).lower()
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    key = api_key or gemini_key or openai_key

    wants_gemini = False
    if env_provider:
        wants_gemini = env_provider == "gemini"
    else:
        wants_gemini = bool(gemini_key)  # heuristic fallback

    if wants_gemini:
        gemini_cls = _import_gemini_class()
        if gemini_cls and gemini_key:
            try:
                # If caller passed an OpenAI-ish model name, swap for a sensible Gemini default
                gemini_model = model
                if not str(model).lower().startswith("gemini-"):
                    # Use gemini-2.5-flash for fast responses (latest default)
                    gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
                
                # langchain-google-genai v2.0+ uses simplified constructor
                llm = gemini_cls(
                    model=gemini_model,
                    temperature=temperature,
                    google_api_key=gemini_key
                )
                logger.info("Using Gemini provider (%s) with model=%s", gemini_cls.__name__, gemini_model)
                return llm
            except Exception as e:  # pragma: no cover (network or version issues)
                logger.warning(
                    "Failed to instantiate Gemini class %s (%s). Falling back to OpenAI. Install/upgrade 'langchain-google-genai'.", 
                    gemini_cls.__name__, e
                )
        else:
            if env_provider == "gemini":
                logger.warning("Gemini provider forced but package not installed or key missing. Falling back to OpenAI.")

    # Fallback: OpenAI-compatible client (langchain_openai)
    try:
        from langchain_openai import ChatOpenAI
        if not openai_key and gemini_key and not os.getenv("OPENAI_API_KEY"):
            # Reuse gemini key if user only provided one key and expects unified env
            openai_key = gemini_key
        logger.info("Using OpenAI provider with model=%s", model)
        return ChatOpenAI(model=model, temperature=temperature, api_key=openai_key or key)
    except Exception as e:
        raise RuntimeError(
            "Failed to create an OpenAI Chat client (langchain_openai.ChatOpenAI). "
            "Ensure 'langchain_openai' and 'openai' are installed. "
            f"Original error: {e}"
        )
