from tools.run_behavior_pipeline import run
from tests.compatibility.test_behavior_requirement_resolution import requirements_fixture


def test_pipeline_defaults_to_manifest_derived_catalog(monkeypatch):
    captured = {}

    def fake_validate(resolution):
        captured["resolution"] = resolution
        return object()

    monkeypatch.setattr("tools.run_behavior_pipeline._validate_resolution", fake_validate)

    resolution, _ = run(requirements_fixture())

    assert resolution["publication_source"] == "manifest-derived"
    assert [binding["semantic_action"] for binding in resolution["bindings"]] == [
        "policy.resolve",
        "state.transition",
        "notification.send",
    ]
    assert captured["resolution"] is resolution
