import threading
import time
import uuid

import jwt

from config import DiscordBot

_pending_states = {}
_state_lock = threading.Lock()

STATE_LIFETIME_SECONDS = 10 * 60


def create_update_url(
    config: DiscordBot, discord_id: int, display_name: str
) -> tuple[str, str]:
    """
    Create a one-time URL associated with a Discord user.
    """
    id = str(uuid.uuid4())

    state = {
        "id": id,
        "display_name": display_name,
        "discord_id": discord_id,
        "created_at": time.time(),
    }
    encoded_state = jwt.encode(state, config.shared_key, algorithm="HS256")
    return f"{config.auth_base_url}/update?state={encoded_state}", id


def create_pending_state(
    state, server_id: int | None, channel_id: int | None, message_id: int | None
):
    with _state_lock:
        _cleanup_expired_states_locked()
        _pending_states[state] = {
            "server_id": server_id,
            "channel_id": channel_id,
            "message_id": message_id,
            "created_at": time.time(),
        }


def _cleanup_expired_states_locked():
    now = time.time()

    expired = [
        state
        for state, entry in _pending_states.items()
        if (now - entry["created_at"] > STATE_LIFETIME_SECONDS)
    ]

    for state in expired:
        _pending_states.pop(state, None)


def _get_pending_state(state: str):
    with _state_lock:
        _cleanup_expired_states_locked()

        entry = _pending_states.get(state)

        if entry is None:
            return None

        return dict(entry)


def _consume_pending_state(state: str):
    with _state_lock:
        return _pending_states.pop(state, None)
