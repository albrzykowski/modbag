import os
import argparse
import json
from jinja2 import Environment, FileSystemLoader

def generate_file(template_path, output_path, context):
    # Load the template directory and template file name
    template_dir = os.path.dirname(template_path)
    template_file = os.path.basename(template_path)

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    # Render the template with context
    rendered_content = template.render(context)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write the rendered content to the output file
    with open(output_path, "w") as f:
        f.write(rendered_content)
    print(f"Generated file at: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Template-based file generator")
    parser.add_argument('--template', required=True, help='Path to the template file, relative to project root')
    parser.add_argument('--output', required=True, help='Path to save the generated file')
    parser.add_argument('--context', required=False, default='{}',
                        help='JSON string with context for template rendering, e.g. \'{"name": "value"}\'')
    args = parser.parse_args()

    # Calculate project root as one directory above this script
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Construct absolute paths
    template_path = os.path.abspath(os.path.join(project_root, args.template))
    output_path = os.path.abspath(os.path.join(project_root, args.output))

    if not os.path.exists(template_path):
        print(f"Template file does not exist: {template_path}")
        return

    try:
        context = json.loads(args.context)
    except json.JSONDecodeError:
        print("Invalid JSON string for context")
        return

    generate_file(template_path, output_path, context)

if __name__ == "__main__":
    main()