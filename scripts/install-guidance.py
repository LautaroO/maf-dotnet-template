#!/usr/bin/env python3
"""Install the MAF Codex guidance pack into a target repository.

Profiles control AGENTS.md placement; the shared .agents/ knowledge layer is reused.
The installer is conservative: it does not overwrite differing files unless --force is used.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED_AGENTS = ROOT / ".agents"
PROFILES = ROOT / "profiles"


def same_content(a: Path, b: Path) -> bool:
    return a.is_file() and b.is_file() and a.read_bytes() == b.read_bytes()


def copy_file(src: Path, dst: Path, *, force: bool) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if same_content(src, dst):
            return f"unchanged {dst}"
        if not force:
            raise FileExistsError(
                f"Refusing to overwrite existing file: {dst}. Merge it manually or rerun with --force."
            )
    shutil.copy2(src, dst)
    return f"installed {dst}"


def copy_tree(src: Path, dst: Path, *, force: bool) -> list[str]:
    messages: list[str] = []
    for path in sorted(src.rglob("*")):
        if not path.is_file():
            continue
        messages.append(copy_file(path, dst / path.relative_to(src), force=force))
    return messages


def install_shared(target: Path, force: bool) -> list[str]:
    return copy_tree(SHARED_AGENTS, target / ".agents", force=force)


def install_ai_first(target: Path, force: bool) -> list[str]:
    messages = install_shared(target, force)
    messages.append(
        copy_file(PROFILES / "ai-first" / "AGENTS.md", target / "AGENTS.md", force=force)
    )
    return messages


def install_application_module(target: Path, ai_path: str | None, force: bool) -> list[str]:
    if not ai_path:
        raise ValueError("--ai-path is required for profile 'application-with-ai-module'.")

    messages = install_shared(target, force)
    profile = PROFILES / "application-with-ai-module"
    ai_dir = (target / ai_path).resolve()
    try:
        ai_dir.relative_to(target.resolve())
    except ValueError as exc:
        raise ValueError("--ai-path must stay inside the target repository.") from exc

    ai_dir.mkdir(parents=True, exist_ok=True)
    messages.append(copy_file(profile / "AGENTS.ai-module.md", ai_dir / "AGENTS.md", force=force))

    root_agents = target / "AGENTS.md"
    fragment = profile / "AGENTS.root-fragment.md"
    if not root_agents.exists():
        messages.append(copy_file(fragment, root_agents, force=False))
        messages.append("created root AGENTS.md from the AI boundary fragment; add your product-wide rules there")
    else:
        handoff = target / ".maf-guidance" / "AGENTS.root-fragment.md"
        messages.append(copy_file(fragment, handoff, force=force))
        messages.append(
            f"root AGENTS.md was preserved; merge the AI boundary section from {handoff} into it"
        )
    return messages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="Target repository root")
    parser.add_argument(
        "--profile",
        required=True,
        choices=("ai-first", "application-with-ai-module"),
        help="Adoption profile",
    )
    parser.add_argument(
        "--ai-path",
        help="AI module path relative to the target root, e.g. src/MyProduct.AI",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite conflicting guidance files. Use only after reviewing local customizations.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = Path(args.target).expanduser().resolve()
    if not target.is_dir():
        print(f"Target repository does not exist or is not a directory: {target}", file=sys.stderr)
        return 2

    try:
        if args.profile == "ai-first":
            messages = install_ai_first(target, args.force)
        else:
            messages = install_application_module(target, args.ai_path, args.force)
    except (FileExistsError, ValueError) as exc:
        print(f"Installation stopped: {exc}", file=sys.stderr)
        return 1

    for message in messages:
        print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
