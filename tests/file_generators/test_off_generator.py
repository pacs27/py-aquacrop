import os
import tempfile

import pytest

from aquacrop.constants import Constants
from aquacrop.file_generators.DATA.off_generator import generate_offseason_file


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def test_offseason_basic(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")

    test_file = os.path.join(temp_dir, "test_off_basic.off")
    description = "Irrigation and field management conditions in the off-season"

    # Generate the file with basic settings (no irrigation events)
    generate_offseason_file(
        file_path=test_file,
        description=description,
        mulch_cover_before=0,
        mulch_cover_after=70,
        mulch_effect=50,
        num_irrigation_before=0,
        irrigation_quality_before=1.5,
        num_irrigation_after=0,
        irrigation_quality_after=4.0,
        surface_wetted_offseason=100,
    )

    # Check if file exists
    assert os.path.isfile(test_file)

    # Read and verify the content
    with open(test_file, "r") as f:
        content = f.read()

    # Check content based on Table 2.23v - 4 (without the irrigation event)
    assert description in content
    assert "7.1 : AquaCrop Version (August 2023)" in content
    assert (
        "0 : percentage (%) of ground surface covered by mulches BEFORE growing period"
        in content
    )
    assert (
        "70 : percentage (%) of ground surface covered by mulches AFTER growing period"
        in content
    )
    assert "50 : effect (%) of mulches on reduction of soil evaporation" in content
    assert "0 : number of irrigation events BEFORE growing period" in content
    assert "1.5 : quality of irrigation water BEFORE growing period (dS/m)" in content
    assert "0 : number of irrigation events AFTER growing period" in content
    assert "4.0 : quality of irrigation water AFTER growing period (dS/m)" in content
    assert (
        "100 : percentage (%) of soil surface wetted by off-season irrigation"
        in content
    )

    # Should not contain irrigation events
    assert "Day Depth(mm) When" not in content


def test_offseason_with_irrigation_before(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")

    test_file = os.path.join(temp_dir, "test_off_irr_before.off")
    description = "Irrigation and field management conditions in the off-season"

    # Irrigation events before the growing period from Table 2.23v - 4
    irrigation_events_before = [{"day": 10, "depth": 40}]

    # Generate the file with irrigation before the growing period
    generate_offseason_file(
        file_path=test_file,
        description=description,
        mulch_cover_before=0,
        mulch_cover_after=70,
        mulch_effect=50,
        num_irrigation_before=1,
        irrigation_quality_before=1.5,
        irrigation_events_before=irrigation_events_before,
        num_irrigation_after=0,
        irrigation_quality_after=4.0,
        surface_wetted_offseason=100,
    )

    # Check if file exists
    assert os.path.isfile(test_file)

    # Read and verify the content
    with open(test_file, "r") as f:
        content = f.read()

    # Check content based on Table 2.23v - 4 (full example)
    assert description in content
    assert "7.1 : AquaCrop Version (August 2023)" in content
    assert (
        "0 : percentage (%) of ground surface covered by mulches BEFORE growing period"
        in content
    )
    assert (
        "70 : percentage (%) of ground surface covered by mulches AFTER growing period"
        in content
    )
    assert "50 : effect (%) of mulches on reduction of soil evaporation" in content
    assert "1 : number of irrigation events BEFORE growing period" in content
    assert "1.5 : quality of irrigation water BEFORE growing period (dS/m)" in content
    assert "0 : number of irrigation events AFTER growing period" in content
    assert "4.0 : quality of irrigation water AFTER growing period (dS/m)" in content
    assert (
        "100 : percentage (%) of soil surface wetted by off-season irrigation"
        in content
    )

    # Check irrigation events section
    assert "Day Depth(mm) When" in content
    assert "=================================" in content
    assert "10 40 before season" in content


def test_offseason_with_irrigation_after(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")

    test_file = os.path.join(temp_dir, "test_off_irr_after.off")
    description = "Off-season with irrigation after growing period"

    # Irrigation events after the growing period
    irrigation_events_after = [{"day": 15, "depth": 50}, {"day": 30, "depth": 45}]

    # Generate the file with irrigation after the growing period
    generate_offseason_file(
        file_path=test_file,
        description=description,
        mulch_cover_before=20,
        mulch_cover_after=60,
        mulch_effect=50,
        num_irrigation_before=0,
        irrigation_quality_before=1.0,
        num_irrigation_after=2,
        irrigation_quality_after=2.0,
        irrigation_events_after=irrigation_events_after,
        surface_wetted_offseason=100,
    )

    # Check if file exists
    assert os.path.isfile(test_file)

    # Read and verify the content
    with open(test_file, "r") as f:
        content = f.read()

    # Check basic content
    assert description in content
    assert "7.1 : AquaCrop Version (August 2023)" in content
    assert (
        "20 : percentage (%) of ground surface covered by mulches BEFORE growing period"
        in content
    )
    assert (
        "60 : percentage (%) of ground surface covered by mulches AFTER growing period"
        in content
    )
    assert "0 : number of irrigation events BEFORE growing period" in content
    assert "2 : number of irrigation events AFTER growing period" in content
    assert "2.0 : quality of irrigation water AFTER growing period (dS/m)" in content

    # Check irrigation events section
    assert "Day Depth(mm) When" in content
    assert "=================================" in content
    assert "15 50 after season" in content
    assert "30 45 after season" in content


def test_offseason_with_both_irrigation_periods(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")

    test_file = os.path.join(temp_dir, "test_off_irr_both.off")
    description = "Off-season with irrigation events before and after growing period"

    # Irrigation events before and after
    irrigation_events_before = [{"day": 5, "depth": 30}, {"day": 15, "depth": 35}]

    irrigation_events_after = [{"day": 10, "depth": 40}, {"day": 25, "depth": 45}]

    # Generate the file with irrigation before and after
    generate_offseason_file(
        file_path=test_file,
        description=description,
        mulch_cover_before=30,
        mulch_cover_after=40,
        mulch_effect=60,
        num_irrigation_before=2,
        irrigation_quality_before=1.2,
        irrigation_events_before=irrigation_events_before,
        num_irrigation_after=2,
        irrigation_quality_after=1.5,
        irrigation_events_after=irrigation_events_after,
        surface_wetted_offseason=80,
    )

    # Check if file exists
    assert os.path.isfile(test_file)

    # Read and verify the content
    with open(test_file, "r") as f:
        content = f.read()

    # Check basic content
    assert description in content
    assert (
        "30 : percentage (%) of ground surface covered by mulches BEFORE growing period"
        in content
    )
    assert (
        "40 : percentage (%) of ground surface covered by mulches AFTER growing period"
        in content
    )
    assert "60 : effect (%) of mulches on reduction of soil evaporation" in content
    assert "2 : number of irrigation events BEFORE growing period" in content
    assert "1.2 : quality of irrigation water BEFORE growing period (dS/m)" in content
    assert "2 : number of irrigation events AFTER growing period" in content
    assert "1.5 : quality of irrigation water AFTER growing period (dS/m)" in content
    assert (
        "80 : percentage (%) of soil surface wetted by off-season irrigation" in content
    )

    # Check irrigation events section
    assert "Day Depth(mm) When" in content
    assert "=================================" in content
    assert "5 30 before season" in content
    assert "15 35 before season" in content
    assert "10 40 after season" in content
    assert "25 45 after season" in content


def test_offseason_with_different_surface_wetted(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")

    # Test different surface wetted percentages from Table 2.23v - 3
    surface_wetted_values = [100, 60, 40, 30, 15, 0]

    for wetted_pct in surface_wetted_values:
        test_file = os.path.join(temp_dir, f"test_off_wetted_{wetted_pct}.off")
        description = f"Off-season with {wetted_pct}% surface wetted"

        # Generate the file with different surface wetted percentages
        generate_offseason_file(
            file_path=test_file,
            description=description,
            mulch_cover_before=0,
            mulch_cover_after=0,
            mulch_effect=50,
            num_irrigation_before=0,
            irrigation_quality_before=0.0,
            num_irrigation_after=0,
            irrigation_quality_after=0.0,
            surface_wetted_offseason=wetted_pct,
        )

        # Check if file exists
        assert os.path.isfile(test_file)

        # Read and verify the content
        with open(test_file, "r") as f:
            content = f.read()

        # Check if surface wetted percentage is correct
        assert (
            f"{wetted_pct} : percentage (%) of soil surface wetted by off-season irrigation"
            in content
        )


def test_offseason_count_validation(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")

    test_file = os.path.join(temp_dir, "test_off_validation.off")
    description = "Off-season with count validation"

    # Provide mismatched counts and events
    irrigation_events_before = [{"day": 5, "depth": 30}, {"day": 15, "depth": 35}]

    irrigation_events_after = [{"day": 10, "depth": 40}]

    # Generate the file with mismatched counts
    generate_offseason_file(
        file_path=test_file,
        description=description,
        mulch_cover_before=30,
        mulch_cover_after=40,
        mulch_effect=60,
        num_irrigation_before=1,  # Says 1 but we provide 2
        irrigation_quality_before=1.2,
        irrigation_events_before=irrigation_events_before,
        num_irrigation_after=2,  # Says 2 but we provide 1
        irrigation_quality_after=1.5,
        irrigation_events_after=irrigation_events_after,
        surface_wetted_offseason=80,
    )

    # Check if file exists
    assert os.path.isfile(test_file)

    # Read and verify the content - check if counts were automatically corrected
    with open(test_file, "r") as f:
        content = f.read()

    # Should have 2 before and 1 after
    assert "2 : number of irrigation events BEFORE growing period" in content
    assert "1 : number of irrigation events AFTER growing period" in content
