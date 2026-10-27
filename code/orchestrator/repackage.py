"""Build a source archive without local environments, caches, or credentials."""
import tarfile
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
EXCLUDE_DIRS={".venv","__pycache__",".cache",".git","node_modules",".pytest_cache"}
EXCLUDE_FILES={".env"}

def walk_with_excludes(root):
    root=Path(root)
    for path in sorted(root.rglob("*")):
        if not path.is_file(): continue
        # Exclude only directories *inside* the packaged tree. The caller's
        # workspace itself may live under a .cache test directory.
        if any(part in EXCLUDE_DIRS for part in path.relative_to(root).parts[:-1]): continue
        if path.name in EXCLUDE_FILES or path.suffix==".pyc" or path.name.startswith(".env."): continue
        yield path

def repackage(repo_root=ROOT):
    repo_root=Path(repo_root); files=list(walk_with_excludes(repo_root/"code"))
    files += [p for p in (repo_root/"README.md",repo_root/"tradeoff.md",repo_root/"worklog.md",
                          repo_root/"requirements.txt") if p.exists()]
    zip_path=repo_root/"code.zip"; tmp=repo_root/"code.zip.tmp"
    try:
        with zipfile.ZipFile(tmp,"w",zipfile.ZIP_DEFLATED) as archive:
            for path in files: archive.write(path,path.relative_to(repo_root))
            # The runnable checkout keeps code/ on PYTHONPATH, while the brief
            # requires evaluation/... at ZIP root. Include portable aliases.
            evaluation_root=repo_root/"code/evaluation"
            for path in walk_with_excludes(evaluation_root):
                archive.write(path,Path("evaluation")/path.relative_to(evaluation_root))
        tmp.replace(zip_path)
        return zip_path,len(files),None
    except (OSError,zipfile.BadZipFile) as exc:
        if tmp.exists(): tmp.unlink()
        out=repo_root/"code.tar.gz"
        with tarfile.open(out,"w:gz") as archive:
            for path in files: archive.add(path,arcname=path.relative_to(repo_root))
            evaluation_root=repo_root/"code/evaluation"
            for path in walk_with_excludes(evaluation_root):
                archive.add(path,arcname=Path("evaluation")/path.relative_to(evaluation_root))
        return out,len(files),str(exc)

if __name__=="__main__":
    path,count,error=repackage(); print(f"Wrote {path} with {count} files"+(f"; ZIP failed: {error}" if error else ""))
