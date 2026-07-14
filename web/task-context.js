export const TASK_EXECUTION_CONTEXT_SCHEMA_VERSION = "1.0.0";

const HARD_RULES = Object.freeze([
  "Work only on the selected task.",
  "Do not broaden scope.",
  "Respect dependencies, allowed files, outputs, non-goals, and verification.",
  "Do not mark done without accepted proof.",
  "If required context is missing, return blocked with a clear blocker.",
  "Return one task_run JSON object only.",
]);

export function buildTaskContextCollection(rows, model, options = {}) {
  const selectedRows = Array.isArray(rows) ? rows.filter(Boolean) : [];
  const selectionMode = options.selectionMode ?? (selectedRows.length === 1 ? "task_id" : "all");
  const workspace = workspacePayload(model);
  const sourceArtifacts = sourceArtifactsPayload(model);

  return {
    schema_version: TASK_EXECUTION_CONTEXT_SCHEMA_VERSION,
    kind: "task_execution_context_collection",
    generated_at: options.generatedAt ?? new Date().toISOString(),
    selection: {
      mode: selectionMode,
      requested_task_id: options.requestedTaskId ?? (selectionMode === "task_id" ? selectedRows[0]?.id ?? null : null),
      source_task_count: Array.isArray(model?.rows) ? model.rows.length : 0,
      included_context_count: selectedRows.length,
    },
    workspace,
    snapshot: {
      git_commit: null,
      git_branch: null,
      is_dirty: null,
    },
    source_artifacts: sourceArtifacts,
    workspace_context: [],
    contexts: selectedRows.map((row) => taskContextPayload(row, model, workspace)),
  };
}

export function formatTaskContextJson(collection) {
  return `${JSON.stringify(collection, null, 2)}\n`;
}

export function formatTaskContextMarkdown(collection) {
  const contexts = Array.isArray(collection?.contexts) ? collection.contexts : [];
  if (!contexts.length) {
    const selection = collection?.selection?.mode ?? "requested";
    return `# AI Assembly Line - Task Contexts\n\nNo tasks matched the ${selection} selection.\n`;
  }

  return `${contexts.map((context) => formatOneTaskContext(collection, context).trimEnd()).join("\n")}\n`;
}

function workspacePayload(model) {
  const projectContext = model?.projectContext;
  const mode = projectContext?.mode ?? "root";
  return {
    mode: mode === "standalone" ? "standalone" : (mode === "project" ? "project" : "root"),
    project_id: projectContext?.projectId ?? model?.state?.workspace_id ?? "root",
    project_name: projectContext?.projectName ?? "Root Generated State",
    workspace_root: projectContext?.workspaceRootPath || ".",
    task_run_path_prefix: model?.taskRunPathPrefix ?? "generated/task_runs/",
  };
}

function sourceArtifactsPayload(model) {
  const configuredPaths = model?.projectContext?.workspace?.paths ?? {};
  const generatedPaths = configuredPaths.generated ?? {};
  const promptsDirectory = configuredPaths.prompts ?? "prompts";
  const contractsDirectory = configuredPaths.contracts ?? "contracts";

  return [
    {
      id: "task_backlog",
      path: generatedPaths.task_backlog ?? "generated/task_backlog.json",
      format: "json",
      description: "Canonical task definitions.",
    },
    {
      id: "collaboration_state",
      path: generatedPaths.collaboration_state ?? "generated/collaboration_state.json",
      format: "json",
      description: "Current assignment, claim, review, and proof state.",
    },
    {
      id: "task_executor_prompt",
      path: joinPath(promptsDirectory, "07-task-executor.md"),
      format: "markdown",
      description: "Task-executor operating rules.",
    },
    {
      id: "task_run_schema",
      path: joinPath(contractsDirectory, "task_run.schema.json"),
      format: "json",
      description: "Required task-run return contract.",
    },
  ];
}

function taskContextPayload(row, model, workspace) {
  const dependencyRows = (row.dependsOn ?? [])
    .map((dependencyId) => model?.rowsById?.get(dependencyId))
    .filter(Boolean);
  const instructionsPath = sourceArtifactPath(model, "prompts", "07-task-executor.md", "prompts/07-task-executor.md");
  const schemaPath = sourceArtifactPath(model, "contracts", "task_run.schema.json", "contracts/task_run.schema.json");
  const taskRunPath = `${workspace.task_run_path_prefix}${row.id}.json`;

  return {
    task_id: row.id,
    title: row.title,
    summary: row.summary ?? "",
    task: row.task,
    dispatch: {
      status: row.dispatchStatus,
      reason: row.dispatchReason,
      planning_status: row.planningStatus,
      execution_status: row.executionStatus,
      assignment: row.assignment ?? { task_id: row.id, status: "unclaimed" },
      active_claim: row.activeClaim ?? null,
      assignee: assigneePayload(row),
      updated_at: row.updatedAt || null,
      dependencies: dependencyRows.map((dependency) => dependencyPayload(dependency)),
      missing_dependency_ids: row.missingDependencies ?? [],
      blocked_dependency_ids: (row.blockedDependencies ?? []).map((dependency) => dependency.id),
      unfinished_dependency_ids: (row.unfinishedDependencies ?? []).map((dependency) => dependency.id),
    },
    executor: {
      target: "unspecified",
      instructions_path: instructionsPath,
      task_run_schema_path: schemaPath,
      expected_task_run_path: taskRunPath,
      hard_rules: [...HARD_RULES],
      environment_guidance: [],
      return_status_guidance: {
        review: "Use status review when implementation appears complete but still needs human review.",
        blocked: "Use status blocked if required context or dependencies are missing.",
      },
      return_template: returnTemplate(row.id),
    },
  };
}

function sourceArtifactPath(model, workspaceKey, fileName, fallback) {
  const configured = model?.projectContext?.workspace?.paths?.[workspaceKey];
  return typeof configured === "string" && configured.trim() ? joinPath(configured, fileName) : fallback;
}

function assigneePayload(row) {
  const actorId = row.actor?.actor_id ?? row.assignment?.assigned_to ?? row.activeClaim?.actor_id ?? null;
  if (!actorId) {
    return null;
  }
  return {
    actor_id: actorId,
    display_name: row.assignedTo,
    kind: row.assigneeType,
  };
}

function dependencyPayload(dependency) {
  return {
    task_id: dependency.id,
    title: dependency.title,
    dispatch_status: dependency.dispatchStatus,
    execution_status: dependency.executionStatus,
    reason: dependency.dispatchReason,
    proof: dependency.proof ?? [],
  };
}

function returnTemplate(taskId) {
  return {
    schema_version: "0.1.0",
    task_id: taskId,
    run_id: "<unique-run-id>",
    actor_id: "<your-actor-id>",
    status: "review",
    implementation_summary: "<what changed>",
    files_changed: [],
    verification: [],
    proof: [],
    blockers: [],
    notes: "<optional notes>",
    updated_at: "<ISO-8601 timestamp>",
  };
}

function formatOneTaskContext(collection, context) {
  const workspace = collection.workspace;
  const dispatch = context.dispatch;
  const executor = context.executor;
  const assignee = dispatch.assignee ?? { display_name: "Unassigned", kind: "unassigned" };
  const documents = formatContextDocuments(collection.workspace_context);
  const environmentGuidance = executor.environment_guidance?.length
    ? `\n\n## Environment Guidance\n\n${executor.environment_guidance.map((guidance) => `- ${guidance}`).join("\n")}`
    : "";
  const documentsSection = documents ? `\n\n${documents}` : "";

  return `--- CONTEXT ${context.task_id} START ---

# AI Assembly Line - One Task Execution Context

You are executing exactly one task from the AI Assembly Line backlog.

Project: ${workspace.project_name}
Project ID: ${workspace.project_id}
Workspace: ${workspace.workspace_root}
${formatSnapshot(collection.snapshot)}

Use the task executor rules from:
${executor.instructions_path}

Hard rules:
${executor.hard_rules.map((rule) => `- ${rule}`).join("\n")}

Expected output path:
${executor.expected_task_run_path}

Dispatch status: ${dispatch.status}
Reason: ${dispatch.reason}
Assigned to: ${assignee.display_name} (${assignee.kind})
Updated at: ${dispatch.updated_at ?? "not recorded"}${documentsSection}${environmentGuidance}

## Selected Task JSON

\`\`\`json
${JSON.stringify(context.task, null, 2)}
\`\`\`

## Current Assignment Metadata

\`\`\`json
${JSON.stringify(dispatch.assignment, null, 2)}
\`\`\`

## Active Claim Metadata

\`\`\`json
${JSON.stringify(dispatch.active_claim ?? { task_id: context.task_id, status: "none" }, null, 2)}
\`\`\`

## Dependency Summary

${formatDependencies(dispatch.dependencies)}${formatMissingDependencies(dispatch.missing_dependency_ids)}

## Dependency Proof Summaries

${formatProofSummaries(dispatch.dependencies)}

## Required Return Shape

Return exactly one JSON object compatible with \`${executor.task_run_schema_path}\`:

\`\`\`json
${JSON.stringify(executor.return_template, null, 2)}
\`\`\`

${executor.return_status_guidance.review}
${executor.return_status_guidance.blocked}
Do not mark done without accepted proof.

--- CONTEXT ${context.task_id} END ---
`;
}

function formatSnapshot(snapshot) {
  if (!snapshot?.git_commit) {
    return "Git snapshot: unavailable.";
  }
  const branch = snapshot.git_branch ?? "detached HEAD";
  const dirty = snapshot.is_dirty ? "dirty" : "clean";
  return `Git snapshot: ${snapshot.git_commit} on ${branch} (${dirty}).`;
}

function formatContextDocuments(documents) {
  if (!Array.isArray(documents) || !documents.length) {
    return "";
  }
  return [
    "## Workspace Context",
    "",
    ...documents.flatMap((document) => [
      `### ${document.title}`,
      `Source: \`${document.path}\``,
      "",
      document.content || "(empty)",
      "",
    ]),
  ].join("\n").trim();
}

function formatDependencies(dependencies) {
  if (!dependencies.length) {
    return "- No dependencies.";
  }
  return dependencies.map((dependency) => [
    `- ${dependency.task_id}: ${dependency.dispatch_status}`,
    `  title: ${dependency.title}`,
    `  execution_status: ${dependency.execution_status}`,
    `  reason: ${dependency.reason}`,
    `  proof: ${proofSummary(dependency.proof)}`,
  ].join("\n")).join("\n");
}

function formatMissingDependencies(missingDependencyIds) {
  return missingDependencyIds?.length
    ? `\nMissing dependency reference(s): ${missingDependencyIds.join(", ")}`
    : "";
}

function formatProofSummaries(dependencies) {
  if (!dependencies.length) {
    return "- No dependency proof required.";
  }
  return dependencies.map((dependency) => `- ${dependency.task_id}: ${proofSummary(dependency.proof)}`).join("\n");
}

function proofSummary(proofItems) {
  if (!Array.isArray(proofItems) || !proofItems.length) {
    return "no proof recorded";
  }
  return proofItems.map((item) => {
    const bits = [item?.kind, item?.status, item?.path, item?.summary].filter(Boolean);
    return bits.length ? bits.join(" / ") : "proof";
  }).join("; ");
}

function joinPath(directory, filename) {
  const cleanDirectory = String(directory ?? "").replace(/\\/g, "/").replace(/^\/+|\/+$/g, "");
  return cleanDirectory ? `${cleanDirectory}/${filename}` : filename;
}
