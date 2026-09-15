import pdfplumber
import re


def group_into_blocks(words):
    blocks = []

    for word in sorted(words, key=lambda word: (word["page"], word["top"], word["x"])):
        placed = False

        for block in blocks:
            same_page = block["page"] == word["page"]
            same_line = abs(block["top"] - word["top"]) < 2

            if not same_page or not same_line:
                continue

            last_word = block["words"][-1]
            gap = word["x"] - last_word["x_end"]

            if 0 <= gap < 20:
                block["words"].append(word)
                block["x_end"] = word["x_end"]
                placed = True
                break

        if not placed:
            blocks.append({
                "page": word["page"],
                "top": word["top"],
                "x_start": word["x"],
                "x_end": word["x_end"],
                "words": [word]
            })

    return blocks


def detect_columns(blocks):
    columns = []

    pages = sorted(set(
        block["page"]
        for block in blocks
    ))

    for page in pages:

        page_blocks = [
            block
            for block in blocks
            if block["page"] == page
        ]

        page_columns = []

        for block in sorted(
            page_blocks,
            key=lambda block: block["top"]
        ):

            placed = False

            for column in page_columns:

                vertical_gap = abs(
                    block["top"] - column["last_top"]
                )

                if vertical_gap > 100:
                    continue

                overlap = min(
                    column["x_end"],
                    block["x_end"]
                ) - max(
                    column["x_start"],
                    block["x_start"]
                )

                if overlap <= 0:
                    continue

                column["blocks"].append(block)

                column["x_start"] = min(
                    column["x_start"],
                    block["x_start"]
                )

                column["x_end"] = max(
                    column["x_end"],
                    block["x_end"]
                )

                column["last_top"] = block["top"]
                column["count"] += 1

                placed = True
                break

            if not placed:
                page_columns.append({
                    "page": page,
                    "x_start": block["x_start"],
                    "x_end": block["x_end"],
                    "last_top": block["top"],
                    "count": 1,
                    "blocks": [block]
                })

        page_columns = [
            column
            for column in page_columns
            if column["count"] >= 3
        ]

        # Remove columns that are completely contained inside another column
        filtered_columns = []

        for column in page_columns:
            is_nested = False

            for other in page_columns:
                if column is other:
                    continue

                if (
                        other["x_start"] <= column["x_start"]
                        and other["x_end"] >= column["x_end"]
                ):
                    is_nested = True
                    break

            if not is_nested:
                filtered_columns.append(column)

        page_columns = filtered_columns

        page_columns.sort(
            key=lambda column: column["x_start"]
        )

        columns.extend(page_columns)

    return columns


def assign_blocks_to_columns(blocks, columns):
    for block in blocks:
        best_column = None
        best_overlap = 0
        for index, column in enumerate(columns):
            if column["page"] != block["page"]:
                continue
            overlap = min(
                column["x_end"],
                block["x_end"]
            ) - max(
                column["x_start"],
                block["x_start"]
            )

            if overlap > best_overlap:
                best_overlap = overlap
                best_column = index

        if best_column is not None:
            block["column"] = best_column

    return blocks

def block_to_lines(blocks):
    ordered_blocks = sorted(
        blocks,
        key=lambda block: (
            block["page"],
            block.get("column", 999),
            block["top"]
            )
        )
    lines = []
    for block in ordered_blocks:
        line = " ".join(
            word["text"]
            for word in block["words"]
        )
        lines.append(line)
    return lines


def extract_text(path):
    extracted_words = []
    extracted_hyperlinks = []
    try:
        with pdfplumber.open(path) as pdf:
            for page_number, page in enumerate(pdf.pages):
                words = page.extract_words(x_tolerance=1)
                hyperlinks = page.hyperlinks

                for word in words:
                    extracted_words.append({
                        "text": word["text"],
                        "x": word["x0"],
                        "x_end": word["x1"],
                        "top": word["top"],
                        "bottom": word["bottom"],
                        "page": page_number,
                    })
                for hyperlink in hyperlinks:
                    extracted_hyperlinks.append(hyperlink["uri"])
            if not extracted_words:
                raise ValueError("PDF contains no extractable text.")

        blocks_from_words = group_into_blocks(extracted_words)
        columns = detect_columns(blocks_from_words)
        blocks = assign_blocks_to_columns(blocks_from_words, columns)
        personal_details = extract_personal_details(blocks, extracted_hyperlinks)
        lines = block_to_lines(blocks)
        return "\n".join(lines), personal_details

    except FileNotFoundError:
        print(f"Resume file not found: '{path}'")
        return "", None


def block_to_text(block):
    return " ".join(word["text"] for word in block["words"])


def extract_personal_details(blocks, extracted_hyperlinks):
    personal_details = {}
    top_block = min(blocks, key=lambda block: (
        block["page"],
        block["top"]
        )
    )
    name = block_to_text(top_block)
    personal_details["name"] = name

    email_pattern = re.compile(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    )
    phone_number_pattern = re.compile(
        r'(?:\+91[\s-]?)?[6-9]\d{9}'
    )
    linkedin_url_pattern = re.compile(
        r"(?:https?://)?(?:www\.)?"
        r"linkedin\.com/(?:in|company)/"
        r"[A-Za-z0-9_-]+/?"
    )
    github_url_pattern = re.compile(
        r"(?:https?://)?(?:www\.)?"
        r"github\.com/"
        r"[A-Za-z0-9_-]+/?"
    )

    emails = []
    phone_numbers = []
    linkedin_urls = []
    github_urls = []
    for block in blocks:
        block_text = block_to_text(block)
        email = email_pattern.search(block_text)
        phone_number = phone_number_pattern.search(block_text)
        if email :
            emails.append(email.group())
        if phone_number:
            phone_numbers.append(phone_number.group())

    for hyperlink in extracted_hyperlinks:
        linkedin_url = linkedin_url_pattern.search(hyperlink)
        github_url = github_url_pattern.search(hyperlink)
        if linkedin_url:
            linkedin_urls.append(linkedin_url.group())
        if github_url:
            github_urls.append(github_url.group())

    personal_details["email"] = emails[0] if emails else ""
    personal_details["phone_number"] = phone_numbers[0] if phone_numbers else ""
    personal_details["linkedin"] = linkedin_urls[0] if linkedin_urls else ""
    personal_details["github"] = github_urls[0] if github_urls else ""

    return personal_details
