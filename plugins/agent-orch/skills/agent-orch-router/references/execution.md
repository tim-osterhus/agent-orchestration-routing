# Execution compatibility note

Execution instructions live in [shared dispatch](dispatch.md), the selected mode linked from the [entrypoint](../SKILL.md), and conditional provider references. Ordinary native routing does not require this compatibility note or the offline planner.

For configurable external CLI plans, see [configuration](../../../docs/configuration.md) and [controller adapters](../../../docs/controller-designs.md). Claude work uses the installed Claude Delegation skill and its selected launch reference. These adapters do not dispatch native workers.
