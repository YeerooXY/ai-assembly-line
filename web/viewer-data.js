export const DATA_FILES = {
  projectSpec: "../generated/project_spec.json",
  repoPlan: "../generated/repo_plan.json",
  taskBacklog: "../generated/task_backlog.json",
  agentPrompts: "../generated/agent_prompts.json",
  slotsDb: "../generated/slots_db.json",
  planningRunsIndex: "../generated/planning_runs_index.json",
};

export const CONTRACT_FILES = {
  projectSpecSchema: "../contracts/project_spec.schema.json",
  repoPlanSchema: "../contracts/repo_plan.schema.json",
  taskSchema: "../contracts/task.schema.json",
  taskBatchIndexSchema: "../contracts/task_batch_index.schema.json",
  taskBatchSchema: "../contracts/task_batch.schema.json",
  slotSchema: "../contracts/slot.schema.json",
  agentPromptSchema: "../contracts/agent_prompt.schema.json",
  collaborationStateSchema: "../contracts/collaboration_state.schema.json",
  apiContract: "../contracts/api_contract.openapi.yaml",
};

export const FILE_NAMES = {
  projectSpec: "project_spec.json",
  repoPlan: "repo_plan.json",
  taskBacklog: "task_backlog.json",
  agentPrompts: "agent_prompts.json",
  slotsDb: "slots_db.json",
  planningRunsIndex: "planning_runs_index.json",
};

export async function loadGeneratedState(requiredKeys) {
  const entries = await Promise.all(
    requiredKeys.map(async (key) => {
      const path = DATA_FILES[key];
      const response = await fetch(path, { cache: "no-store" });

      if (!response.ok) {
        throw new Error(`Failed to fetch ${path}: ${response.status} ${response.statusText}`);
      }

      try {
        return [key, await response.json()];
      } catch (error) {
        throw new Error(`Failed to parse ${path}: ${formatError(error)}`);
      }
    }),
  );

  return Object.fromEntries(entries);
}

export async function loadLocalState(requiredKeys, files) {
  const fileMap = new Map(Array.from(files ?? []).map((file) => [file.name, file]));

  for (const key of requiredKeys) {
    const fileName = FILE_NAMES[key];
    if (!fileMap.has(fileName)) {
      throw new Error(`Missing required file: ${fileName}`);
    }
  }

  const entries = await Promise.all(
    requiredKeys.map(async (key) => {
      const fileName = FILE_NAMES[key];
      const raw = await fileMap.get(fileName).text();

      try {
        return [key, JSON.parse(raw)];
      } catch (error) {
        throw new Error(`Failed to parse ${fileName}: ${formatError(error)}`);
      }
    }),
  );

  return Object.fromEntries(entries);
}

export async function loadTextFile(path) {
  const response = await fetch(path, { cache: "no-store" });

  if (!response.ok) {
    throw new Error(`Failed to fetch ${path}: ${response.status} ${response.statusText}`);
  }

  return response.text();
}

export function sourceFilesForKeys(requiredKeys) {
  return requiredKeys.map((key) => `generated/${FILE_NAMES[key]}`);
}

export function isFileProtocol() {
  return window.location.protocol === "file:";
}

export function formatError(error) {
  return error instanceof Error ? error.message : String(error);
}
