import hashlib
import secrets
from typing import Sequence, Any
from collections import defaultdict
import time
import streamlit as st


def hash_password(password: str) -> str:
    """Hash password with salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 100000
    )
    return f"{salt}${password_hash.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored hash"""
    try:
        salt, hash_hex = stored_hash.split("$", 1)
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), 100000
        )
        return password_hash.hex() == hash_hex
    except ValueError:
        return False


def group_by(all_items: Sequence, group_by: str) -> Any:
    """Group a sequence of items by a specified attribute"""
    grouped = defaultdict(list)
    for item in all_items:
        key = getattr(item, group_by)
        grouped[key].append(item)
    return dict(grouped)


def disappearing_message(st, message: str, msg_type: str, duration: int = 3):
    """Display a message that disappears after a certain duration"""
    try:
        if msg_type == "error":
            message_container = st.empty()
            message_container.error(message)
            time.sleep(duration)
            message_container.empty()
            return
        elif msg_type == "success":
            message_container = st.empty()
            message_container.success(message)
            time.sleep(duration)
            message_container.empty()
            return
        else:
            message_container = st.empty()
            message_container.info(message)
            time.sleep(duration)
            message_container.empty()
    except Exception as e:
        st.error(f"Error displaying disappearing message: {str(e)}")
