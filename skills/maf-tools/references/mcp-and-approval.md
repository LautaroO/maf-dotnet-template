# MCP and approval

MAF .NET can use tools discovered through the official MCP C# SDK and expose them as AI tools/functions to supported agents.

Use MCP when you want an interoperable external tool server boundary, not simply because an API exists.

The 1.24 `Microsoft.Agents.AI.Mcp` package is published as alpha. Basic local tool integration can use the official MCP C# SDK directly; do not require this package for every MCP tool or describe its experimental skill/task integrations as stable merely because core MAF is stable.

Checklist:

- trust the server/operator;
- constrain transports/endpoints;
- keep credentials out of prompts/tool descriptions;
- expose only needed tools;
- validate tenant/user scope outside the model;
- log/audit consequential calls appropriately;
- handle cancellation/timeouts;
- use approval for destructive or expensive actions;
- assume remote tool output can contain malicious/prompt-injection content.

Hosted/provider-owned MCP is provider-specific. Keep it behind a capability adapter if portability matters. Local/client-side MCP integration is usually more portable across compatible agent/provider combinations.

## Release-sensitive approval and task contracts

The [1.19 release](https://github.com/microsoft/agent-framework/releases/tag/dotnet-1.19.0) reports a breaking migration of MCP long-running tasks to the 2026-07-28 Tasks extension. Verify client/server SDK and extension compatibility rather than treating a task as an ordinary synchronous function call.

The [1.22 release](https://github.com/microsoft/agent-framework/releases/tag/dotnet-1.22.0) changes approval replay binding and scopes provider-backed MCP sessions per invocation. [1.23](https://github.com/microsoft/agent-framework/releases/tag/dotnet-1.23.0) strengthens approval response binding and changes tool updates between runs; [1.24](https://github.com/microsoft/agent-framework/releases/tag/dotnet-1.24.0) binds approval headers to the approved invocation. Preserve request identity, arguments, session and caller across resume; reject fabricated, changed and cross-session approval responses. Retest middleware replacement and hosted adapters so direct invocation cannot bypass the approval gate. Use installed framework approval types rather than rebuilding binding from prompt text.
