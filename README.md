# QA Job Application Automation (Selenium + PyTest)

A QA automation portfolio project that automates a job application form using **Selenium WebDriver** and **PyTest**, built with a **Page Object Model (POM)** and **data-driven testing**.

## Features
- Page Object Model structure (`pages/`, `tests/`, `data/`)
- Data-driven test runs using `data/applicants.json`
- Dropdown selections (position, employment status, platform)
- Resume upload using `<input type="file">`
- End-to-end submit flow validated by passing tests

## Project Structure
- `pages/` — Page Objects (selectors + actions)
- `tests/` — PyTest tests
- `data/` — Test data (`applicants.json`) and local resume file

## Setup (macOS)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

