import json
import sys
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from desktop_core import validate_folders, local_path, prepare_sample
from pkos_folder import FolderConverter, FolderSettings

class DesktopTests(unittest.TestCase):
    def test_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "원본"
            src.mkdir()
            out = Path(temp) / "결과"
            self.assertEqual(validate_folders('"' + str(src) + '"', str(out)), (src.resolve(), out.resolve()))
            for invalid in (src, src.parent):
                with self.assertRaises(ValueError):
                    validate_folders(str(src), str(invalid))
            for invalid in ("", "relative", "/content/drive/MyDrive", "https://drive.google.com/xxx"):
                with self.assertRaises(ValueError):
                    local_path(invalid)

    def test_output_prefix_and_cancellation(self):
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "docs-extra"
            src.mkdir()
            (src / "a.txt").write_text("테스트 문서를 마크다운으로 변환합니다.", encoding="utf-8")
            dst = Path(temp) / "docs"
            fc = FolderConverter(FolderSettings(src_dir=str(src), out_dir=str(dst), verbose=False, 개인정보_가리기=False))
            self.assertEqual(len(fc.collect()), 1)
            cancel = threading.Event()
            cancel.set()
            result = fc.run(cancel=cancel)
            self.assertTrue(result["cancelled"])
            self.assertEqual(result["done"], 0)
            cancel.clear()
            progress = []
            result = fc.run(cancel=cancel, progress=lambda *args: progress.append(args))
            self.assertEqual(result["done"], 1)
            self.assertEqual(progress[0][:2], (1, 1))

    def test_app_conversion_and_preview(self):
        from pkos_app import App
        with tempfile.TemporaryDirectory() as temp:
            src, dst = prepare_sample(Path(temp) / "sample")
            app = App()
            app.withdraw()
            app.config_path = Path(temp) / "settings.json"
            app.source.set(str(src))
            app.output.set(str(dst))
            errors = []
            try:
                with patch("pkos_app.messagebox.showerror", side_effect=lambda *a, **k: errors.append(a)):
                    app.start("sample")
                    until = time.monotonic() + 30
                    while app.busy and time.monotonic() < until:
                        app.update()
                        time.sleep(0.02)
                    app.update()
                self.assertFalse(app.busy)
                self.assertFalse(errors, errors)
                self.assertTrue(app.result_paths)
                app.preview()
                self.assertIn("동해물과 백두산이", app.preview_text.get("1.0", "end"))
                self.assertEqual(app.output_path, dst.resolve())
            finally:
                app.destroy()

if __name__ == "__main__":
    unittest.main()
