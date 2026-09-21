"""Windows EXE 제작: python -m pip install pyinstaller 후 실행."""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile", "--windowed",
        "--name", "PKOS", "--distpath", str(ROOT / "dist"),
        "--workpath", str(Path(tempfile.gettempdir()) / "pkos-pyinstaller-build"),
        "--specpath", str(ROOT),
        "--add-data", str(ROOT / "output/pdf/대한민국_태극기와_애국가.pdf") + ";output/pdf",
        str(ROOT / "pkos_app.py")], cwd=ROOT, check=True)
