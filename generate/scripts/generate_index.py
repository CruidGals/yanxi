import yaml
from pathlib import Path
import os
import argparse

# HTML Imports
from generate_research import generate_research_html
from generate_service import generate_service_html
from generate_teaching import generate_teaching_html
from generate_whats_new import generate_whats_new_html

index_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Homepage</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.5/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-SgOJa3DmI69IUzQ2PVdRZhwQ+dy64/BUtbMJw1MZ8t5HZApcHrRKUc4W0kG879m7" crossorigin="anonymous">
    <link href="https://cdn.jsdelivr.net/npm/glightbox/dist/css/glightbox.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">
    <link rel="stylesheet" href="/assets/styles.css">
</head>
<body>  
    {navbar}
    {home}

    <div class="section bg-light" id="whatsNewBlock">
        <h2>What's New</h2>
        {whats_new}
    </div>

    <div class="section" id="researchBlock">
        <h2>Research</h2>
        <div class="research-topics">
            <h3 class="section-year">Topics:</h3>
            <div class="section-group:">
                <div class="block">
                    <div class="block-other"><strong>Perception: </strong>Computer Vision versus Human Vision (Group-Theory based)</div>
                    <div class="block-other"><strong>Action: </strong>AI Planning, Robotics, Reconstruction/Tracking via Machine Learning</div>
                    <a href="https://sites.psu.edu/eecslpac/home">LPAC Website</a>
                    <a href="http://vivid.cse.psu.edu/texturedb/gallery/">Near-Regular Texture Databse</a>
                </div>
            </div>
        </div><hr />
        {research}
    </div>

    <div class="section bg-light" id="teachingBlock">
        <h2>Teaching</h2>
        {teaching}
    </div>

    <div class="section" id="serviceBlock">
        <h2>Service</h2>
        {service}
    </div>

    {contact}
    {script}
</body>
</html>
'''

navbar_html = '''<nav class="navbar fixed-top navbar-expand-md">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Dr. Yanxi Liu</a>

        <button class="navbar-toggler bg-white rounded mb-2" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="collapsibleNavbar">
            <ul class="navbar-nav ms-auto bg-white rounded">
                <li class="nav-item px-3 px-md-0">
                    <a class="nav-link active" href="#">Home</a>
                </li>
                <li class="nav-item px-3 px-md-0">
                    <a class="nav-link" href="#whatsNewBlock">What's New</a>
                </li>
                <li class="nav-item px-3 px-md-0">
                    <a class="nav-link" href="#researchBlock">Research</a>
                </li>
                <li class="nav-item px-3 px-md-0">
                    <a class="nav-link" href="#teachingBlock">Teaching</a>
                </li>
                <li class="nav-item px-3 px-md-0">
                    <a class="nav-link" href="#serviceBlock">Service</a>
                </li>
                <li class="nav-item dropdown px-3 px-md-0">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Personal</a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="tea.html">Tea</a></li>
                        <li><a class="dropdown-item" href="taiji.html">Taiji</a></li>
                        <li><a class="dropdown-item" href="quote.html">Quotes</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>
'''

home_html = '''<div class="container-fluid bg-secondary-subtle p-4">
    <div class="row">
        <div class="col-12">
            <div class="d-flex flex-column flex-sm-row justify-content-center align-items-center">
                <div class="m-2">
                    <img src="/assets/images/liuyanxi.jpg" class="w-75 h-auto rounded-5" alt="Yanxi Liu">
                </div>
                <div class="m-2">
                    <h1>Yanxi Liu</h1>
                    <p>
                        <a href="https://www.eecs.psu.edu/">Computer Science and Engineering</a> 
                        and 
                        <a href="http://www.ee.psu.edu/">Electrical Engineering,</a>
                    </p>
                    <p>
                        <a href="https://www.eecs.psu.edu/">College of Engineering,</a>
                        and
                        <a href="http://www.ee.psu.edu/">Penn State University.</a>
                    </p>

                    <p>Director for <strong>Motion Capture Lab for Smart Health</strong></p>
                    <p>Co-Director for the <strong>Lab for Perception, Action and Cognition</strong> <a href="https://sites.psu.edu/eecslpac/">(LPAC)</a></p>
                    <p><a href="http://scholar.google.com/citations?user=qYcG-q0AAAAJ">Google Scholar</a> | <a href="https://www.researchgate.net/profile/Yanxi_Liu">Research Gate</a> | <a href="https://www.linkedin.com/in/yanxi-liu-527643111">Linkedin</a> | <a href="http://vision.cse.psu.edu/publications/publications.shtml">LPAC Publications</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
'''

contact_html = '''<div class="container-fluid mt-3 p-5 bg-light" id="contactBlock">
    <div class="row">
        <div class="col-12 col-md-6 d-flex justify-content-center align-items-center p-3">
            <h1>Contact Info:</h1>
        </div>
        <div class="col-12 col-md-6 d-flex justify-content-center justify-content-md-start align-items-center">
            <div class="d-flex flex-column gap-3">
                <div class="d-flex flex-row align-items-baseline">
                    <i class="bi bi-geo-alt-fill fs-3 me-4"></i>
                    <h4>
                        Dr. Yanxi Liu <br>
                        W372 WESTGATE Building<br>
                        University Park, PA 16802<br>
                    </h4>
                </div>
                <div class="d-flex flex-row align-items-baseline">
                    <i class="bi bi-telephone-fill fs-3 me-4"></i>
                    <h4>(814) 865-7495</h4>
                </div>
                <div class="d-flex flex-row align-items-baseline">
                    <i class="bi bi-envelope-fill fs-3 me-4"></i>
                    <h4>firstname ATsign cse.psu.edu</h4>
                </div>
            </div>
        </div>
    </div>
</div>
'''

script_html = '''<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.5/dist/js/bootstrap.bundle.min.js" integrity="sha384-k6d4wzSIapyDyv1kpU366/PK5hCdSbCRGRCMv+eplOQJWyd1fbcAu9OCUj5zNLiq" crossorigin="anonymous"></script>
<script>
    const tabs = document.getElementsByClassName("nav-link");

    for (const tab of tabs) {
        tab.addEventListener("click", (e) => {
            activeTab = document.getElementsByClassName("active")[0];
            
            if (!tab.classList.contains('dropdown-toggle')) {
                activeTab.classList.toggle("active");
                tab.classList.toggle("active");
            }
        });
    }
</script>

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
</script>
'''

def generate_index_html(output_path):
    whats_new_html = generate_whats_new_html("generate/yaml/whats_new.yaml")
    research_html = generate_research_html("generate/yaml/research.yaml")
    teaching_html = generate_teaching_html("generate/yaml/teaching.yaml")
    service_html = generate_service_html("generate/yaml/service.yaml")

    index_html = index_template.format(navbar=navbar_html, home=home_html, whats_new=whats_new_html, research=research_html, teaching=teaching_html, service=service_html, contact=contact_html, script=script_html)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(index_html)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate index.htmlß")
    parser.add_argument("--output_path", default="generate/output/index.html", type=str, help="Path to the output file.")
    args = parser.parse_args()

    generate_index_html(args.output_path)