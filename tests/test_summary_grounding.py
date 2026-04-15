from pathlib import Path


def test_summary_prompt_versions_exist():
    assert Path("prompts/summary/v1.txt").exists()
    assert Path("prompts/summary/v2.txt").exists()
