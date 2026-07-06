import platform

import pytest

from src.core.platform.platform_detector import Platform, PlatformDetector
from src.providers.factory import (
    get_encryption_provider,
    get_firewall_provider,
    get_system_provider,
    get_update_provider,
)


def test_platform_detector_matches_stdlib():
    detected = PlatformDetector.current()
    assert detected.value in (platform.system(), "Unknown")


@pytest.mark.skipif(
    PlatformDetector.current() == Platform.UNKNOWN,
    reason="No provider exists for an unrecognized platform.",
)
def test_factory_returns_a_provider_for_every_kind():
    assert get_firewall_provider() is not None
    assert get_encryption_provider() is not None
    assert get_update_provider() is not None
    assert get_system_provider() is not None
