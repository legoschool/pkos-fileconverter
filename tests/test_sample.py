import base64
import ast
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

class SampleTests(unittest.TestCase):
    def test_embedded_sample_cell_converts_and_reruns(self):
        nb = json.loads((ROOT / "PKOS_변환기.ipynb").read_text(encoding="utf-8"))
        src = next("".join(c["source"]) for c in nb["cells"] if "".join(c["source"]).startswith("#@title ▶ 샘플 PDF로 변환 테스트"))
        displays = []
        display_module = types.ModuleType("IPython.display")
        display_module.display = displays.append
        display_module.Markdown = lambda value: value
        with tempfile.TemporaryDirectory() as temp, patch.dict(sys.modules, {"IPython": types.ModuleType("IPython"), "IPython.display": display_module}):
            tree = ast.parse(src)
            class LocalRoot(ast.NodeTransformer):
                def visit_Constant(self, node):
                    if node.value == "/content/PKOS_샘플":
                        return ast.copy_location(ast.Constant(temp), node)
                    return node
            code = compile(ast.fix_missing_locations(LocalRoot().visit(tree)), "sample-cell", "exec")
            scope = {}
            for _ in range(2):
                exec(code, scope)
                self.assertEqual(len(scope["sample_fc"].records), 1)
                self.assertFalse(scope["sample_fc"].errors)
                self.assertEqual(scope["sample_pdf"].read_bytes(), (ROOT / "output/pdf/대한민국_태극기와_애국가.pdf").read_bytes())
                for lyric in ("동해물과 백두산이", "남산 위에 저 소나무", "가을 하늘 공활한데", "이 기상과 이 맘으로", "무궁화 삼천리 화려강산"):
                    self.assertIn(lyric, displays[-1])
                self.assertTrue((scope["sample_out"] / "INDEX.md").exists())

if __name__ == "__main__":
    unittest.main()
