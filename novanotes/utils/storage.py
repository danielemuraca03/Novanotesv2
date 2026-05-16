"""
NovaNotes — Supabase Storage helper.
Replaces local uploads/ folder with Supabase Storage bucket.

Usage in your page files:
    from utils.storage import upload_file, download_file, delete_file
"""

import streamlit as st
from supabase import create_client
import uuid
import os


def _get_client():
    """Create a Supabase client from Streamlit secrets."""
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )


BUCKET = "notes"  # must match the bucket you created in the dashboard


def upload_file(file_bytes: bytes, original_filename: str) -> str:
    """Upload a file to Supabase Storage.

    Args:
        file_bytes: the raw bytes of the uploaded file
        original_filename: e.g. 'lecture_3.pdf'

    Returns:
        The storage path (used as file_path in the notes table),
        e.g. 'a3f1b2c4_lecture_3.pdf'
    """
    # Prefix with a short UUID to avoid name collisions
    ext = os.path.splitext(original_filename)[1]
    safe_name = f"{uuid.uuid4().hex[:8]}_{original_filename}"

    client = _get_client()
    client.storage.from_(BUCKET).upload(
        path=safe_name,
        file=file_bytes,
        file_options={"content-type": _guess_mime(ext)},
    )
    return safe_name


def download_file(storage_path: str) -> bytes:
    """Download a file from Supabase Storage and return raw bytes."""
    client = _get_client()
    return client.storage.from_(BUCKET).download(storage_path)


def get_public_url(storage_path: str) -> str:
    """Get a public URL for a file (if bucket is public)."""
    client = _get_client()
    return client.storage.from_(BUCKET).get_public_url(storage_path)


def delete_file(storage_path: str):
    """Delete a file from Supabase Storage."""
    client = _get_client()
    client.storage.from_(BUCKET).remove([storage_path])


def _guess_mime(ext: str) -> str:
    """Return a MIME type for common note file extensions."""
    mapping = {
        ".pdf": "application/pdf",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
    return mapping.get(ext.lower(), "application/octet-stream")
