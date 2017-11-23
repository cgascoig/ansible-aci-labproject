import unittest
# import imp
#
# aci_model=imp.load_source("acimodel", "./aci_model")

import aci_utils

class TestInterfaceParsing(unittest.TestCase):

    def test_valid_interfaces(self):
        tests = [
            ('leaf-111/eth1/5', 'topology/pod-1/paths-111/pathep-[eth1/5]'),
            ('leaf-111/eth1/6', 'topology/pod-1/paths-111/pathep-[eth1/6]'),
            ('leaf-222/eth1/6', 'topology/pod-1/paths-222/pathep-[eth1/6]'),
            ('leaf-2222/eth1/6', 'topology/pod-1/paths-2222/pathep-[eth1/6]'),
            ('leaf-222/eth1/46', 'topology/pod-1/paths-222/pathep-[eth1/46]'),
            ('leaf-111/e1/5', 'topology/pod-1/paths-111/pathep-[eth1/5]'),
            ('leaf-111/eth1/5', 'topology/pod-1/paths-111/pathep-[eth1/5]'),
            ('leaf-111/eth101/1/5', 'topology/pod-1/paths-111/extpaths-101/pathep-[eth1/5]'),
            ('leaf-111/eth102/1/5', 'topology/pod-1/paths-111/extpaths-102/pathep-[eth1/5]'),
            ('pod-1/leaf-111/eth1/6', 'topology/pod-1/paths-111/pathep-[eth1/6]'),
            ('pod-2/leaf-111/eth1/6', 'topology/pod-2/paths-111/pathep-[eth1/6]'),
        ]
        for test in tests:
            simple, canonical = test
            self.assertEqual(aci_utils.parse_interface(simple), canonical)
            
if __name__ == '__main__':
    unittest.main()