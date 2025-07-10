import yaml
from pathlib import Path
import argparse

research_template = '''
<div class="research-list">
    {research}
</div>
'''

def generate_research_block(data):
    # Parse the links first
    if 'links' in data:
        links_html = "".join([f'''<a href="{link['url']}">{link['type']}</a>''' for link in data['links']])

    # Every research paper requires title, authors, publishers, and years
    research_html = f'''<div class="research m-3">
        <div class="research-title">{data['title']}</div>
        <div class="research-contributors">{data['authors']}</div>
        <div class="research-other">{data['publisher']}, {data['year']}</div>
        {links_html}
    </div>
    '''

    return research_html

def generate_research_html(yaml_path, output_path):
    # Load the yaml file to read
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Parse research data into html
    research_blocks = []
    for research_data in data.get('research', []):
        research_blocks.append(generate_research_block(research_data))

    research_blocks_html = "".join(research_blocks)
    research_html = research_template.format(research=research_blocks_html)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(research_html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate research list using YAML files.")
    parser.add_argument("--yaml_path", default="generate/yaml/research.yaml", type=str, help="Path to YAML file.")
    parser.add_argument("--output_path", default="generate/output/research.html", type=str, help="Path to the output file.")
    args = parser.parse_args()

    generate_research_html(args.yaml_path, args.output_path)