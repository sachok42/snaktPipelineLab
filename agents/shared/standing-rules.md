# Shared Standing Rules 

These rules apply to every pipeline agent unless a role instruction narrows them. 
%% Stored here to not repeat them in each of the instructions files.

## Make Problems Visible

List every problem encountered in a human-readable section before finishing, even when the step otherwise succeeds. 
%% collecting feedback for the operator to adjust the prompts next time

## Preserve Work Products

Commit every work product before replacing or discarding it. A verified replacement must already be in place before any work product is removed. 
%% So whenever LLMs fail, we can look at what went wrong and whether LLMs are stupid or we lack some feature

## Branch Writes

Agents that change feature-repository code push those changes to the feature branch. Collect code work produced during a pipeline run into a single pull request targeting `main`. 
%% Everything should be collected into a united pull request to be properly analysed

## Missing Information

When a required artifact, datum, or instruction is missing, ask the agent that gave you the task. The Orchestrator asks the operator. If one full escalation cycle passes without a response, document the question in an incident record, take the most conservative safe action, and flag the fallback in your transcript. 
%% A fallback in case of some important instructions or data missing
