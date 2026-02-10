import pytest

@pytest.fixture
def resume_file(tmp_path):
    p = tmp_path / "resume.pdf"

    # Minimal PDF bytes (enough for file upload)
    p.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj<<>>endobj\n"
        b"trailer<<>>\n"
        b"%%EOF\n"
    )
    return str(p)

