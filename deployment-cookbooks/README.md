# deployment-cookbooks/

This folder contains operational cookbooks for users deploying the `claude-for-customer-success` plugin suite.

---

## What's in This Folder

| File | Description |
|------|-------------|
| `solo-csm-cookbook.md` | Solo CSM Cookbook — step-by-step operational guide for individual CSMs deploying the full plugin suite for personal use across the customer lifecycle |

---

## Important: These Are Reference Builds

**The plugins and cookbooks in this repository are reference builds, not plug-and-play deployments.**

A reference build means:

- **The architecture and workflows are proven**, but they are designed around generalizable patterns, not any specific company's systems, data sources, naming conventions, or CS motion.
- **Every deployment requires tailoring.** Before any plugin or cookbook produces useful output, it must be configured for the environment it runs in — your CRM, your customer data schema, your product terminology, your team's process definitions, your outcome vocabulary.
- **The cold-start interview is not optional.** It is the mechanism that converts a reference build into a deployment. Skipping it means the plugins operate on defaults that will not match your context.
- **Skill commands are starting points, not finished automations.** Many commands will need their prompts, filters, or output formats adjusted to reflect how your team actually works.

### What "Tailoring" Means in Practice

| What needs tailoring | Why |
|---|---|
| Data source connections | The plugins reference connector types (CRM, CSP, product analytics); you wire in the specific tools your company uses |
| Outcome statements | The Provisional Outcome Catalog is generated from public product information; it must be reviewed and validated against your actual customer outcomes |
| Account segmentation rules | Health thresholds, segment labels, and escalation triggers are set to generic defaults; they need to match your team's definitions |
| Agent activation choices | Not every managed agent applies to every CS motion; activation decisions should reflect your team's coverage model |
| Playbook language | TARO plays and skill command outputs use neutral framing; you may need to adjust tone, terminology, and escalation paths to match your organization |

### Who Should Tailor

Someone with working knowledge of both the Claude plugin ecosystem and the target CS environment. Tailoring is not a technical job — it does not require writing code — but it does require understanding what the plugins are doing and what the organization expects from them.

---

## Adding New Cookbooks

If you build a cookbook for a specific role, motion, or deployment variant, add it to this folder and update the table above. Include an **Audience** line and a **Status** signal (`[DRAFT]`, `[PROPOSED]`, or `[VALIDATED]`) at the top of the file.
