import json
from typing import Any, Optional
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle


class ThoughtData:
    """Represents a single thought in the sequential thinking process."""
    def __init__(
        self,
        thought: str,
        thought_number: int,
        total_thoughts: int,
        next_thought_needed: bool,
        is_revision: Optional[bool] = None,
        revises_thought: Optional[int] = None,
        branch_from_thought: Optional[int] = None,
        branch_id: Optional[str] = None,
        needs_more_thoughts: Optional[bool] = None,
    ):
        self.thought = thought
        self.thought_number = thought_number
        self.total_thoughts = total_thoughts
        self.next_thought_needed = next_thought_needed
        self.is_revision = is_revision
        self.revises_thought = revises_thought
        self.branch_from_thought = branch_from_thought
        self.branch_id = branch_id
        self.needs_more_thoughts = needs_more_thoughts

    def to_dict(self) -> dict:
        return {
            "thought": self.thought,
            "thoughtNumber": self.thought_number,
            "totalThoughts": self.total_thoughts,
            "nextThoughtNeeded": self.next_thought_needed,
            "isRevision": self.is_revision,
            "revisesThought": self.revises_thought,
            "branchFromThought": self.branch_from_thought,
            "branchId": self.branch_id,
            "needsMoreThoughts": self.needs_more_thoughts,
        }


class SequentialThinking(Tool):
    """
    A tool for dynamic and reflective problem-solving through a structured thinking process.
    This tool helps analyze problems through a flexible thinking process that can adapt and evolve.
    Each thought can build on, question, or revise previous insights as understanding deepens.
    """

    STATE_KEY = "_sequential_thinking_state"

    async def execute(self, **kwargs) -> Response:
        """
        Process a thought step in the sequential thinking process.
        Expected arguments (from self.args):
            thought (str): The current thinking step
            nextThoughtNeeded (bool): Whether another thought step is needed
            thoughtNumber (int): Current thought number (1-indexed)
            totalThoughts (int): Estimated total thoughts needed
            isRevision (bool, optional): Whether this revises previous thinking
            revisesThought (int, optional): Which thought is being reconsidered
            branchFromThought (int, optional): Branching point thought number
            branchId (str, optional): Branch identifier
            needsMoreThoughts (bool, optional): If more thoughts are needed
        """
        # Extract arguments
        thought = self.args.get("thought", "")
        next_thought_needed = self.args.get("nextThoughtNeeded", True)
        thought_number = self.args.get("thoughtNumber", 1)
        total_thoughts = self.args.get("totalThoughts", 1)
        is_revision = self.args.get("isRevision")
        revises_thought = self.args.get("revisesThought")
        branch_from_thought = self.args.get("branchFromThought")
        branch_id = self.args.get("branchId")
        needs_more_thoughts = self.args.get("needsMoreThoughts")

        # Validate required fields
        if not thought:
            return Response(
                message="Error: 'thought' is required.",
                break_loop=False,
                additional={"error": True}
            )

        # Adjust total_thoughts if thought_number exceeds it
        if thought_number > total_thoughts:
            total_thoughts = thought_number

        # Create ThoughtData object
        thought_data = ThoughtData(
            thought=thought,
            thought_number=thought_number,
            total_thoughts=total_thoughts,
            next_thought_needed=next_thought_needed,
            is_revision=is_revision,
            revises_thought=revises_thought,
            branch_from_thought=branch_from_thought,
            branch_id=branch_id,
            needs_more_thoughts=needs_more_thoughts,
        )

        # Update state
        state = self._get_state()
        state["thought_history"].append(thought_data.to_dict())

        # Handle branching
        if branch_from_thought and branch_id:
            if branch_id not in state["branches"]:
                state["branches"][branch_id] = []
            state["branches"][branch_id].append(thought_data.to_dict())

        # Save state
        self._save_state(state)

        # Log thought (optional)
        self._log_thought(thought_data)

        # Prepare response
        response_data = {
            "thoughtNumber": thought_number,
            "totalThoughts": total_thoughts,
            "nextThoughtNeeded": next_thought_needed,
            "branches": list(state["branches"].keys()),
            "thoughtHistoryLength": len(state["thought_history"]),
        }

        return Response(
            message=json.dumps(response_data, indent=2),
            break_loop=False,
            additional=response_data
        )

    def _get_state(self) -> dict:
        """Retrieve the current thinking state from agent data."""
        state = self.agent.get_data(self.STATE_KEY)
        if not state:
            state = {
                "thought_history": [],
                "branches": {},
            }
        return state

    def _save_state(self, state: dict):
        """Save the thinking state to agent data."""
        self.agent.set_data(self.STATE_KEY, state)

    def _log_thought(self, thought_data: ThoughtData):
        """Log the thought in a formatted way (similar to the MCP server)."""
        # Determine prefix and context
        prefix = "💭 Thought"
        context = ""
        if thought_data.is_revision:
            prefix = "🔄 Revision"
            context = f" (revising thought {thought_data.revises_thought})"
        elif thought_data.branch_from_thought:
            prefix = "🌿 Branch"
            context = f" (from thought {thought_data.branch_from_thought}, ID: {thought_data.branch_id})"

        header = f"{prefix} {thought_data.thought_number}/{thought_data.total_thoughts}{context}"
        border = "─" * (max(len(header), len(thought_data.thought)) + 4)

        formatted = f"""
┌{border}┐
│ {header} │
├{border}┤
│ {thought_data.thought.ljust(len(border) - 2)} │
└{border}┘"""
        PrintStyle(font_color="#1B4F72", padding=True).print(formatted)

    async def before_execution(self, **kwargs):
        """Override to provide custom logging."""
        await super().before_execution(**kwargs)
        PrintStyle(font_color="#1B4F72", background_color="white", bold=True).print(
            f"{self.agent.agent_name}: Starting sequential thinking step"
        )

    async def after_execution(self, response: Response, **kwargs):
        """Override to handle response."""
        await super().after_execution(response, **kwargs)
        # Additional logging if needed
        if response.additional and not response.additional.get("error"):
            PrintStyle(font_color="#85C1E9").print(
                f"Thought history length: {response.additional.get('thoughtHistoryLength')}"
            )