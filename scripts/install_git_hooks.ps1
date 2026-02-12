param()

$ErrorActionPreference = 'Stop'

$repoRoot = (git rev-parse --show-toplevel).Trim()
if (-not $repoRoot) {
  throw "Not inside a git repository."
}

$source = Join-Path $repoRoot "scripts/git-hooks/post-commit"
$hooksDir = Join-Path $repoRoot ".git/hooks"
$target = Join-Path $hooksDir "post-commit"

if (-not (Test-Path $hooksDir)) {
  throw "Hooks directory not found: $hooksDir"
}

Copy-Item -Force $source $target
Write-Host "Installed git hook: $target"
Write-Host "Post-commit LCI refresh enabled (set KLM_SKIP_LCI_REFRESH=1 to skip)."
