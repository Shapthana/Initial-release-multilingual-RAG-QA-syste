import requests

from app.config import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL


GENERATION_TIMEOUT = 240
MAX_OUTPUT_TOKENS = 512


def ollama_base_url():
    base_url = LLM_BASE_URL.rstrip("/")

    if base_url.endswith("/v1"):
        base_url = base_url[:-3]

    return base_url


def clean_answer(text):
    """
    Remove Qwen3 reasoning and return only the final answer.
    """

    if not text:
        return ""

    text = text.strip()

    # Qwen3 may expose its reasoning followed by </think>.
    if "</think>" in text:
        text = text.rsplit("</think>", 1)[1].strip()

    # If the model explicitly announces the final answer,
    # keep only what follows that marker.
    markers = [
        "So the final answer is:",
        "The final answer is:",
        "Final answer:",
        "Final Answer:",
        "Answer:",
        "ANSWER:",
    ]

    for marker in markers:
        if marker in text:
            text = text.rsplit(marker, 1)[1].strip()
            break

    # Remove accidental surrounding quotes.
    text = text.strip().strip('"').strip("'").strip()

    # If reasoning still remains, prefer the last line containing
    # a citation such as [1].
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    cited_lines = [
        line for line in lines
        if "[" in line and "]" in line
    ]

    if cited_lines:
        text = cited_lines[-1]

    return text

def generate_answer(query, contexts):

    citations = [
        c.get("source", "unknown")
        for c in contexts
    ]

    if not (LLM_BASE_URL and LLM_MODEL):
        return {
            "answer": (
                "LLM generation is not configured. "
                "Retrieved evidence is shown below."
            ),
            "citations": citations,
        }

    context_parts = []

    for i, context_item in enumerate(contexts):

        source = context_item.get(
            "source",
            "unknown",
        )

        text = context_item.get(
            "text",
            "",
        )

        context_parts.append(
            f"[{i + 1}] SOURCE: {source}\n{text}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
/no_think

Answer the question using ONLY the provided context.

IMPORTANT:
- Give ONLY the final answer.
- Do NOT explain your reasoning.
- Do NOT discuss the context.
- Do NOT discuss which source is reliable.
- Do NOT repeat the question.
- Do NOT mention these instructions.
- Answer in the same language as the question.
- Keep the answer to 1 or 2 sentences.
- Include the citation number supporting the answer, for example [1].
- Do not invent information.
- If the context does not contain enough information, answer:
The provided evidence is insufficient.

Question:
{query}

Context:
{context}

Final answer:
""".strip()

    url = f"{ollama_base_url()}/api/chat"

    payload = {
        "model": LLM_MODEL,

        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],

        "stream": False,

        # Qwen3/Ollama thinking control.
        "think": False,

        "options": {
            "temperature": 0,
            "num_predict": MAX_OUTPUT_TOKENS,
        },
    }

    headers = {
        "Content-Type": "application/json"
    }

    if LLM_API_KEY:
        headers["Authorization"] = (
            f"Bearer {LLM_API_KEY}"
        )

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=GENERATION_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        message = data.get(
            "message",
            {},
        )

        # Normal Ollama chat response.
        raw_answer = message.get(
            "content",
            "",
        )

        answer = clean_answer(
            raw_answer
        )

        if not answer:
            answer = (
                "[GENERATION_EMPTY] "
                "The LLM returned an empty answer."
            )

        return {
            "answer": answer,
            "citations": citations,
        }

    except requests.exceptions.Timeout:

        return {
            "answer": (
                "[GENERATION_TIMEOUT] "
                f"The local LLM did not finish within "
                f"{GENERATION_TIMEOUT} seconds."
            ),
            "citations": citations,
        }

    except requests.exceptions.RequestException as exc:

        return {
            "answer": (
                f"[GENERATION_ERROR] {str(exc)}"
            ),
            "citations": citations,
        }

    except (
        KeyError,
        IndexError,
        TypeError,
        ValueError,
    ) as exc:

        return {
            "answer": (
                f"[GENERATION_RESPONSE_ERROR] "
                f"{str(exc)}"
            ),
            "citations": citations,
        }