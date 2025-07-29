import yaml
from pathlib import Path
import os
import argparse

def generate_gallery(data):
    """
    Generates the body of the personal page section.
    """

    # Gallery
    type = data['type']
    media = data['media']
    image_list = []

    for image_link in media['images']:
        image_list.append(f'''<a href="{image_link['filename']}" class="glightbox" data-gallery="{type}-gallery">
            <img src="{image_link['filename']}" class="gallery-image-small" alt="{image_link['filename']}">
        </a>''')
    
    image_list_html = "\n".join(image_list)
    gallery_html = f'''<div class="gallery">
        {image_list_html}
    </div>'''

    return gallery_html

def generate_personal_html(type):
    yaml_path = f"wordpress_generators/yaml/{type}.yaml"
    output_path = f"wordpress_generators/output/{type}.html"

    # Load the yaml file to read
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Get necessary html
    gallery_html = generate_gallery(data)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(gallery_html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate research list using YAML files.")
    parser.add_argument("--type", default="tea", type=str, help="Type of personal page (choices: quote, taiji, tea)")
    args = parser.parse_args()

    types = ['quote', 'tea', 'taiji']
    personal_type = args.type.lower()

    if personal_type not in types:
        print('You have entered an invalid type. (Choices are: Quote, Tea, or Taiji)')
    else:
        generate_personal_html(personal_type)