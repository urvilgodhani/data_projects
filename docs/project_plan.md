# Project Completion Record

This document records the delivered scope of the portfolio project. All core phases are complete; optional Power BI report authoring and future hosting changes can be added without changing the architecture.

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

Status: complete

- Created and connected a MongoDB Atlas cluster
- Added environment-based credentials
- Loaded analytics collections with `scripts/load_to_mongodb.py`
- Added current-state, snapshot, event, and manager-action collections
- Added TTL indexes for a bounded 72-hour live history

## Phase 4: Power BI

Status: data model and import workflow complete

- Exported clean CSV source tables
- Documented Home, Picking, Staging, Dispensing, Returns, and Store pages
- Defined button and bookmark navigation
- Defined read-only metric governance and manager action logging
- Kept the interactive web command center as the final public presentation

## Phase 5: GitHub Portfolio

Status: complete

- Published the repository and GitHub Pages dashboard
- Added a recruiter-focused README and architecture story
- Added current screenshots for all six dashboard views
- Added a Beacons-ready portfolio case study
- Added setup, data model, MongoDB, Power BI, live deployment, and Azure guides

## Phase 6: Live Operations Simulation

Status: complete

- Built a FastAPI service with health and live-data endpoints
- Updated approximately 10% of stores per simulation tick
- Connected current state and rolling history to MongoDB Atlas
- Added 72-hour TTL retention to control storage growth
- Added a browser fallback when the hosted API is unavailable

## Final Scope

- 50 synthetic stores
- 5,000 synthetic employees
- 12,000 synthetic orders
- 10 analytics datasets
- 6 interactive dashboard views
- Live API, MongoDB persistence, and rolling retention
- Auditable manager overrides with read-only operational metrics
