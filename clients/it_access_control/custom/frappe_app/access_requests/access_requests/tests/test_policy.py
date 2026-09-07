from access_requests.policy import parse_security_levels, requires_security_approval


def test_standard_access_does_not_require_security():
    assert requires_security_approval("Standard") is False


def test_sensitive_and_privileged_require_security():
    assert requires_security_approval("Sensitive") is True
    assert requires_security_approval("Privileged") is True


def test_configured_levels_are_respected():
    assert parse_security_levels("Privileged") == {"Privileged"}
    assert requires_security_approval("Sensitive", "Privileged") is False
    assert requires_security_approval("Privileged", "Privileged") is True
