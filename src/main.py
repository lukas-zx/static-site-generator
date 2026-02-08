from __future__ import annotations

import os
import shutil


def clear_directory(path: str) -> None:
    """Delete all contents inside `path`, but keep the directory itself."""
    if not os.path.exists(path):
        os.makedirs(path)
        return

    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        if os.path.isfile(full_path) or os.path.islink(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)


def copy_dir_recursive(src: str, dst: str) -> None:
    """
    Recursively copy contents of src directory into dst directory.
    Assumes dst exists (create it if needed).
    Logs each file copied.
    """
    if not os.path.exists(dst):
        os.makedirs(dst)

    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)

        if os.path.isdir(src_path):
            os.makedirs(dst_path, exist_ok=True)
            copy_dir_recursive(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
            print(f"copied: {src_path} -> {dst_path}")


def copy_static_to_public(
    static_dir: str = "static", public_dir: str = "public"
) -> None:
    clear_directory(public_dir)
    copy_dir_recursive(static_dir, public_dir)


def main():
    copy_static_to_public("static", "public")


if __name__ == "__main__":
    main()
