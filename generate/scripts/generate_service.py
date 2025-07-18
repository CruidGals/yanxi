import yaml
from pathlib import Path
import argparse
from collections import defaultdict

service_template = '''
<div class="service-list">
    {service}
</div>
'''

def generate_service_block(year_map, data):
    """
    Generates the service blocks and categorizes them by year in year_map
    """

    # Parse the links first
    if 'links' in data:
        links_html = "".join([f'''<a class="pe-3" href="{link['url']}">{link['type']}</a>''' for link in data['links']])
    else:
        links_html = ""

    # Metadata HTML, if applicable
    metadata_list = []

    if 'location' in data:
        metadata_list.append(data['location'])
    if 'date' in data:
        metadata_list.append(data['date'])

    metadata_html = f'''<div class="block-metadata">{', '.join(metadata_list)}</div>''' if metadata_list else ""
    service_html = f'''<li class="pb-1">
                    <div class="block-title">{data['title']}</div>
                    {metadata_html}
                    {f'<div class="block-other">{data["desc"]}</div>' if data.get('desc') else ""}
                    {links_html}
            </li>
    '''

    year_map[data['year']].append(service_html)

def generate_service_grouped(year_map):
    """
    Formally puts the service blocks into a format categorized by the year
    """

    # Sort the keys in decreasing fashion
    sorted_keys = sorted(year_map.keys(), reverse=True)
    service_groups = []

    for key in sorted_keys:
        service_blocks_html = "".join(year_map[key])
        service_group = f'''<h3 class="section-year">{key}</h3>
        <div class="px-5"><ul>
            {service_blocks_html}
        </ul></div>
        '''

        service_groups.append(service_group)

    return service_groups


def generate_service_html(yaml_path, output_path=""):
    # Load the yaml file to read
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Parse service data into html (sorted by year)
    service_blocks = defaultdict(list)
    for service_data in data.get('service', []):
        generate_service_block(service_blocks, service_data)

    service_groups_html = "".join(generate_service_grouped(service_blocks))
    service_html = service_template.format(service=service_groups_html)
    
    if output_path != "":
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(service_html)

    return service_html

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate service list using YAML files.")
    parser.add_argument("--yaml_path", default="generate/yaml/service.yaml", type=str, help="Path to YAML file.")
    parser.add_argument("--output_path", default="generate/output/service.html", type=str, help="Path to the output file.")
    args = parser.parse_args()

    generate_service_html(args.yaml_path, args.output_path)