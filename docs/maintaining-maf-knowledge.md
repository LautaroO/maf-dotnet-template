# Maintaining stable MAF architectural guidance

Maintain decisions and useful methods rather than mirror a fast-changing SDK. The primary implementation reference is the [official MAF repository](https://github.com/microsoft/agent-framework); the [source investigation guide](../resources/references/official-sources.md) explains how to match its .NET code/samples with an adopting project's actual package surface.

## What changes this plugin

Update a skill, concept reference or pattern when an architectural abstraction changes materially, a real usage scenario exposes a gap, or a behavioral evaluation demonstrates a recurring mistake. A new release or patch alone is not a maintenance task. Keep exact signatures, package maturity/default claims, migration recipes and release fixes in project-specific implementation evidence where needed, not a shared plugin knowledge matrix.

1. Identify the observed problem or changed design decision and its owning topic.
2. Inspect relevant official .NET evidence; distinguish framework responsibility from provider/cloud setup. Record uncertainty when local packages, matching source or network access are unavailable.
3. Change only the useful conceptual guidance, pattern or investigation procedure. Preserve authorization, tenancy, state lifetime, bounded execution, provider neutrality and project process ownership.
4. Exercise representative responses/actions for the changed behavior, including cases where no new question or finding is needed. Fixture schema validation does not prove assistant behavior.
5. Update active docs and Unreleased notes, run repository validation, Python compilation, unittest discovery, embedded shell syntax and diff whitespace checks. Check changed links; report untested client/runtime behavior.

## Context and release boundaries

Application instructions record project facts and canonical design links; they do not copy the plugin or impose a second development process. Skill roots route tasks; references retain durable concepts and relevant tradeoffs; the pattern catalog explains when alternatives fit.

There is no scheduled source audit, compatibility matrix, release coverage index or automated maintenance issue flow. Previous dated reviews are historical records, and retired artifacts remain accessible in Git history. Do not promote their evidence into current support claims.

Plugin releases still synchronize plugin.json, VERSION and changelog, and require the existing native/fresh-session checks. A plugin release does not certify a MAF version. Default CI stays standard-library Python and live-model-free; SDK compilation and provider/runtime behavior are checked in an adopting application, not asserted here.
