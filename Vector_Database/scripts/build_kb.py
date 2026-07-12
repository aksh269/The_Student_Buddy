import os
import re
import urllib.parse
import yaml
from datetime import datetime

# Define directories
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "daiict_document"))
DEST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "knowledge_base"))

# Directory name to OKF type mapping
TYPE_MAPPING = {
    "academic": "academic_rules",
    "academic rules-guidelines": "academic_rules",
    "admissions": "admission_info",
    "announcement": "announcements",
    "administration": "administrative_policy",
    "faculty": "faculty_profile",
    "placements": "placement_data",
    "programs_of_study": "study_program",
    "scholarships daiict 2026": "scholarship_details",
    "student_services": "student_services"
}

def clean_title(filename):
    # Decode URL encoding like %20, replace underscores/hyphens with spaces
    name = os.path.splitext(filename)[0]
    name = urllib.parse.unquote(name)
    name = name.replace("_", " ").replace("-", " ")
    # Clean up multiple spaces
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def parse_existing_frontmatter(content):
    # Check if file already has frontmatter
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if match:
        yaml_content = match.group(1)
        remaining_content = content[match.end():]
        try:
            data = yaml.safe_load(yaml_content)
            if isinstance(data, dict):
                return data, remaining_content
        except Exception:
            pass
    return {}, content

def infer_metadata(file_path, content, existing_meta):
    rel_path = os.path.relpath(file_path, SRC_DIR)
    parts = rel_path.split(os.sep)
    
    # 1. Infer Type
    inferred_type = "general_info"
    if parts:
        parent_dir = parts[0].lower()
        for key, val in TYPE_MAPPING.items():
            if key in parent_dir:
                inferred_type = val
                break
    
    # 2. Infer Title
    inferred_title = clean_title(os.path.basename(file_path))
    # Look for first # heading in content
    heading_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if heading_match:
        inferred_title = clean_title(heading_match.group(1).strip())

    # 3. Infer Source
    inferred_source = f"data/daiict_document/{rel_path.replace(os.sep, '/')}"
    source_match = re.search(r"Source:\s*[`']?([^`'\n]+)[`']?", content)
    if source_match:
        inferred_source = source_match.group(1).strip()

    # 4. Infer Description
    # Strip headings and source lines to find first text paragraph
    lines = content.split('\n')
    text_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('#') or stripped.startswith('Source:') or stripped.startswith('## Page'):
            continue
        text_lines.append(stripped)
        if len(text_lines) >= 3:
            break
    
    inferred_desc = ""
    if text_lines:
        inferred_desc = " ".join(text_lines)
        if len(inferred_desc) > 150:
            inferred_desc = inferred_desc[:147] + "..."
    else:
        inferred_desc = f"Information about {inferred_title} from DA-IICT documents."

    # 5. Infer Tags
    tags = [inferred_type.replace("_", "-")]
    if len(parts) > 1:
        tags.append(parts[0].lower().replace(" ", "-"))
    # Add a tag based on filename keywords
    filename_words = [w.lower() for w in re.findall(r'[a-zA-Z]+', os.path.basename(file_path))]
    for w in ["scholarship", "fees", "registration", "syllabus", "placement", "guidelines", "rules", "admission", "committee"]:
        if w in filename_words and w not in tags:
            tags.append(w)

    # Merge with existing
    meta = {
        "type": existing_meta.get("type") or inferred_type,
        "title": existing_meta.get("title") or inferred_title,
        "description": existing_meta.get("description") or inferred_desc,
        "source": existing_meta.get("source") or inferred_source,
        "tags": list(set(existing_meta.get("tags") or tags)),
        "last_updated": existing_meta.get("last_updated") or datetime.now().strftime("%Y-%m-%d")
    }
    return meta

def main():
    print(f"Scanning raw documents from: {SRC_DIR}")
    print(f"Outputting OKF bundle to: {DEST_DIR}")
    
    if not os.path.exists(SRC_DIR):
        print(f"Error: Source directory {SRC_DIR} does not exist.")
        return

    processed_count = 0
    
    for root, dirs, files in os.walk(SRC_DIR):
        for file in files:
            if not file.endswith(".md"):
                continue
            
            src_path = os.path.join(root, file)
            
            # Read content
            with open(src_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            # Parse any existing partial frontmatter
            existing_meta, clean_content = parse_existing_frontmatter(content)
            
            # Infer missing pieces
            meta = infer_metadata(src_path, clean_content, existing_meta)
            
            # Reconstruct content with standard frontmatter
            frontmatter = yaml.dump(meta, sort_keys=False, default_flow_style=False)
            new_content = f"---\n{frontmatter}---\n\n{clean_content.strip()}\n"
            
            # Determine destination path
            rel_path = os.path.relpath(src_path, SRC_DIR)
            # We want to preserve file names cleanly
            clean_filename = clean_title(file) + ".md"
            dest_subdir = os.path.dirname(rel_path)
            dest_dir_path = os.path.join(DEST_DIR, dest_subdir)
            
            os.makedirs(dest_dir_path, exist_ok=True)
            dest_path = os.path.join(dest_dir_path, clean_filename)
            
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(new_content)
                
            processed_count += 1
            print(f"Processed: {rel_path} -> {os.path.relpath(dest_path, DEST_DIR)}")
            
    print(f"\nSuccessfully processed {processed_count} files into the OKF bundle.")

if __name__ == "__main__":
    main()
