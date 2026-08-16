# Using the guidance in an application that has one AI project

This is the recommended profile for a normal product/application where MAF is only one integration/orchestration module.

## Target shape

```text
MyProduct/
├── AGENTS.md                         # product-wide rules and dependency boundaries
├── .agents/
│   ├── references/
│   └── skills/maf-*/                 # one shared MAF knowledge layer
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

## Install

From the guidance-pack repository:

```bash
python3 scripts/install-guidance.py \
  --profile application-with-ai-module \
  --target /path/to/MyProduct \
  --ai-path src/MyProduct.AI
```

If the target already has a root `AGENTS.md`, the installer preserves it and writes the proposed AI-boundary fragment to `.maf-guidance/AGENTS.root-fragment.md` for manual merge.

It never silently overwrites differing guidance unless `--force` is explicitly passed.

## What remains shared

Do not duplicate the MAF skills into the AI project. Keep them once under repository-root `.agents/skills/`. Their descriptions provide discovery and the selected skill loads detailed guidance only when needed.
