#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="${1:-.}"
cd "$REPO_ROOT"
[[ -f .github/workflows/build.yml ]] || { echo 'Run this from the root of a WildKernels/GKI_KernelSU_SUSFS fork.' >&2; exit 1; }
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -a "$SCRIPT_DIR/.github/actions/zeromount" .github/actions/
mkdir -p patches/zeromount
cp -a "$SCRIPT_DIR/patches/zeromount/." patches/zeromount/
python3 - .github/workflows/build.yml <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
if 'uses: ./.github/actions/zeromount' in s:
    print('ZeroMount workflow step is already installed')
    raise SystemExit(0)
needle="""    - name: Baseband Guard
      if: (contains(inputs.feature_set, 'BBG') || inputs.feature_set == 'FULL')
"""
insert="""    - name: Apply ZeroMount VFS patch set
      if: inputs.version == 'android13-5.15'
      uses: ./.github/actions/zeromount
      with:
        version: ${{ inputs.version }}
        kernel_version: ${{ inputs.kernel_version }}
        android_version: ${{ inputs.android_version }}

"""
if needle not in s:
    raise SystemExit('Could not locate the Baseband Guard insertion point; upstream workflow changed.')
p.write_text(s.replace(needle, insert+needle, 1))
PY
printf '\nInstalled ZeroMount overlay. Commit and push these files:\n'
git status --short 2>/dev/null || true
