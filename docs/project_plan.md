# Project Plan

## Phase 1: Local Analytics Foundation

Status: complete

- Generate synthetic stores, employees, and orders
- Calculate operational KPIs
- Export dashboard-ready CSV files
- Build local command-center dashboard

## Phase 2: Command Center Experience

Status: complete

- Home screen with 5 main tiles
- Picking drill-through page
- Staging drill-through page
- Dispensing drill-through page
- Returns and exceptions page
- Total Store selector and store dashboard
- Manager override action logging concept

## Phase 3: MongoDB Atlas

Status: ready to connect

- Create Atlas cluster
- Add environment variables
- Run `scripts/load_to_mongodb.py`
- Confirm collections are loaded
- Add indexes if the dataset grows

## Phase 4: Power BI

Status: ready to build

- Import CSV files first
- Build Home, Picking, Staging, Dispensing, Returns, and Store pages
- Use buttons/bookmarks for navigation
- Keep metrics read-only
- Add manager action-log visual

## Phase 5: GitHub Portfolio

Status: ready to publish

- Initialize Git
- Commit project files
- Create GitHub repository
- Push code
- Add screenshots
- Add Power BI screenshots or exported PDF

