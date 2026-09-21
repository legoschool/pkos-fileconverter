import ast
import base64
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pkos_paths import drive_path


class DrivePathTests(unittest.TestCase):
    def test_copied_paths(self):
        suffix = '00_개인지식운영체계(PKOS)/01_외부 정보'
        expected = '/content/drive/MyDrive/' + suffix
        for value in (suffix, expected, '"G:\\내 드라이브\\' + suffix.replace('/', '\\') + '"', '“' + expected + '”'):
            with self.subTest(value=value):
                self.assertEqual(drive_path(value), expected)

    def test_invalid_inputs(self):
        for value in ('', 'https://drive.google.com/drive/folders/123', '../../outside', 'C:/Users/data', '/tmp/data'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                drive_path(value)

    def test_notebook_engines_and_syntax(self):
        for p in ROOT.glob('*.py'):
            ast.parse(p.read_text(encoding='utf-8'))
        nb = json.loads((ROOT / 'PKOS_변환기.ipynb').read_text(encoding='utf-8'))
        found = False
        for cell in nb['cells']:
            if cell['cell_type'] != 'code':
                continue
            tree = ast.parse(''.join(cell['source']))
            for node in tree.body:
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '_ENGINES' for t in node.targets):
                    found = True
                    for name, data in ast.literal_eval(node.value).items():
                        self.assertEqual(base64.b64decode(data).decode('utf-8'), (ROOT / name).read_text(encoding='utf-8'))
        self.assertTrue(found)


if __name__ == '__main__':
    unittest.main()
