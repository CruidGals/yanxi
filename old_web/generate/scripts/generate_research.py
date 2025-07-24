import yaml
from pathlib import Path
import argparse
from collections import defaultdict

research_template = '''
<div class="research-list">
    {research}
</div>
'''

def generate_research_block(year_map, data):
    """
    Generates the research blocks and categorizes them by year in year_map
    """

    # Parse the links first
    if 'links' in data:
        links_html = "".join([f'''<a href="{link['url']}">{link['type']}</a>''' for link in data['links']])
    else:
        links_html = ""

    # Every research paper requires title, authors, publishers, and years
    research_html = f'''<div class="block">
                <div class="block-title">{data['title']}</div>
                <div class="block-contributors">{data['authors']}</div>
                <div class="block-other">{data['publisher']}, {data['year']}</div>
                {links_html}
            </div>
    '''

    year_map[data['year']].append(research_html)

def generate_research_grouped(year_map):
    """
    Formally puts the research blocks into a format categorized by the year
    """

    # Sort the keys in decreasing fashion
    sorted_keys = sorted(year_map.keys(), reverse=True)
    research_groups = []

    for key in sorted_keys:
        research_blocks_html = "".join(year_map[key])
        research_group = f'''<h3 class="section-year">{key}</h3>
        <div class="section-group">
            {research_blocks_html}
        </div>
        '''

        research_groups.append(research_group)

    return research_groups


def generate_research_html(yaml_path, output_path=""):
    # Load the yaml file to read
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Parse research data into html (sorted by year)
    research_blocks = defaultdict(list)
    for research_data in data.get('research', []):
        generate_research_block(research_blocks, research_data)

    research_groups_html = "".join(generate_research_grouped(research_blocks))
    research_html = research_template.format(research=research_groups_html)
    
    if output_path != "":
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(research_html)

    return research_html

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate research list using YAML files.")
    parser.add_argument("--yaml_path", default="generate/yaml/research.yaml", type=str, help="Path to YAML file.")
    parser.add_argument("--output_path", default="generate/output/research.html", type=str, help="Path to the output file.")
    args = parser.parse_args()

    generate_research_html(args.yaml_path, args.output_path)