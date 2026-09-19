# Local publication preparation

The maintained tree contains research code, narrative, executed study, generated aggregate
results and original figures. Original notebooks, helper code and data are recoverable from
`old` and ignored `research/private-legacy/`; these historical copies are not release-cleared.
The user authorized upload to the existing GitHub repository. The maintained work is on
`renovation`, with original research on `old`; no history rewrite, default-branch replacement,
visibility change or live blog publication is part of this update.

## Current-file review

Run `uv run python research/check_artifacts.py --public` to check maintained links, notebook
outputs and blocked data paths. Full `uv run python research/check_artifacts.py` additionally
verifies provenance and independently reconstructs consequential saved numerical results.
Review `git diff --stat old` and explicit files; avoid printing full historical diffs that may
contain old credential values. The audit records credential findings by category/path only.

Raw vendor snapshots and private legacy data are excluded by `.gitignore`; no unrestricted
data redistribution or commercial-use rights are asserted. Reproduction requires permitted
access to the pinned cache; a later vendor download may differ and must not silently replace
it. The twelve topic notebooks use original constructed examples with declared assumptions.
Keep original attribution in `NOTICE` and the source register. No blanket license is inferred.

## History and release boundary

A clean maintained branch does not clean the `old` branch, earlier commits, remote copies or
local archives. The original Asset Allocation engine contains a credential-like default:
owner review of rotation and historical copies is still needed. Do not publish recovery
folders or use the embedded credential. Other projects' historical vendor inputs also require
rights review. These statements describe actual inspected legacy material, not a secret audit
of every historical object.

CI installs the locked Linux environment, runs focused synthetic/known-answer tests and public
artifact checks. It does not download licensed histories, certify provider data quality or
validate live execution. Complete reproduction commands are on the secondary
[reproduction page](docs/reproduction.md). Codex and agent instructions, environments, private
recovery material and vendor snapshots remain excluded from the maintained public files.
