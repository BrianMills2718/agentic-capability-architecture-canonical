import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "capabilities/notifications/frappe_app/na_notifications/na_notifications/email.py"
spec = importlib.util.spec_from_file_location("na_notifications_email_test", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_normalize_single_recipient():
    assert module.normalize_recipients("person@example.com") == ["person@example.com"]


def test_normalize_multiple_recipients_and_blanks():
    assert module.normalize_recipients([" a@example.com ", "", "b@example.com"]) == [
        "a@example.com",
        "b@example.com",
    ]
