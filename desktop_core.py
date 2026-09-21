"""PC 앱에서 사용하는 경로 검증과 샘플 준비. 코랩 경로로 바꾸지 않는다."""
import os
import shutil
import sys
from pathlib import Path


def local_path(value):
    value = value.strip().strip('"\'“”‘’').strip()
    if not value:
        raise ValueError("폴더 경로를 입력하거나 [찾아보기]로 선택해주세요.")
    if value.startswith(("http://", "https://", "/content/")):
        raise ValueError("PC 폴더 경로를 넣어주세요. 예: G:\\내 드라이브\\자료\n구글 공유 링크·코랩 경로는 PC에서 열 수 없습니다.")
    path = Path(os.path.expandvars(value)).expanduser()
    if not path.is_absolute():
        raise ValueError("전체 경로를 입력해주세요. [찾아보기]로 선택하면 정확합니다.")
    return path.resolve()


def validate_folders(source, output):
    src, dst = local_path(source), local_path(output)
    if not src.is_dir():
        raise ValueError(f"원본 폴더를 찾을 수 없습니다.\n{src}\n탐색기에서 이 폴더가 열리는지 확인해주세요.")
    if dst.exists() and not dst.is_dir():
        raise ValueError("결과 경로에 같은 이름의 파일이 있습니다. 다른 폴더를 선택해주세요.")
    if src == dst or dst in src.parents:
        raise ValueError("결과 폴더는 원본과 다른 폴더로 지정해주세요.\n원본의 상위 폴더도 결과 위치로 사용할 수 없습니다.")
    return src, dst


def resource_root():
    return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))


def prepare_sample(destination):
    root = Path(destination)
    source = root / "원본"
    source.mkdir(parents=True, exist_ok=True)
    name = "대한민국_태극기와_애국가.pdf"
    target = source / name
    original = resource_root() / "output" / "pdf" / name
    if not target.exists():
        shutil.copy2(original, target)
    return source, root / "변환결과"
