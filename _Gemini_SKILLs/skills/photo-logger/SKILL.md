---
name: photo-logger
description: photo-logger (根據照片檔名生成日誌)。根據包含序號、地點與描述的照片檔名，自動生成結構化的旅遊足跡日誌 (.md)。
---

# Photo Logger (根據照片檔名生成日誌)

## Overview

This skill enables the autonomous generation of a structured travel log from a collection of photos. It uses the metadata encoded in filenames—specifically dates, sequence numbers, locations, and descriptions—to reconstruct a chronological narrative of a trip or event.

## Core Logic

- **Filename Priority**: Always follow the numerical order of the sequence numbers (e.g., 001, 002...) in the filenames to determine the narrative flow.
- **Conciseness**: Keep descriptions brief and factual (approx. 10-20 words per item). Avoid excessive emotional or flowery language.
- **Item Merging**: If multiple consecutive photos belong to the same location, attraction, or restaurant, merge them into a single entry in the log.

## Content Structure

The generated log must be a `.md` file with the following sections:

### 1. Title
- Format: `# YYYY.MM.DD 足跡日誌` (or a date range if the photos span multiple days).

### 2. Route Summary (路線摘要)
- A concise list of all unique locations visited.
- Format: `### Location A → Location B → Location C`

### 3. Detailed Content (內容)
- For each unique location or major event:
  - **Header**: `### [Location/Attraction Name]`
  - **Description**: A bulleted list with a short description (10-20 words) mentioning key objects or highlights seen in the photos (e.g., specific dishes, landmarks, or activities).
  - **Formatting**: Do NOT use numbered lists (1. 2. 3.). Use bullet points (`-`).

## Storage Rules

- **Format**: Always save as a `.md` file.
- **Filename**: The filename of the log should match the name of the folder containing the photos.

## Example

### Input Filename:
`2026-03-08_095_Dudu_Vegetarian_Cafe_Old_House_Night_View.jpg`

### Output Log Entry:
### Dudu Vegetarian Cafe
- Enjoyed a quiet dinner in a renovated old house, featuring creative vegetarian dishes and a beautiful night view.
