param()

$ErrorActionPreference = 'Continue'

if ($env:KLM_SKIP_LCI_REFRESH -and $env:KLM_SKIP_LCI_REFRESH.Trim() -ne '') {
  Write-Host "[post-commit] KLM_SKIP_LCI_REFRESH set; skipping LCI refresh."
  exit 0
}

function Invoke-Safe {
  param(
    [Parameter(Mandatory=$true)][string]$Command
  )

  try {
    Write-Host "[post-commit] $Command"
    iex $Command
  } catch {
    Write-Host "[post-commit] WARNING: command failed: $Command"
  }
}

Invoke-Safe "npx lci status"
Invoke-Safe "npx lci list"
