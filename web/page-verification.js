import { escapeHtml, initializeViewerPage, renderCardGrid, renderChipRow, renderList } from "./viewer-layout.js";

initializeViewerPage({
  pageId: "verification",
  eyebrow: "Verification",
  title: "Verification Rules And Proof Requirements",
  description: "Read-only verification view assembled from the generated project spec, backlog, prompts, and slots.",
  requiredKeys: ["projectSpec", "taskBacklog", "agentPrompts", "slotsDb"],
  renderContent(container, data) {
    const taskGroups = groupTaskVerification(data.taskBacklog);
    const promptCards = data.agentPrompts.prompts.map(
      (prompt) => `
        <article class="card">
          <div class="chip-row">
            <span class="chip">${escapeHtml(prompt.role)}</span>
            <span class="chip">${escapeHtml(prompt.target_repo)}</span>
          </div>
          <h3>${escapeHtml(prompt.prompt_id)}</h3>
          <h4>Verification Required</h4>
          ${renderList(prompt.verification_required)}
          <h4>Task Boundaries</h4>
          ${renderList(prompt.task_boundaries)}
        </article>
      `,
    );

    const slotCards = data.slotsDb.map(
      (slot) => `
        <article class="card">
          <div class="chip-row">
            <span class="chip">${escapeHtml(slot.role)}</span>
            <span class="chip status-${escapeHtml(slot.status)}">${escapeHtml(slot.status)}</span>
          </div>
          <h3>${escapeHtml(slot.slot_id)}</h3>
          <h4>Verification Requirements</h4>
          ${renderList(slot.verification_requirements)}
        </article>
      `,
    );

    container.innerHTML = `
      <div class="stack">
        ${renderCardGrid(
          `
            <article class="card">
              <h2>Source Of Truth Notes</h2>
              <p class="muted">This page renders verification expectations from generated JSON only and keeps the frontend read-only.</p>
              <h3>Generated Artifacts</h3>
              ${renderList([
                "generated/project_spec.json defines top-level verification tasks and scope boundaries.",
                "generated/task_backlog.json defines task acceptance criteria and proof checks.",
                "generated/agent_prompts.json defines role-level verification requirements.",
                "generated/slots_db.json defines slot verification requirements.",
              ])}
            </article>
            <article class="card">
              <h2>Project Verification Rules</h2>
              <h3>Verification Tasks</h3>
              ${renderList(data.projectSpec.verification_tasks)}
              <h3>Safety Boundaries</h3>
              ${renderList(data.projectSpec.safety_boundaries)}
            </article>
          `,
          "two-up",
        )}

        <section class="card">
          <div class="section-heading">
            <h2>Backlog Proof Requirements</h2>
            <span class="chip">${data.taskBacklog.length} task${data.taskBacklog.length === 1 ? "" : "s"}</span>
          </div>
          <div class="stack">
            ${taskGroups
              .map(
                ([repoTarget, tasks]) => `
                  <article class="card inset-card">
                    <div class="section-heading">
                      <div>
                        <h3>${escapeHtml(repoTarget)}</h3>
                        <p class="muted">Acceptance criteria and verification steps grouped by existing <code>repo_target</code>.</p>
                      </div>
                      <span class="chip">${tasks.length} task${tasks.length === 1 ? "" : "s"}</span>
                    </div>
                    <div class="stack">
                      ${tasks
                        .map(
                          (task) => `
                            <div class="card inset-card">
                              <div class="chip-row">
                                <span class="chip">${escapeHtml(task.id)}</span>
                                <span class="chip">${escapeHtml(task.owner_role)}</span>
                              </div>
                              <h4>${escapeHtml(task.title)}</h4>
                              <div class="card-grid two-up">
                                <div>
                                  <h5>Acceptance Criteria</h5>
                                  ${renderList(task.acceptance_criteria)}
                                </div>
                                <div>
                                  <h5>Verification</h5>
                                  ${renderList(task.verification)}
                                </div>
                              </div>
                            </div>
                          `,
                        )
                        .join("")}
                    </div>
                  </article>
                `,
              )
              .join("")}
          </div>
        </section>

        <section class="card">
          <h2>Prompt Verification Requirements</h2>
          ${renderCardGrid(promptCards.join(""), "two-up")}
        </section>

        <section class="card">
          <h2>Slot Verification Requirements</h2>
          ${renderCardGrid(slotCards.join(""), "three-up")}
        </section>
      </div>
    `;
  },
});

function groupTaskVerification(tasks) {
  const groups = new Map();

  for (const task of tasks) {
    if (!groups.has(task.repo_target)) {
      groups.set(task.repo_target, []);
    }
    groups.get(task.repo_target).push(task);
  }

  return Array.from(groups.entries());
}
