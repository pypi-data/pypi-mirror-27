from seaborn.calling_function import *
from collections import OrderedDict
import unittest

class test_cf(unittest.TestCase):

    def test_function_defaults(self):
        ssrt = True
        answer = function_defaults(function_doc)
        for i in [1,None]:
            ssrt = ssrt and i in answer
        self.assertEquals((ssrt and len(answer) == 2),True)

    def test_function_doc(self):
        """
        tests function_doc()
        :return:
        """
        self.assertEquals(function_doc(), '\n        tests function_doc()\n        :return:\n        ')

    def test_function_path(self):
        self.assertRegexpMatches (function_path(function_doc),r'(.+/)+calling_function.py')

    def test_file_code(self):
        self.assertIn('from seaborn.calling_function import *\nfrom collections import OrderedDict\n', file_code())

    def test_function_args(self):
        self.assertTupleEqual(('function_index', 'function_name', 'frm', 'func'),function_args(function_doc))

    def test_function_info(self):
        self.assertListEqual(function_info().keys(),
                             ['line_number', 'class_name', 'basename', 'globals', 'file',
                              'path', 'locals', 'arguments', 'kwargs', 'frame', 'function_name'])

    def test_function_history(self):
        self.assertListEqual(function_history(),
                             ['function_history', 'test_function_history', 'run', '__call__', '_wrapped_run',
                              '_wrapped_run', '_wrapped_run', 'run', '__call__', 'run', 'run', 'runTests',
                              '__init__', '<module>', 'run', '<module>'])

    def test_function_linenumber(self):
        self.assertEqual(function_linenumber(),'42   ')

    def test_path(self):
        self.assertEqual(path(),'test_calling_function__test_cf__test_path')

    def test_current_folder(self):
        self.assertRegexpMatches(current_folder(),r'(.+/)+test$')

    def test_trace_error(self):
        error = trace_error()
        self.assertEqual(error[0],'51')
        self.assertIn('in test_trace_error',error[1])

if __name__ == "__main__":
    unittest.main()