
from fastapi import FastAPI, UploadFile, File, HTTPException
from bs4 import BeautifulSoup

app = FastAPI(
    title="Phase 3 CI/CD Integration API",
    description="REST API for processing HTML catalog files",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Phase 3 API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/process-html")
async def process_html(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".html"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an HTML file"
        )

    content = await file.read()

    try:
        soup = BeautifulSoup(content, "html.parser")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process HTML file"
        )

    title = soup.title.string.strip() if soup.title and soup.title.string else None

    headings = [
        heading.get_text(" ", strip=True)
        for heading in soup.find_all(["h1", "h2", "h3"])
    ]

    links = [
        {
            "text": link.get_text(" ", strip=True),
            "url": link.get("href")
        }
        for link in soup.find_all("a", href=True)
    ]

    return {
        "filename": file.filename,
        "title": title,
        "headings": headings,
        "links": links,
        "status": "success"
    }
