import unittest

from engiverify.ocr.tesseract_cli import parse_tesseract_tsv

class TesseractTsvTests(unittest.TestCase):
    def test_words_group_into_lines_with_confidence_and_bbox(self):
        tsv = (
            "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n"
            "5\t1\t1\t1\t1\t1\t10\t20\t30\t10\t90\tPAGA\n"
            "5\t1\t1\t1\t1\t2\t45\t20\t40\t10\t80\tshall\n"
            "5\t1\t1\t1\t2\t1\t10\t40\t50\t10\t70\tprovide\n"
        )
        lines = parse_tesseract_tsv(tsv)
        self.assertEqual(len(lines),2)
        self.assertEqual(lines[0]["text"],"PAGA shall")
        self.assertEqual(lines[0]["bbox_px"],[10,20,85,30])
        self.assertAlmostEqual(lines[0]["confidence"],0.85)
        self.assertEqual(lines[1]["text"],"provide")

if __name__=="__main__":
    unittest.main()
