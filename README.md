## Developer Documentation: Evidence Surveillance Hub Prototype

This repository contains a Quarto-based static website for publishing outbreak evidence surveillance outputs. The site is built with Quarto, hosted through GitHub Pages, and deployed automatically using GitHub Actions.

The purpose of the project is to provide a searchable, downloadable, and maintainable public-facing interface for outbreak-specific evidence surveillance datasets.

---

## Technology Stack

* **Quarto**: Static site generation
* **Observable JavaScript (OJS)**: Interactive CSV loading, searching, filtering, and table display
* **GitHub Pages**: Static site hosting
* **GitHub Actions**: Automated rendering and deployment
* **CSV files**: Source data for outbreak evidence tables
* **XLSX files**: Optional full datasets for end-user download
* **CSS**: Custom styling for cards, tables, filters, buttons, and page layout

---

## Repository Structure

```text
Evidence-Surveillance-Hub-prototype/
├── _quarto.yml
├── index.qmd
├── outbreaks.qmd
├── methods.qmd
├── update-guide.qmd
├── styles.css
├── _recent-updates.md
├── scripts/
│   └── generate_recent_updates.py
├── outbreaks/
│   ├── mpox/
│   │   ├── index.qmd
│   │   └── data/
│   │       └── references.csv
│   ├── hantavirus/
│   │   ├── index.qmd
│   │   ├── background/
│   │   │   └── index.qmd
│   │   └── data/
│   │       └── references.csv
│   └── bundibugyo-ebola/
│       ├── index.qmd
│       └── data/
│           ├── references.csv
│           └── full-dataset.xlsx
└── .github/
    └── workflows/
        └── publish.yml
```

---

## Site Configuration

The main Quarto site configuration is stored in:

```text
_quarto.yml
```

This file controls the website title, navigation bar, search settings, theme, footer, and custom CSS.

The site uses:

```yaml
project:
  type: website
```

and applies global styling through:

```yaml
format:
  html:
    theme: cosmo
    css: styles.css
```

---

## Homepage

The homepage is defined in:

```text
index.qmd
```

It includes:

* A project introduction
* A prototype banner
* A “Recently Updated” section
* A summary of the site purpose
* A high-level workflow description
* Links to key pages

The “Recently Updated” section is generated automatically and included using:

```markdown
{{< include _recent-updates.md >}}
```

The included file is regenerated during deployment by:

```text
scripts/generate_recent_updates.py
```

---

## Outbreak Directory

The outbreak directory is defined in:

```text
outbreaks.qmd
```

Each outbreak is displayed as a card using Quarto div syntax:

```markdown
::: {.info-card}
### Hantavirus

Evidence surveillance data and background information for Hantavirus literature.

[View evidence](outbreaks/hantavirus/)  
[View background](outbreaks/hantavirus/background/)
```
