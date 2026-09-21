"""코랩 및 Windows Google Drive 경로를 내 드라이브 경로로 정규화한다."""
import posixpath
import re

MYDRIVE = "/content/drive/MyDrive"


def drive_path(value: str) -> str:
    text = (value or "").strip().strip('"\'“”‘’').strip().replace("\\", "/")
    if not text:
        raise ValueError("폴더 경로를 입력해주세요. 코랩에서 '경로 복사'한 값을 붙여넣으세요.")
    if re.match(r"https?://", text):
        raise ValueError("이 칸은 폴더 링크나 ID가 아닌 경로를 받습니다. 왼쪽 파일 탐색기에서 폴더의 '경로 복사'를 사용하세요.")
    windows = re.match(r"^[A-Za-z]:/(?:내 드라이브|My Drive|MyDrive)(?:/|$)", text)
    if windows:
        text = text[windows.end():]
    elif re.match(r"^[A-Za-z]:", text):
        raise ValueError("내 드라이브 경로만 지원합니다. 코랩에서 폴더의 경로를 복사해주세요.")
    elif text == MYDRIVE or text.startswith(MYDRIVE + "/"):
        text = text[len(MYDRIVE):].lstrip("/")
    elif text.startswith("/"):
        raise ValueError("/content/drive/MyDrive 안의 경로를 입력해주세요.")
    result = posixpath.normpath(posixpath.join(MYDRIVE, text))
    if result != MYDRIVE and not result.startswith(MYDRIVE + "/"):
        raise ValueError("내 드라이브 바깥의 경로는 사용할 수 없습니다.")
    return result
