import time

import jwt

from config import DiscordBot


def create_update_url(config: DiscordBot, discord_id: int, display_name: str) -> str:
    """
    Create a one-time URL associated with a Discord user.
    """

    state = {
        "display_name": display_name,
        "discord_id": discord_id,
        "created_at": time.time(),
    }
    encoded_state = jwt.encode(state, config.shared_key, algorithm="HS256")
    return f"{config.auth_base_url}/update?state={encoded_state}"
