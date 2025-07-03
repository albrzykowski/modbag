import unittest
from unittest.mock import patch, mock_open
from modbag.generator import generate_file  # podmień na faktyczną nazwę modułu

class TestGenerateFile(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    @patch("jinja2.Environment.get_template")
    def test_generate_file(self, mock_get_template, mock_makedirs, mock_file):
        # Prepare mock template
        mock_template = mock_get_template.return_value
        mock_template.render.return_value = "rendered content"

        # Call the function
        generate_file("some/path/template.j2", "output/path/result.txt", {"key": "value"})

        # Check if makedirs was called to ensure output directory exists
        mock_makedirs.assert_called_once_with("output/path", exist_ok=True)

        # Check if template.render was called with correct context
        mock_template.render.assert_called_once_with({"key": "value"})

        # Check if open was called to write the rendered content
        mock_file.assert_called_once_with("output/path/result.txt", "w")
        mock_file().write.assert_called_once_with("rendered content")

if __name__ == "__main__":
    unittest.main()
