import unittest
from unittest.mock import patch, MagicMock
import dependency_visualizer

class TestDependencyVisualizer(unittest.TestCase):
    
    @patch('dependency_visualizer.subprocess.run')
    def test_get_dependencies(self, mock_run):
        mock_run.return_value = MagicMock(stdout='Depends: dep1\nDepends: dep2\n')
        dependencies = dependency_visualizer.get_dependencies('testpkg', 0, 1, set())
        self.assertEqual(dependencies, ['dep1', 'dep2'])
    
    def test_generate_graph(self):
        dependencies = ['dep1', 'dep2']
        dot = dependency_visualizer.generate_graph('testpkg', dependencies)
        self.assertIn('testpkg', dot.source)
        self.assertIn('dep1', dot.source)
        self.assertIn('dep2', dot.source)
        self.assertIn('testpkg -> dep1', dot.source)
        self.assertIn('testpkg -> dep2', dot.source)

if __name__ == '__main__':
    unittest.main()