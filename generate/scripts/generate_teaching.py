import yaml
from pathlib import Path
import argparse
from collections import defaultdict

teaching_template = '''
<div class="teaching-list">
    {teaching}
</div>
'''

def generate_teaching_block(year_map, data):
    """
    Generates the teaching blocks and categorizes them by year in year_map
    """

    # Parse the links first
    if 'links' in data:
        links_html = "".join([f'''<a href="{link['url']}">{link['type']}</a>''' for link in data['links']])
    else:
        links_html = ""

    # Every teaching paper requires title, course code, and year. Semester is optioanl
    semester_str = f"{data['semester']} " if data.get('semester') else ""
    teaching_html = f'''<div class="block">
                <div class="block-title">{data['title']}</div>
                <div class="teaching-course-code">{data['course-code']}, {semester_str}{data['year']}</div>
                {links_html}
            </div>
    '''

    year_map[data['year']].append(teaching_html)

def generate_teaching_grouped(year_map):
    """
    Formally puts the teaching blocks into a format categorized by the year
    """

    # Sort the keys in decreasing fashion
    sorted_keys = sorted(year_map.keys(), reverse=True)
    teaching_groups = []

    for key in sorted_keys:
        teaching_blocks_html = "".join(year_map[key])
        teaching_group = f'''<h3 class="section-year">{key}</h3>
        <div class="section-group">
            {teaching_blocks_html}
        </div>
        '''

        teaching_groups.append(teaching_group)

    return teaching_groups


def generate_teaching_html(yaml_path, output_path):
    # Load the yaml file to read
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Parse teaching data into html (sorted by year)
    teaching_blocks = defaultdict(list)
    for teaching_data in data.get('teaching', []):
        generate_teaching_block(teaching_blocks, teaching_data)

    teaching_groups_html = "".join(generate_teaching_grouped(teaching_blocks))
    teaching_html = teaching_template.format(teaching=teaching_groups_html)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(teaching_html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate teaching list using YAML files.")
    parser.add_argument("--yaml_path", default="generate/yaml/teaching.yaml", type=str, help="Path to YAML file.")
    parser.add_argument("--output_path", default="generate/output/teaching.html", type=str, help="Path to the output file.")
    args = parser.parse_args()

    generate_teaching_html(args.yaml_path, args.output_path)