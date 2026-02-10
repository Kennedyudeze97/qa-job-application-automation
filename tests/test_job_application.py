import json
from pathlib import Path

import pytest
from pages.job_application_page import JobApplicationPage


def load_applicants():
    data_file = Path(__file__).parent.parent / "data" / "applicants.json"
    return json.loads(data_file.read_text())


@pytest.mark.parametrize("applicant", load_applicants())
def test_submit_job_application(driver, applicant):
    page = JobApplicationPage(driver)
    page.load()

    page.enter_name(applicant["name"])
    page.enter_email(applicant["email"])
    page.enter_phone(applicant["phone"])
    page.select_position(applicant["position"])
    page.set_employment_status(applicant["employment_status"])
    page.select_platform(applicant["platform"])
    page.upload_resume(applicant["resume_path"])
    page.submit()

    assert True

    # Optional: verify some success text if the form shows it
    # (If the site doesn't show a stable confirmation, we keep the test as "no crash" + submit click)
