param(
    [string]$PlanningRun = "planning_runs\coc-base-builder-v1",
    [switch]$SkipPlanningRun
)

$ErrorActionPreference = "Stop"

Write-Host "== AI Assembly Line: sync and check =="

Write-Host "`n== Current branch =="
git branch --show-current

Write-Host "`n== Current HEAD before pull =="
git log --oneline -1

$Before = git rev-parse HEAD

Write-Host "`n== Pulling latest =="
git pull --ff-only

$After = git rev-parse HEAD

Write-Host "`n== Current HEAD after pull =="
git log --oneline -1

if ($Before -ne $After) {
    Write-Host "`n== Changed commits =="
    git log --oneline "$Before..$After"

    Write-Host "`n== Changed files =="
    git diff --name-status "$Before..$After"
} else {
    Write-Host "`n== No new commits pulled =="
}

Write-Host "`n== Validate seed =="
python tools\validate_seed.py

Write-Host "`n== Rebuild context pack =="
python tools\build_context_pack.py

Write-Host "`n== Validate seed after context rebuild =="
python tools\validate_seed.py

Write-Host "`n== JavaScript syntax checks =="
Get-ChildItem web -Filter *.js | Sort-Object Name | ForEach-Object {
    Write-Host (">>> node --check " + $_.Name)
    node --check $_.FullName
}

if (-not $SkipPlanningRun) {
    Write-Host "`n== Validate planning run: $PlanningRun =="
    python tools\validate_planning_run.py $PlanningRun
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Planning run validation returned nonzero. This may be expected if outputs are intentionally missing."
    }
}

Write-Host "`n== Git status =="
git status --short

Write-Host "`n== Done =="
