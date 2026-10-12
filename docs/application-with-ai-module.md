# Using the guidance in an application that has one AI project

This is the recommended profile for a normal product/application where MAF is only one integration/orchestration module.

## Target shape

This example uses the installed plugin for shared skills/resources and keeps only project-specific instructions in the application.

```text
MyProduct/
├── AGENTS.md                         # product-wide rules and dependency boundaries
└── src/
    ├── MyProduct.Domain/
    ├── MyProduct.Application/
    ├── MyProduct.Infrastructure/
    ├── MyProduct.Api/
    └── MyProduct.AI/
        ├── AGENTS.md                 # MAF-specific local rules
        ├── Agents/
        ├── Workflows/
        ├── Tools/
        ├── Context/
        └── Providers/
```

The exact clean-architecture layering is not prescribed. What matters is that the AI module does not become the owner of product/domain behavior.

## Why nested instructions

Codex reads project instructions from the repository root down toward the working directory. A nested `src/MyProduct.AI/AGENTS.md` therefore refines the product rules only for work performed in that subtree.

That gives two useful scopes:

- root: product architecture, domain boundaries, commands, conventions;
- AI project: MAF abstractions, provider isolation, agent/workflow/tool rules.

## Dependency rule

Conceptually prefer:

```text
Domain <- Application <- AI
```

The AI project may adapt/call application capabilities. Domain/application projects should not need MAF or provider SDK references to serve non-AI use cases.

## Example

Suppose the application already has:

```csharp
public interface IOrderPricingUseCase
{
    Task<OrderPrice> GetPriceAsync(Guid orderId, CancellationToken cancellationToken);
}
```

The AI tool can expose a model-friendly contract and delegate:

```csharp
public sealed class GetOrderPriceTool(IOrderPricingUseCase pricing)
{
    public Task<OrderPrice> ExecuteAsync(Guid orderId, CancellationToken cancellationToken)
        => pricing.GetPriceAsync(orderId, cancellationToken);
}
```

The tool should not reimplement discounts, tax rules, eligibility, or persistence. Those remain application/domain concerns.

## Adopt manually

Use the installed plugin's shared knowledge layer. Merge its `resources/profiles/application-with-ai-module/AGENTS.root-fragment.md` into the existing root instructions without replacing them, then copy `AGENTS.ai-module.md` into the AI subtree as `AGENTS.md`.

Invoke `$maf-adoption` so Codex inspects solution/package/command evidence and populates the project context. There is intentionally no installer or force-overwrite path.

## What remains shared

Do not duplicate the MAF skills into the AI project. Keep the shared skills in the installed plugin. Their descriptions provide discovery and the selected skill loads detailed guidance only when needed.
