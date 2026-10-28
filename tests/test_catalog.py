import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('catalog', Path(__file__).resolve().parents[1] / 'catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)

class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_library = catalog.LIBRARY
        catalog.LIBRARY = Path(self.temp.name)
        (catalog.LIBRARY / 'data').mkdir()
        (catalog.LIBRARY / 'img').mkdir()
        (catalog.LIBRARY / 'thumbs').mkdir()
        row = {'id': 'test_front', '原图': 'img/test_front.png', '缩略图': 'thumbs/test_front.jpg'}
        (catalog.LIBRARY / 'data/pose-zh.json').write_text(json.dumps([row]))
        (catalog.LIBRARY / row['原图']).write_bytes(b'fixture')
        catalog.records.cache_clear(); catalog.index.cache_clear()

    def tearDown(self):
        catalog.LIBRARY = self.old_library
        catalog.records.cache_clear(); catalog.index.cache_clear()
        self.temp.cleanup()

    def test_selected_id_maps_to_allowlisted_file(self):
        self.assertEqual(catalog.asset('img', 'test_front.png').read_bytes(), b'fixture')

    def test_rejects_traversal_unknown_ids_and_mismatched_extension(self):
        for kind, name in [('img', '../test_front.png'), ('img', 'test_front.jpg'), ('data', 'test_front.png'), ('img', 'unknown.png'), ('img', '..\\test_front.png')]:
            with self.subTest(kind=kind, name=name), self.assertRaises(ValueError):
                catalog.asset(kind, name)

    def test_missing_image_is_actionable(self):
        with self.assertRaises(FileNotFoundError):
            catalog.asset('thumbs', 'test_front.jpg')

    def test_symlink_outside_library_is_rejected(self):
        file = catalog.LIBRARY / 'img/test_front.png'
        file.unlink(); file.symlink_to('/etc/passwd')
        with self.assertRaises(ValueError):
            catalog.asset('img', 'test_front.png')

if __name__ == '__main__': unittest.main()
