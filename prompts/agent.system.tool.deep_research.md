### deep_research:
Perform deep research using Google Gemini Deep Research agent. It plans, executes, and synthesizes multi‑step research tasks autonomously, using web search and your own data to produce detailed, sourced reports.

**Note**: Deep Research is an asynchronous agent that runs in the background (background=True by default). Research tasks can take several minutes.

#### Arguments:
- `query` (string, required) – The research question or topic.
- `background` (boolean, optional) – Whether to run the research in background (asynchronous). Default is `true`. Must be `true` for deep research.
- `stream` (boolean, optional) – Whether to stream results in real‑time (including thought summaries). Default is `false`.
- `tools` (list, optional) – Additional tools, e.g., file‑search. Example: `[{"type": "file_search", "file_search_store_names": ["store_name"]}]`.
- `format` (string, optional) – Instructions for output formatting, e.g., "Format the output as a technical report with sections 1, 2, 3".
- `previous_interaction_id` (string, optional) – For follow‑up questions to a previous research task.
- `agent_config` (dict, optional) – Configuration for the agent. For streaming thought summaries, use `{"type": "deep-research", "thinking_summaries": "auto"}`.
- `detach` (boolean, optional) – If `true`, starts the research and returns the interaction ID immediately without waiting. Default `false`.
- `poll_id` (string, optional) – Provide an interaction ID to check the status of a detached task. If used, `query` is not required.

#### Environment:
- Requires the environment variable `API_KEY_GOOGLE` set to a valid Google AI API key.
- The tool uses the `google‑genai` library (already installed).

#### Example usage (background polling):
~~~json
{
    "thoughts": [
        "I need to research the history of Google TPUs.",
        "I'll use the deep_research tool with background mode."
    ],
    "headline": "Starting deep research on Google TPUs",
    "tool_name": "deep_research",
    "tool_args": {
        "query": "Research the history of Google TPUs.",
        "background": true,
        "stream": false
    }
}
~~~

#### Example usage (streaming with thought summaries):
~~~json
{
    "thoughts": [
        "I want to watch the research process in real‑time."
    ],
    "headline": "Streaming deep research on EV batteries",
    "tool_name": "deep_research",
    "tool_args": {
        "query": "Research the competitive landscape of EV batteries.",
        "background": true,
        "stream": true,
        "agent_config": {
            "type": "deep-research",
            "thinking_summaries": "auto"
        }
    }
}
~~~

#### Example usage with file search and formatting:
~~~json
{
    "thoughts": [
        "I need to compare internal reports with public news."
    ],
    "headline": "Deep research with custom tools and format",
    "tool_name": "deep_research",
    "tool_args": {
        "query": "Compare our 2025 fiscal year report against current public web news.",
        "tools": [
            {
                "type": "file_search",
                "file_search_store_names": ["fileSearchStores/my‑store"]
            }
        ],
        "format": "Provide a summary table and bullet points."
    }
}
~~~

#### Example usage (Fire and Forget - Detached Mode):
~~~json
{
    "thoughts": [
        "I'll start the research now and check the results later."
    ],
    "headline": "Starting detached deep research",
    "tool_name": "deep_research",
    "tool_args": {
        "query": "Research the impact of quantum computing on cryptography.",
        "detach": true
    }
}
~~~

#### Example usage (Check Status - Poll ID):
~~~json
{
    "thoughts": [
        "Checking if the previous research task is finished."
    ],
    "headline": "Polling deep research status",
    "tool_name": "deep_research",
    "tool_args": {
        "poll_id": "interaction-1234567890"
    }
}
~~~

#### Important notes:
- The tool returns the final research report as text (or streams incremental updates).
- If the API key is missing or invalid, the tool returns an error message.
- For follow‑up questions, use the `previous_interaction_id` obtained from a completed interaction.
- Research tasks may take up to 20 minutes; the tool polls every 10 seconds until completion.
- Streaming requires `agent_config` with `thinking_summaries` to see thought updates.
