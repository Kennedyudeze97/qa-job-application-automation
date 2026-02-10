import json
from pathlib import Path

import pytest
from pages.job_application_page import JobApplicationPage


def load_applicants():
    data_file = Path(__file__).parent.parent / "data" / "applicants.json"
    return json.loads(data_file.read_text())


@pytest.mark.parametrize("applicant", load_applicants())
def test_submit_job_application(driver, applicant, resume_file):
    page = JobApplicationPage(driver)
    page.load()

    page.enter_name(applicant["name"])
    page.enter_email(applicant["email"])
    page.enter_phone(applicant["phone"])
    page.select_position(applicant["position"])
    page.set_employment_status(applicant["employment_status"])
    page.select_platform(applicant["platform"])

    page.upload_resume(resume_file)

    page.submit()
    assert page.is_success()

