
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_process_html():
    html = """
    <html>
        <head><title>Student Catalog</title></head>
        <body>
            <h1>Students</h1>
            <a href="/students">View Students</a>
        </body>
    </html>
    """

    response = client.post(
        "/process-html",
        files={"file": ("students.html", html, "text/html")}
    )

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Student Catalog"
    assert "Students" in data["headings"]
    assert data["links"][0]["url"] == "/students"


def test_process_html_rejects_wrong_file():
    response = client.post(
        "/process-html",
        files={"file": ("students.txt", "test content", "text/plain")}
    )

    assert response.status_code == 400
