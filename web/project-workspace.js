const PROJECT_REGISTRY_URL = "../projects/index.json";

const ROOT_PROJECT_CONTEXT = Object.freeze({
  mode: "root",
  projectId: null,
  projectName: "Root Generated State",
  projectStatus: "seed",
  workspacePath: null,
  workspaceRootPath: "",
  workspaceRootUrl: "../",
  taskRunPathPrefix: "generated/task_runs/",
  registry: null,
  workspace: null,
  project: null,
  projects: [],
  requestedProjectId: "",
});

export async function loadProjectContext() {
  const requestedProjectId = getRequestedProjectId();
  const registryResult = await fetchOptionalJson(PROJECT_REGISTRY_URL);

  if (!registryResult.ok) {
    if (requestedProjectId) {
      throw new Error(`Project "${requestedProjectId}" was requested, but projects/index.json could not be loaded: ${registryResult.error}`);
    }
    return { ...ROOT_PROJECT_CONTEXT, requestedProjectId };
  }

  const registry = registryResult.payload;
  const projects = Array.isArray(registry.projects) ? registry.projects : [];
  const project = chooseProject(projects, registry.default_project_id, requestedProjectId);

  if (!project) {
    if (requestedProjectId) {
      throw new Error(`Project "${requestedProjectId}" was not found in projects/index.json.`);
    }
    return { ...ROOT_PROJECT_CONTEXT, registry, projects, requestedProjectId };
  }

  const workspaceUrl = `../${trimSlashes(project.workspace_path)}`;
  const workspace = await fetchJson(workspaceUrl, `project workspace for ${project.project_id}`);
  const workspaceRootPath = project.workspace_path.replace(/project_workspace\.json$/, "");
  const workspaceRootUrl = `../${workspaceRootPath}`;

  if (workspace.project_id !== project.project_id) {
    throw new Error(`Project registry id "${project.project_id}" does not match workspace id "${workspace.project_id}".`);
  }

  const taskRunsDir = workspace.paths?.generated?.task_runs_dir ?? "generated/task_runs";
  return {
    mode: "project",
    projectId: project.project_id,
    projectName: project.name,
    projectStatus: project.status,
    workspacePath: project.workspace_path,
    workspaceRootPath,
    workspaceRootUrl,
    taskRunPathPrefix: joinPath(workspaceRootPath, ensureTrailingSlash(taskRunsDir)),
    registry,
    workspace,
    project,
    projects,
    requestedProjectId,
  };
}

export function projectUrlForPage(pageHref, projectContext) {
  if (!projectContext || projectContext.mode !== "project" || !projectContext.projectId) {
    return pageHref;
  }

  const [path, hash = ""] = pageHref.split("#");
  const separator = path.includes("?") ? "&" : "?";
  return `${path}${separator}project=${encodeURIComponent(projectContext.projectId)}${hash ? `#${hash}` : ""}`;
}

export function renderProjectLabel(projectContext) {
  if (!projectContext || projectContext.mode === "root") {
    return "Root Generated State";
  }

  return `${projectContext.projectName} (${projectContext.projectId})`;
}

export function workspaceDisplayPath(projectContext, relativePath) {
  const cleanRelative = trimSlashes(relativePath);
  if (!projectContext || projectContext.mode !== "project") {
    return cleanRelative;
  }

  return joinPath(projectContext.workspaceRootPath, cleanRelative);
}

export function workspaceFetchPath(projectContext, relativePath) {
  const cleanRelative = trimSlashes(relativePath);
  if (!projectContext || projectContext.mode !== "project") {
    return `../${cleanRelative}`;
  }

  if (cleanRelative.startsWith("projects/")) {
    return `../${cleanRelative}`;
  }

  return joinUrl(projectContext.workspaceRootUrl, cleanRelative);
}

export function getRequestedProjectId() {
  return new URLSearchParams(window.location.search).get("project")?.trim() ?? "";
}

export function buildProjectSelectionUrl(projectId) {
  const pageName = window.location.pathname.split("/").pop() || "index.html";
  const params = new URLSearchParams(window.location.search);

  if (projectId) {
    params.set("project", projectId);
  } else {
    params.delete("project");
  }

  const query = params.toString();
  return `${pageName}${query ? `?${query}` : ""}${window.location.hash}`;
}

function chooseProject(projects, defaultProjectId, requestedProjectId) {
  if (requestedProjectId) {
    return projects.find((project) => project.project_id === requestedProjectId) ?? null;
  }

  if (defaultProjectId) {
    const defaultProject = projects.find((project) => project.project_id === defaultProjectId);
    if (defaultProject) {
      return defaultProject;
    }
  }

  return projects.find((project) => project.status === "active") ?? projects[0] ?? null;
}

async function fetchOptionalJson(url) {
  try {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) {
      return { ok: false, payload: null, error: `${response.status} ${response.statusText}` };
    }
    return { ok: true, payload: await response.json(), error: "" };
  } catch (error) {
    return { ok: false, payload: null, error: formatError(error) };
  }
}

async function fetchJson(url, label) {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to fetch ${label} at ${url}: ${response.status} ${response.statusText}`);
  }

  try {
    return await response.json();
  } catch (error) {
    throw new Error(`Failed to parse ${label} at ${url}: ${formatError(error)}`);
  }
}

function joinUrl(root, relativePath) {
  return `${ensureTrailingSlash(root)}${trimSlashes(relativePath)}`;
}

function joinPath(root, relativePath) {
  const cleanRoot = trimSlashes(root);
  const cleanRelative = trimSlashes(relativePath);
  if (!cleanRoot) {
    return cleanRelative;
  }
  if (!cleanRelative) {
    return `${cleanRoot}/`;
  }
  return `${cleanRoot}/${cleanRelative}`;
}

function ensureTrailingSlash(value) {
  return value.endsWith("/") ? value : `${value}/`;
}

function trimSlashes(value) {
  return String(value ?? "").replace(/^\/+|\/+$/g, "");
}

function formatError(error) {
  return error instanceof Error ? error.message : String(error);
}
