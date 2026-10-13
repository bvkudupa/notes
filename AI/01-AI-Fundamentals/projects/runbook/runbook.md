# esc bash Service Runbook

## Deployments
- Deploys run from the `main` branch through the `deploy` pipeline.
- To roll back, run `escctl rollback <service> --to-previous`. A rollback takes about 90 seconds.
- Any production deploy after 6pm must be approved by the on-call engineer.

## Ownership
- The billing service is owned by the Payments team (Slack channel #team-payments).
- The reports API is owned by the Data team.

## Incidents
- The Sev-1 phone bridge is 900-555-0142, access code 4417.
- Always open an incident doc from the template before paging anyone.