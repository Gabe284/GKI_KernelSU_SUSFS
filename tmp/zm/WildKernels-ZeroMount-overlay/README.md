# WildKernels Android 13–5.15 ZeroMount build overlay

This overlay adds the supplied enhanced SUSFS, ZeroMount VFS, and WKSU safety patches to the WildKernels `GKI_KernelSU_SUSFS` GitHub Actions build.

## Target

- Android 13 GKI
- Linux 5.15 LTS
- KernelSU/Wild KSU + SUSFS already applied by the upstream workflow
- `CONFIG_ZEROMOUNT=y`

## Apply to a fork

1. Fork `WildKernels/GKI_KernelSU_SUSFS` on GitHub.
2. Clone your fork on Linux, macOS, or Termux with Git installed.
3. Extract this ZIP next to the cloned repository.
4. Run:

```sh
./WildKernels-ZeroMount-overlay/install-overlay.sh /path/to/GKI_KernelSU_SUSFS
cd /path/to/GKI_KernelSU_SUSFS
git add .github/actions/zeromount .github/workflows/build.yml patches/zeromount
git commit -m "Add ZeroMount VFS to Android 13 GKI 5.15"
git push
```

5. Open the fork's **Actions** tab and enable workflows when prompted.
6. Run the repository's normal build workflow for **android13-5.15**, sublevel **207**, LTS, with KernelSU-Next and SUSFS enabled.
7. Download the `AnyKernel3` artifact after the job succeeds.

## Patch order

The custom action runs after the upstream SUSFS action:

1. `51_enhanced_susfs-android13-5.15.patch`
2. `60_zeromount-android13-5.15.patch`
3. `70_ksu_safety-wksu-5.15.patch`

The job deliberately stops on a rejected hunk. Rejects are copied into the upstream `patch-rejects` artifact rather than continuing to compile an unsafe partial patch.

## Important

Do not flash an artifact unless the build completes without patch rejects and the resulting configuration contains `CONFIG_ZEROMOUNT=y`. Keep the original working AnyKernel ZIP and boot image available for recovery.
