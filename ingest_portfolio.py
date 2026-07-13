import os
import sys
import uuid
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add app to path if running from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.rag.embedder import embed_and_upsert_chunks

def parse_html_resume(file_path: str):
    """
    Parses the HTML resume and returns semantic chunks.
    Parent-Child Strategy: 
    - Parent = Section Title (e.g. Featured Projects) + Item Title
    - Child = Individual Bullet Points / Paragraphs
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        logger.error("BeautifulSoup not found! Please run: pip install beautifulsoup4")
        sys.exit(1)

    logger.info(f"Parsing HTML resume: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    soup = BeautifulSoup(html_content, "html.parser")
    main_content = soup.find("main")
    
    if not main_content:
        logger.error("Could not find <main> tag in HTML!")
        sys.exit(1)
    
    chunks = []
    
    # 1. Parse Header (Name, Title, Contact)
    header = main_content.find("header")
    if header:
        header_text = header.get_text(separator="\n", strip=True)
        chunks.append({
            "chunk_id": str(uuid.uuid4()),
            "text": f"PORTFOLIO_OWNER_CONTACT_INFO: {header_text}",
            "metadata": {
                "source_file": "ambuj_resume.html",
                "page": 1,
                "chunk_type": "header_contact",
                "parent_text": header_text
            }
        })

    # 2. Parse Sections dynamically
    sections = main_content.find_all("section")
    for section in sections:
        section_title = section.find("h2", class_="section-title")
        if not section_title:
            continue
            
        parent_title = section_title.get_text(strip=True)
        
        # 2a. Find Articles (Projects / Experience)
        articles = section.find_all("article")
        if articles:
            for article in articles:
                item_title = article.find("h3")
                item_title_text = item_title.get_text(strip=True) if item_title else "Details"
                
                # Tech used or company line
                subtext = article.find("p", class_=["tech-used", "company-line"])
                subtext_content = subtext.get_text(strip=True) if subtext else ""
                
                # Bullets
                bullets = article.find_all("li")
                
                full_parent_text = f"Section: {parent_title}\nItem: {item_title_text}\n{subtext_content}"
                
                # Add Parent Chunk
                chunks.append({
                    "chunk_id": str(uuid.uuid4()),
                    "text": full_parent_text,
                    "metadata": {
                        "source_file": "ambuj_resume.html",
                        "page": 1,
                        "chunk_type": "parent_context",
                        "parent_text": full_parent_text
                    }
                })
                
                for bullet in bullets:
                    bullet_text = bullet.get_text(strip=True)
                    chunk_text = f"Context: {parent_title} - {item_title_text}\n{bullet_text}"
                    
                    chunks.append({
                        "chunk_id": str(uuid.uuid4()),
                        "text": chunk_text,
                        "metadata": {
                            "source_file": "ambuj_resume.html",
                            "page": 1,
                            "chunk_type": "bullet_point",
                            "parent_text": full_parent_text
                        }
                    })
        else:
            # 2b. General Sections without articles (Summary, Skills, Certs, Education)
            elements = section.find_all(["p", "div", "li"])
            
            # Combine to prevent over-fragmenting small sections like Summary
            combined_text = []
            for el in elements:
                text = el.get_text(strip=True)
                if len(text) > 10: 
                    combined_text.append(text)
            
            if combined_text:
                full_text = " ".join(combined_text)
                chunk_text = f"Context: {parent_title}\n{full_text}"
                chunks.append({
                    "chunk_id": str(uuid.uuid4()),
                    "text": chunk_text,
                    "metadata": {
                        "source_file": "ambuj_resume.html",
                        "page": 1,
                        "chunk_type": "general_info",
                        "parent_text": f"Section: {parent_title}"
                    }
                })

    logger.info(f"Generated {len(chunks)} semantic chunks from HTML.")
    return chunks

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    resume_path = os.path.join("data", "ambuj_resume.html")
    if not os.path.exists(resume_path):
        logger.error(f"Error: {resume_path} not found!")
        sys.exit(1)
        
    chunks = parse_html_resume(resume_path)
    
    # Ingest into Pinecone using existing Jina Embedder
    # Using a dedicated namespace to keep it isolated from Legal/Financial data
    try:
        logger.info("Starting embedding process using Jina v3 (this might take a minute)...")
        total_upserted = embed_and_upsert_chunks(
            chunks=chunks,
            source_file="ambuj_resume.html",
            namespace="ambuj_portfolio"
        )
        print(f"\n=======================================================")
        print(f"✅ SUCCESS! {total_upserted} chunks embedded and upserted to Pinecone.")
        print(f"🎯 Namespace: 'ambuj_portfolio'")
        print(f"=======================================================\n")
    except Exception as e:
        logger.error(f"Failed to ingest: {e}")
