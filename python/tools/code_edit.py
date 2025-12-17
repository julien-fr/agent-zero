import re
import math
from difflib import SequenceMatcher
from pathlib import Path
from typing import Optional, Tuple, List
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle


# --- Functions copied/adapted from aider.coders.editblock_coder ---

def prep(content: str) -> Tuple[str, List[str]]:
    """Ensure content ends with newline and split into lines."""
    if content and not content.endswith("\n"):
        content += "\n"
    lines = content.splitlines(keepends=True)
    return content, lines


def perfect_replace(whole_lines: List[str], part_lines: List[str], replace_lines: List[str]) -> Optional[str]:
    """Exact match replacement."""
    part_tup = tuple(part_lines)
    part_len = len(part_lines)

    for i in range(len(whole_lines) - part_len + 1):
        whole_tup = tuple(whole_lines[i : i + part_len])
        if part_tup == whole_tup:
            res = whole_lines[:i] + replace_lines + whole_lines[i + part_len :]
            return "".join(res)
    return None


def match_but_for_leading_whitespace(whole_lines: List[str], part_lines: List[str]) -> Optional[str]:
    """Check if lines match ignoring leading whitespace, return the whitespace to add."""
    num = len(whole_lines)
    if not all(whole_lines[i].lstrip() == part_lines[i].lstrip() for i in range(num)):
        return None
    # are they all offset the same?
    add = set(
        whole_lines[i][: len(whole_lines[i]) - len(part_lines[i])]
        for i in range(num)
        if whole_lines[i].strip()
    )
    if len(add) != 1:
        return None
    return add.pop()


def replace_part_with_missing_leading_whitespace(
    whole_lines: List[str], part_lines: List[str], replace_lines: List[str]
) -> Optional[str]:
    """Try to match part_lines ignoring uniform leading whitespace."""
    leading = [len(p) - len(p.lstrip()) for p in part_lines if p.strip()] + [
        len(p) - len(p.lstrip()) for p in replace_lines if p.strip()
    ]
    if leading and min(leading):
        num_leading = min(leading)
        part_lines = [p[num_leading:] if p.strip() else p for p in part_lines]
        replace_lines = [p[num_leading:] if p.strip() else p for p in replace_lines]

    num_part_lines = len(part_lines)
    for i in range(len(whole_lines) - num_part_lines + 1):
        add_leading = match_but_for_leading_whitespace(
            whole_lines[i : i + num_part_lines], part_lines
        )
        if add_leading is None:
            continue
        replace_lines = [add_leading + rline if rline.strip() else rline for rline in replace_lines]
        whole_lines = whole_lines[:i] + replace_lines + whole_lines[i + num_part_lines :]
        return "".join(whole_lines)
    return None


def perfect_or_whitespace(whole_lines: List[str], part_lines: List[str], replace_lines: List[str]) -> Optional[str]:
    """Try perfect match, then whitespace‑flexible match."""
    res = perfect_replace(whole_lines, part_lines, replace_lines)
    if res:
        return res
    res = replace_part_with_missing_leading_whitespace(whole_lines, part_lines, replace_lines)
    if res:
        return res
    return None


def replace_closest_edit_distance(
    whole_lines: List[str], part: str, part_lines: List[str], replace_lines: List[str]
) -> Optional[str]:
    """Fallback fuzzy replacement based on edit distance."""
    similarity_thresh = 0.8
    max_similarity = 0
    most_similar_chunk_start = -1
    most_similar_chunk_end = -1

    scale = 0.1
    min_len = math.floor(len(part_lines) * (1 - scale))
    max_len = math.ceil(len(part_lines) * (1 + scale))

    for length in range(min_len, max_len):
        for i in range(len(whole_lines) - length + 1):
            chunk = whole_lines[i : i + length]
            chunk = "".join(chunk)
            similarity = SequenceMatcher(None, chunk, part).ratio()
            if similarity > max_similarity and similarity:
                max_similarity = similarity
                most_similar_chunk_start = i
                most_similar_chunk_end = i + length

    if max_similarity < similarity_thresh:
        return None

    modified_whole = (
        whole_lines[:most_similar_chunk_start]
        + replace_lines
        + whole_lines[most_similar_chunk_end:]
    )
    return "".join(modified_whole)


def replace_most_similar_chunk(whole: str, part: str, replace: str) -> Optional[str]:
    """Main replacement driver."""
    whole, whole_lines = prep(whole)
    part, part_lines = prep(part)
    replace, replace_lines = prep(replace)

    res = perfect_or_whitespace(whole_lines, part_lines, replace_lines)
    if res:
        return res

    # drop leading empty line, GPT sometimes adds them spuriously
    if len(part_lines) > 2 and not part_lines[0].strip():
        skip_blank_line_part_lines = part_lines[1:]
        res = perfect_or_whitespace(whole_lines, skip_blank_line_part_lines, replace_lines)
        if res:
            return res

    # Try to handle when it elides code with ...
    try:
        res = try_dotdotdots(whole, part, replace)
        if res:
            return res
    except ValueError:
        pass

    # Final fuzzy fallback
    res = replace_closest_edit_distance(whole_lines, part, part_lines, replace_lines)
    return res


def try_dotdotdots(whole: str, part: str, replace: str) -> Optional[str]:
    """Handle SEARCH/REPLACE blocks containing ... lines."""
    dots_re = re.compile(r"(^\s*\.\.\.\n)", re.MULTILINE | re.DOTALL)
    part_pieces = re.split(dots_re, part)
    replace_pieces = re.split(dots_re, replace)

    if len(part_pieces) != len(replace_pieces):
        raise ValueError("Unpaired ... in SEARCH/REPLACE block")
    if len(part_pieces) == 1:
        return None  # no dots

    # Compare odd strings (the ... lines)
    all_dots_match = all(part_pieces[i] == replace_pieces[i] for i in range(1, len(part_pieces), 2))
    if not all_dots_match:
        raise ValueError("Unmatched ... in SEARCH/REPLACE block")

    part_pieces = [part_pieces[i] for i in range(0, len(part_pieces), 2)]
    replace_pieces = [replace_pieces[i] for i in range(0, len(replace_pieces), 2)]

    for p, r in zip(part_pieces, replace_pieces):
        if not p and not r:
            continue
        if not p and r:
            if not whole.endswith("\n"):
                whole += "\n"
            whole += r
            continue
        if whole.count(p) != 1:
            raise ValueError
        whole = whole.replace(p, r, 1)
    return whole


def strip_quoted_wrapping(res: str, fname: Optional[str] = None, fence: Tuple[str, str] = ("```", "```")) -> str:
    """Remove filename and fence wrapping from a SEARCH/REPLACE block."""
    if not res:
        return res
    lines = res.splitlines()
    if fname and lines and lines[0].strip().endswith(Path(fname).name):
        lines = lines[1:]
    if lines and lines[0].startswith(fence[0]) and lines[-1].startswith(fence[1]):
        lines = lines[1:-1]
    result = "\n".join(lines)
    if result and result[-1] != "\n":
        result += "\n"
    return result


def do_replace(fname: str, content: str, before_text: str, after_text: str, fence: Tuple[str, str] = ("```", "```")) -> Optional[str]:
    """Apply a single SEARCH/REPLACE edit to a file."""
    before_text = strip_quoted_wrapping(before_text, fname, fence)
    after_text = strip_quoted_wrapping(after_text, fname, fence)
    path = Path(fname)

    # create new file if SEARCH is empty
    if not path.exists() and not before_text.strip():
        path.touch()
        content = ""

    if content is None:
        return None

    if not before_text.strip():
        # append to existing file, or start a new file
        new_content = content + after_text
    else:
        new_content = replace_most_similar_chunk(content, before_text, after_text)

    return new_content


# --- Tool class ---

class CodeEditTool(Tool):
    """
    Apply SEARCH/REPLACE edits to files, similar to AIDER's editblock coder.
    """

    async def execute(self, **kwargs) -> Response:
        """
        Expected args:
            file_path: path to the file (relative to project root)
            search: the exact text to search for (SEARCH block)
            replace: the replacement text (REPLACE block)
        Alternatively:
            edits: a list of dicts with file_path, search, replace
        """
        edits = self.args.get("edits")
        if edits:
            # Process multiple edits
            results = []
            for edit in edits:
                file_path = edit.get("file_path")
                search = edit.get("search", "")
                replace = edit.get("replace", "")
                if not file_path:
                    return Response(
                        message="Error: missing 'file_path' in edit",
                        break_loop=False,
                        additional={"error": True}
                    )
                result = await self._apply_single_edit(file_path, search, replace)
                results.append(result)
            success = all(r.get("success") for r in results)
            message = "\n".join(r.get("message") for r in results)
            return Response(
                message=message,
                break_loop=False,
                additional={"success": success, "results": results}
            )
        else:
            # Single edit
            file_path = self.args.get("file_path")
            search = self.args.get("search", "")
            replace = self.args.get("replace", "")
            if not file_path:
                return Response(
                    message="Error: 'file_path' is required",
                    break_loop=False,
                    additional={"error": True}
                )
            result = await self._apply_single_edit(file_path, search, replace)
            return Response(
                message=result["message"],
                break_loop=False,
                additional=result
            )

    async def _apply_single_edit(self, file_path: str, search: str, replace: str) -> dict:
        """Apply one SEARCH/REPLACE pair to a file."""
        from pathlib import Path
        
        # Collect all possible locations to try
        candidates = []
        tried_paths_info = []  # For detailed error messages
        
        # Debug: Print agent context info for troubleshooting
        debug_info = []
        if hasattr(self.agent, 'context'):
            debug_info.append(f"Agent context available: {type(self.agent.context)}")
            # List all attributes of context
            context_attrs = [attr for attr in dir(self.agent.context) if not attr.startswith('_')]
            debug_info.append(f"Context attributes: {', '.join(context_attrs)}")
            
            # Check for project-related attributes
            if hasattr(self.agent.context, 'project'):
                debug_info.append(f"Project context available: {self.agent.context.project}")
                project_attrs = [attr for attr in dir(self.agent.context.project) if not attr.startswith('_')]
                debug_info.append(f"Project attributes: {', '.join(project_attrs)}")
                if hasattr(self.agent.context.project, 'root'):
                    debug_info.append(f"Project root: {self.agent.context.project.root}")
            
            # Check for other potential project info
            for attr in ['current_project', 'active_project', 'project_path', 'project_dir']:
                if hasattr(self.agent.context, attr):
                    debug_info.append(f"{attr}: {getattr(self.agent.context, attr)}")
            
            # Check for workspace or working directory
            if hasattr(self.agent.context, 'workspace'):
                debug_info.append(f"Workspace: {self.agent.context.workspace}")
            if hasattr(self.agent.context, 'working_directory'):
                debug_info.append(f"Working directory: {self.agent.context.working_directory}")
            
            # Inspect 'data' and 'config' attributes for project info
            if hasattr(self.agent.context, 'data'):
                debug_info.append(f"Data type: {type(self.agent.context.data)}")
                if isinstance(self.agent.context.data, dict):
                    for key, value in list(self.agent.context.data.items())[:5]:  # Limit output
                        debug_info.append(f"Data key '{key}': {value}")
            if hasattr(self.agent.context, 'config'):
                debug_info.append(f"Config type: {type(self.agent.context.config)}")
                if isinstance(self.agent.context.config, dict):
                    for key, value in list(self.agent.context.config.items())[:5]:
                        debug_info.append(f"Config key '{key}': {value}")
        
        # 1. If file_path is already absolute, try it directly
        if Path(file_path).is_absolute():
            candidate = Path(file_path).resolve()
            candidates.append(candidate)
            tried_paths_info.append(f"Absolute path: {candidate}")
        
        # 2. Try project root from agent context data
        project_root = None
        if hasattr(self.agent.context, 'data') and isinstance(self.agent.context.data, dict):
            project_name = self.agent.context.data.get('project')
            if project_name:
                # Construct project root path based on standard structure
                base_projects_dir = Path('/a0/usr/projects')
                candidate_root = base_projects_dir / project_name
                if candidate_root.exists():
                    project_root = candidate_root
                    candidate = (project_root / file_path).resolve()
                    candidates.append(candidate)
                    tried_paths_info.append(f"Relative to project root from data ({project_root}): {candidate}")
        
        # 3. Try project root from agent context attribute (old style)
        if not project_root and hasattr(self.agent.context, 'project') and hasattr(self.agent.context.project, 'root'):
            project_root = self.agent.context.project.root
            if project_root:
                candidate = (project_root / file_path).resolve()
                candidates.append(candidate)
                tried_paths_info.append(f"Relative to project root attribute ({project_root}): {candidate}")
        
        # 3. Try calculated project path based on common structure
        # Look for /a0/usr/projects/*/.a0proj directory to identify project root
        calculated_project_root = None
        current = Path.cwd()
        while current and current != current.parent:
            if (current / '.a0proj').exists():
                calculated_project_root = current
                break
            current = current.parent
        
        if calculated_project_root and calculated_project_root not in [c.parent for c in candidates if c.parent]:
            candidate = (calculated_project_root / file_path).resolve()
            candidates.append(candidate)
            tried_paths_info.append(f"Relative to calculated project root ({calculated_project_root}): {candidate}")
        
        # 4. Try relative to current working directory (fallback)
        cwd = Path.cwd()
        candidate = (cwd / file_path).resolve()
        if candidate not in candidates:
            candidates.append(candidate)
            tried_paths_info.append(f"Relative to CWD ({cwd}): {candidate}")
        
        # 5. Try the file as-is (no resolution)
        candidate = Path(file_path)
        if candidate not in candidates:
            candidates.append(candidate)
            tried_paths_info.append(f"As-is (no resolution): {candidate}")
        
        # Remove duplicates while preserving order
        unique_candidates = []
        seen = set()
        for cand in candidates:
            cand_str = str(cand)
            if cand_str not in seen:
                seen.add(cand_str)
                unique_candidates.append(cand)
        
        # Try each candidate
        abs_path = None
        tried_paths = []
        for candidate in unique_candidates:
            tried_paths.append(str(candidate))
            if candidate.exists():
                abs_path = candidate
                break
        
        if abs_path is None:
            # If search is empty, we can create the file
            if not search.strip():
                # Choose the first candidate location to create the file
                # We'll use the first candidate from unique_candidates
                if not unique_candidates:
                    # This should not happen, but fallback to the file_path as is
                    candidate = Path(file_path)
                else:
                    candidate = unique_candidates[0]
                # Create parent directories if needed
                candidate.parent.mkdir(parents=True, exist_ok=True)
                candidate.touch()
                abs_path = candidate
            else:
                error_msg = f"File not found: {file_path}\n"
                error_msg += "Tried the following locations:\n" + "\n".join(tried_paths_info)
                error_msg += "\n\nDebug info:\n" + "\n".join(debug_info) if debug_info else "\nNo debug info."
                error_msg += "\n\nPossible solutions:"
                error_msg += "\n- Use an absolute path"
                error_msg += "\n- Ensure the file exists in the current working directory"
                error_msg += "\n- Check if you're in the correct project directory"
                error_msg += "\n\nCurrent working directory: " + str(cwd)
                if project_root:
                    error_msg += "\nProject root: " + str(project_root)

                return {
                    "success": False,
                    "message": error_msg,
                    "file_path": file_path
                }


        try:
            content = abs_path.read_text(encoding="utf-8")
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to read file {file_path}: {e}",
                "file_path": file_path
            }

        new_content = do_replace(str(abs_path), content, search, replace)
        if new_content is None:
            return {
                "success": False,
                "message": f"SEARCH block did not match in {file_path}. Ensure the SEARCH block matches exactly, including whitespace and indentation. You can try:\n- Check for extra or missing spaces\n- Use the exact lines from the file\n- If using ... lines, ensure they match the omitted sections\n- Consider using absolute file path if relative path issues persist.",
                "file_path": file_path,
                "search": search,
                "replace": replace
            }

        try:
            abs_path.write_text(new_content, encoding="utf-8")
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to write file {file_path}: {e}",
                "file_path": file_path
            }

        # Log the change
        PrintStyle(font_color="#1B4F72", bold=True).print(f"Edited {file_path}")
        return {
            "success": True,
            "message": f"Successfully applied edit to {file_path}",
            "file_path": file_path,
            "changes": len(search.splitlines()) if search else 0
        }
