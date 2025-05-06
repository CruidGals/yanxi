# Personal Website Generator

This is the source code for Dr. Yanxi Liu's website. You may also use this template for your own personal website.

## Generating Blocks of HTML

In the `index.html` file, the page is split into sections of **research**, **teaching**, and **service**. In the `/generate` directory, you can use the yaml files in `/generate/yaml` to add, remove, or edit the blocks within these sections

### Example:

To add another research paper, go into the `research.yaml` file. Then, add a research "block" as so:

```
-   title: [Title of paper]
    authors: [Authors of paper]
    publisher: [Publisher of paper]
    year: [Year of publication]
    links:
      - type: [Placeholder for link]
        url: [URL for link]
```

Once you are done adding research blocks, run the command

```
python generate/scripts/generate_research.py
```

to generate the HTML for the entire research section. It will be outputted as `research.html` in the `/generate/output` directory.