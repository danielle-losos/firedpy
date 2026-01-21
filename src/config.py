from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Optional

_settings = None

def _get(name: str) -> Optional[str]:
    v = os.getenv(name)
    return v.strip() if isinstance(v, str) else v

@dataclass(frozen = True)
class Settings:
    # declare additional env vars/configs here
    firedpy_ed_user: Optional[str]
    firedpy_ed_pwd: Optional[str]

def _load_settings() -> Settings:
    # declare additional env vars/configs here
    return Settings(
        firedpy_ed_user = _get("FIREDPY_ED_USER"),
        firedpy_ed_pwd = _get("FIREDPY_ED_PWD")
    )

def _ensure_earthdata_env(settings: Settings) -> None:
    """
    earthaccess.login() for example requries EARTHDATA_USERNAME/PASSWORD to be declared as env vars.
    Make sure earthaccess can read EARTHDATA_USERNAME/PASSWORD from env.
    Do NOT require the user to set them explicitly.
    Do NOT overwrite if the user already set EARTHDATA_*.
    """
    if not os.getenv("EARTHDATA_USERNAME"):
        os.environ["EARTHDATA_USERNAME"] = settings.firedpy_ed_user
    if not os.getenv("EARTHDATA_PASSWORD"):
        os.environ["EARTHDATA_PASSWORD"] = settings.firedpy_ed_pwd

def _validate_settings(settings: Settings) -> None:
    # add validation for additional env vars/configs here
    err_message = ""
    if not settings.firedpy_ed_user:
        err_message = "FIREDPY_ED_USER env var is not set"
    elif not settings.firedpy_ed_pwd:
        err_message = "FIREDPY_ED_PWD env var is not set"
    else:
        # everything good
        return
    raise RuntimeError(err_message)

def get_settings():
    global _settings
    if _settings is None:
        s = _load_settings()
        _validate_settings(s)
        _ensure_earthdata_env(s)
        _settings = s
    return _settings
