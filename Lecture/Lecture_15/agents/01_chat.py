"""
Step 1: The LLM is just a function.

Strip away the chat interface and an LLM is a stateless function:

    reply = f(list_of_messages)

It has NO memory. "Conversation" is an illusion created by the caller
(that's us!) re-sending the whole message history every time.
Understanding this is the foundation of every agent workflow:
an "agent" is just a program that keeps editing this list in a loop.

Run:
    uv run 01_chat.py
"""

from llm import chat, get_client

client = get_client()

# A "message" is a dict with a role and content.
#  - "system": standing instructions, set by the programmer (us)
#  - "user":   the request
#  - "assistant": what the model said earlier (we send its own words back!)
messages = [
    {
        "role": "system",
        "content": "You are a terse assistant for an architecture school "
        "computational design course. Answer in at most two sentences.",
    },
    {"role": "user", "content": "What is a mesh, compared to a NURBS surface?"},
]

reply = chat(client, messages)
print("ASSISTANT:", reply.content)

# --- The illusion of memory -------------------------------------------
# To "continue the conversation" we must append the assistant's reply
# and our follow-up, then send EVERYTHING again.
messages.append({"role": "assistant", "content": reply.content})
messages.append({"role": "user", "content": "Which one is better for fabrication?"})

reply = chat(client, messages)
print("\nASSISTANT:", reply.content)

# Try this: comment out the two `messages.append(...)` lines above and
# send only the follow-up question. The model has no idea what "which one"
# refers to. State lives on OUR side, not in the model.
