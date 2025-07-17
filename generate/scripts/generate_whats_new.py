import yaml
from pathlib import Path
import argparse
from collections import defaultdict

whats_new_template = '''
<div class="whats_new-list">
    {whats_new}
</div>
'''

def generate_whats_new_block(year_map, data):
    """
    Generates the whats_new blocks and categorizes them by year in year_map
    """

    # Parse the links first
    if 'links' in data:
        links_html = "".join([f'''<a class="pe-3" href="{link['url']}">{link['type']}</a>''' for link in data['links']])
    else:
        links_html = ""

    # Create the image html seperately
    if 'image' in data:
        image_html = f'''<a href="{data["image"]}" class="glightbox col-12 col-md-4" data-gallery="whats-new-gallery">
            <img src="{data["image"]}" class="whats-new-image p-3 rounded-5" alt="{data["image_alt"] if data.get("image_alt") else "What's New Image"}">
        </a>'''
    else:
        image_html = ""

    whats_new_html = f'''<li class="pb-1 container"><div class="row">
                    <div class="col-12 {"col-md-8" if image_html else ""}">
                        <div class="block-title">{data['title']}</div>
                        {f'<div class="block-other">{data["desc"]}</div>' if data.get('desc') else ""}
                        {links_html}
                    </div>
                    {image_html}
            </div></li>
    '''

    year_map[data['year']].append(whats_new_html)

def generate_whats_new_grouped(year_map):
    """
    Formally puts the whats_new blocks into a format categorized by the year
    """

    # Sort the keys in decreasing fashion
    sorted_keys = sorted(year_map.keys(), reverse=True)
    whats_new_groups = []

    for key in sorted_keys:
        whats_new_blocks_html = "".join(year_map[key])
        whats_new_group = f'''<h3 class="section-year">{key}</h3>
        <div class="px-5"><ul>
            {whats_new_blocks_html}
        </ul></div>
        '''

        whats_new_groups.append(whats_new_group)

    return whats_new_groups


def generate_whats_new_html(yaml_path, output_path):
    # Load the yaml file to read
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Parse whats_new data into html (sorted by year)
    whats_new_blocks = defaultdict(list)
    for whats_new_data in data.get('whats_new', []):
        generate_whats_new_block(whats_new_blocks, whats_new_data)

    whats_new_groups_html = "".join(generate_whats_new_grouped(whats_new_blocks))
    whats_new_html = whats_new_template.format(whats_new=whats_new_groups_html)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(whats_new_html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate whats_new list using YAML files.")
    parser.add_argument("--yaml_path", default="generate/yaml/whats_new.yaml", type=str, help="Path to YAML file.")
    parser.add_argument("--output_path", default="generate/output/whats_new.html", type=str, help="Path to the output file.")
    args = parser.parse_args()

    generate_whats_new_html(args.yaml_path, args.output_path)