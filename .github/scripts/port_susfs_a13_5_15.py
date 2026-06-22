#!/usr/bin/env python3
from pathlib import Path


def insert_after(path: str, anchor: str, block: str, sentinel: str) -> None:
    file = Path(path)
    text = file.read_text()

    if sentinel in text:
        print(f"{path}: already contains {sentinel}")
        return

    if anchor not in text:
        raise SystemExit(f"ERROR: anchor not found in {path}: {anchor}")

    file.write_text(text.replace(anchor, f"{anchor}\n{block}", 1))
    print(f"{path}: inserted {sentinel}")


insert_after(
    "fs/namespace.c",
    "#include <linux/mnt_idmapping.h>",
    "#ifdef CONFIG_KSU_SUSFS_SUS_MOUNT\n"
    "#include <linux/susfs_def.h>\n"
    "#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MOUNT",
    "#include <linux/susfs_def.h>",
)

insert_after(
    "fs/namespace.c",
    '#include "internal.h"',
    "#ifdef CONFIG_KSU_SUSFS_SUS_MOUNT\n"
    "extern bool susfs_is_current_ksu_domain(void);\n"
    "extern struct static_key_true susfs_is_sdcard_android_data_not_decrypted;\n\n"
    "#define CL_COPY_MNT_NS BIT(25) /* used by copy_mnt_ns() */\n\n"
    "#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MOUNT",
    "#define CL_COPY_MNT_NS BIT(25)",
)

insert_after(
    "fs/proc/task_mmu.c",
    "#include <linux/pkeys.h>",
    "#if defined(CONFIG_KSU_SUSFS_SUS_KSTAT) || defined(CONFIG_KSU_SUSFS_SUS_MAP) || defined(CONFIG_KSU_SUSFS_OPEN_REDIRECT)\n"
    "#include <linux/susfs_def.h>\n"
    "#endif // #if defined(CONFIG_KSU_SUSFS_SUS_KSTAT) || defined(CONFIG_KSU_SUSFS_SUS_MAP) || defined(CONFIG_KSU_SUSFS_OPEN_REDIRECT)",
    "#include <linux/susfs_def.h>",
)
