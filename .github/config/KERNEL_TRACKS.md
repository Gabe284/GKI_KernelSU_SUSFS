# Kernel build tracks

This repository now has two deliberately separate build paths.

## Android Common Kernel / GKI

The existing **Build Kernels** workflow builds Android Common Kernel (ACK/GKI) branches using the repository's Android-specific patching, KernelSU-Next, and SUSFS integration steps.

- Existing targets remain unchanged.
- Android 17 GKI uses the official dated source branch `android17-6.18-2026-09` (kernel 6.18.32).
- SUSFS is intentionally skipped for Android 17 until a compatible `gki-android17-6.18` branch and patch set are verified. The build emits a warning and is **not** a SUSFS-enabled Android 17 artifact.
- The Android 17 target is a build experiment, not a claim of device compatibility.

## Upstream Linux

Run **Actions → Upstream Linux ARM64 Build → Run workflow** to build generic ARM64 kernel artifacts from upstream kernel.org Git repositories.

- **mainline** follows Linus Torvalds' `master` branch.
- **stable** selects the newest `linux-X.Y.y` branch, or a requested series.
- **longterm** selects the newest known LTS series in the workflow's ordered candidate list, or a requested series.
- The workflow builds `Image`, modules, the resolved configuration, `System.map`, source metadata, and SHA-256 checksums.

The upstream workflow is compile-only. It does not apply KernelSU, SUSFS, Android GKI patches, vendor modules, device-specific fixes, AVB signing, or Android boot-image packaging. Its artifacts are not ready to flash to a phone.

## Compatibility and safety

Android GKI and upstream Linux are not interchangeable. Android GKI depends on Android-specific patches and a kernel module interface; a generic upstream ARM64 build does not reproduce that ABI or the device vendor's kernel modules. Successful compilation only proves that the selected source/configuration built. It does not establish bootability on any particular device.
