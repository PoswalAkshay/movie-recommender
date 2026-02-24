#!/usr/bin/env pwsh
# Copies .env.example to .env if .env does not exist

$src = ".env.example"
$dest = ".env"

if (-Not (Test-Path $src)) {
    Write-Error "Missing $src"
    exit 1
}

if (Test-Path $dest) {
    Write-Host ".env already exists — no changes made."
    exit 0
}

Copy-Item $src $dest
Write-Host "Created .env from .env.example — edit .env and set TMDB_API_KEY before running."
