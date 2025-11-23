"""
Memo backend entrypoint: thin alias to the IdeasGlass FastAPI app.

Runs the same application (shared database, media paths, and static assets) but
lets you bind it on a different port/host for parallel access.
"""

from backend.glass.app import app  # re-export

