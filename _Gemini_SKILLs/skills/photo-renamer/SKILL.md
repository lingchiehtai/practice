---
name: photo-renamer
description: photo-renamer (照片檔名加上關鍵字)。結合照片內容與 mynote.txt 的上下文，為照片檔名添加 2-6 個描述性關鍵字。
---

# Photo Renamer (照片檔名加上關鍵字)

This skill automates the process of renaming photo files by analyzing their content alongside text notes (usually `mynote.txt`).

## Workflow

1.  **Preparation**:
    - Ensure `.jpg` files and `mynote.txt` are present in the current directory.
    - Read `mynote.txt` to gather context.

2.  **Processing Loop**:
    For each `.jpg` file in the directory:
    - Analyze the image and the context from `mynote.txt`.
    - Generate a new filename using the following logic:

    **System Prompt Logic**:
    - The new filename MUST start with the exact original filename (without extension).
    - Append **2-6 descriptive keywords** based on image content (e.g., text found in the image, specific ingredients, objects) and notes, separated by underscores (`_`).
    - **Forbidden Keywords**: Do NOT include: `人像`, `人物`, `景觀`, `女子`, `男子`, `女性`, `男性`, `合照`, `多人合照`, `比讚`, `比YA`, `微笑`, `笑臉`.
    - Do NOT change the file extension.
    - If notes don't match the image, rely only on visual content.
    - The AI response for the name should be ONLY the new filename.

3.  **Renaming**:
    - If a new name is generated and differs from the original, rename the file using `mv` or equivalent.
    - Log success or skip/error for each file.

## Example Command
"Use the photo-renamer skill to process the images in this folder."
