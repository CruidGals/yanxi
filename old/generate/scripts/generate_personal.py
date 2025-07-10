import yaml
from pathlib import Path
import os
import argparse

# HTML boilerplate to be edited
html_boilerplate = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/glightbox/dist/css/glightbox.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
    {navbar}
    {body}
    {script}
</body>
"""

# Js script
script = """<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/glightbox/dist/js/glightbox.min.js"></script>
<script>
const lightbox = GLightbox({ selector: '.glightbox' });
</script>
<script>
    const images = document.querySelectorAll('.gallery-image-small');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target); // fade in only once
        }
        });
    }, {
        threshold: 0.1
    });

    images.forEach(img => {
        observer.observe(img);
    });
</script>"""

# Sets the path of the assets folder
assets_path = "assets/images/personal"

def generate_navbar_html(data):
    """
    Generates the navbar for the page. Calculates how many pages are under the "Personal Tab," and lists them all in
    the dropdown menu.

    Args:
        data: The yaml file of the personal page. Will only access the type variable
    """

    # Navbar boilerplate html
    navbar = """<nav class="navbar fixed-top navbar-expand-md bg-dark navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="index.html">Dr. Yanxi Liu</a>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="collapsibleNavbar">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="index.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="index.html#whatsNewBlock">What's New</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="index.html#researchBlock">Research</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="index.html#teachingBlock">Teaching</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="index.html#serviceBlock">Service</a>
                    </li>
                    <li class="nav-item active dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Personal</a>
                        <ul class="dropdown-menu">
                            {dropdown_items}
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>"""
    
    dropdown_page_list = []
    curr_page_name = data.get('type', "")

    for _, dirs, __ in os.walk(assets_path):
        for dir in dirs:
            # For each asset directory, make a "dropdown page" for it
            page_name = dir.capitalize()

            if curr_page_name == page_name:
                dropdown_page_list.append(f'<li><a class="dropdown-item" href="#">{page_name}</a></li>')
            else:
                dropdown_page_list.append(f'<li><a class="dropdown-item" href="{page_name}.html">{page_name}</a></li>')
    
    navbar_html = navbar.format(dropdown_items="\n".join(dropdown_page_list))
    return navbar_html

def generate_body(data):
    """
    Generates the body of the personal page section.

    Args:
        data: The yaml file of the personal page. Requires type and media to be filled in inside the yaml file. Also requires
              that there exists the directory `assets/generate/personal/{type}`, and that the image links within the media section
              exists too.
    """

    # Title section
    title_html = f"""<div class="container-fluid bg-light">
        <div class="container py-5">
            <h1>{data['title']}</h1>
        </div>
    </div>"""

    # Gallery
    type = data['type']
    media = data['media']
    image_list = []

    for image_link in media['images']:
        image_list.append(f'''<a href="assets/images/personal/{type}/{image_link['filename']}" class="glightbox" data-gallery="{type}-gallery">
            <img src="assets/images/personal/{type}/{image_link['filename']}" class="img-fluid gallery-image-small p-3" alt="{image_link['filename']}">
        </a>''')
    
    image_list_html = "\n".join(image_list)
    gallery_html = f'''<div class="container p-5">
        <div class="d-flex flex-wrap">
            {image_list_html}
        </div>
    </div>'''

    return f'{title_html}\n{gallery_html}'

def generate_personal_html(yaml_path, output_path):
    # Load the yaml file to read
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Get necessary html
    navbar = generate_navbar_html(data)
    body = generate_body(data)

    page_title = data['type'].capitalize()
    personal_html = html_boilerplate.format(title=page_title, navbar=navbar, body=body, script=script)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(personal_html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate research list using YAML files.")
    parser.add_argument("--yaml_path", default="generate/yaml/tea.yaml", type=str, help="Path to YAML file.")
    parser.add_argument("--output_path", default="generate/output/tea.html", type=str, help="Path to the output file.")
    args = parser.parse_args()

    generate_personal_html(args.yaml_path, args.output_path)