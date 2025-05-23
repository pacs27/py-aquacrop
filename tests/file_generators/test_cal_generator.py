import os
import pytest
import tempfile
from aquacrop.file_generators.DATA.cal_generator import generate_calendar_file
from aquacrop.constants import Constants

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_fixed_date_calendar_file(temp_dir, monkeypatch):
    # Mock the Constants.AQUACROP_VERSION_NUMBER and Constants.AQUACROP_VERSION_DATE
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_fixed.cal")
    description = "Fixed date calendar for testing"
    day_number = 274  # October 1st
    
    # Generate the file
    generate_calendar_file(
        file_path=test_file,
        description=description,
        onset_mode=0,
        day_number=day_number
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    expected_content = (
        f"{description}\n"
        f"7.1 : AquaCrop Version (August 2023)\n"
        f"0 : The onset of the growing period is fixed on a specific date\n"
        f"-9 : Day-number (1 ... 366) of the Start of the time window for the onset criterion: Not applicable\n"
        f"-9 : Length (days) of the time window for the onset criterion: Not applicable\n"
        f"274 : Day-number (1 ... 366) for the onset of the growing period\n"
        f"-9 : Preset value for generation of the onset: Not applicable\n"
        f"-9 : Number of successive days: Not applicable\n"
        f"-9 : Number of occurrences: Not applicable"
    )
    assert content == expected_content

def test_rainfall_criteria_calendar_file(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_criteria.cal")
    description = "1st occurrence 20 mm Rain in 4 days since 1/10"
    
    # Generate the file with criteria mode
    generate_calendar_file(
        file_path=test_file,
        description=description,
        onset_mode=1,
        window_start_day=274,  # Oct 1st
        window_length=92,
        criterion_number=2,  # Observed rainfall during successive days
        criterion_value=20.0,
        successive_days=4,
        occurrences=1
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Expected content based on Table 2.23o4 example
    expected_content = (
        f"{description}\n"
        f"7.1 : AquaCrop Version (August 2023)\n"
        f"1 : The onset of the growing period is generated by a rainfall or air temperature criterion\n"
        f"274 : Day-number (1 ... 366) of the Start of the time window for the onset criterion\n"
        f"92 : Length (days) of the time window for the onset criterion\n"
        f"2 : Criterion Nr (Observed rainfall)\n"
        f"20.0 : Preset value of Observed rainfall (mm)\n"
        f"4 : Number of successive days for the onset criterion\n"
        f"1 : Number of occurrences before the onset criterion applies (max = 3)"
    )
    assert content == expected_content

def test_temperature_criteria_calendar_file(temp_dir, monkeypatch):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_temp_criteria.cal")
    description = "Calendar with temperature criteria"
    
    # Generate the file with temperature criteria mode
    generate_calendar_file(
        file_path=test_file,
        description=description,
        onset_mode=1,
        window_start_day=1,  # Jan 1st
        window_length=60,
        criterion_number=12,  # Average air temperature threshold
        criterion_value=15.0,
        successive_days=5,
        occurrences=2
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    expected_content = (
        f"{description}\n"
        f"7.1 : AquaCrop Version (August 2023)\n"
        f"1 : The onset of the growing period is generated by a rainfall or air temperature criterion\n"
        f"1 : Day-number (1 ... 366) of the Start of the time window for the onset criterion\n"
        f"60 : Length (days) of the time window for the onset criterion\n"
        f"12 : Criterion Nr (Average air temperature)\n"
        f"15.0 : Preset value of Average air temperature (°C)\n"
        f"5 : Number of successive days for the onset criterion\n"
        f"2 : Number of occurrences before the onset criterion applies (max = 3)"
    )
    assert content == expected_content

def test_invalid_day_number(temp_dir):
    test_file = os.path.join(temp_dir, "test_invalid.cal")
    
    # Test with invalid day number
    with pytest.raises(ValueError, match="day_number must be between 1 and 366"):
        generate_calendar_file(
            file_path=test_file,
            description="Invalid calendar",
            day_number=367
        )
    
    with pytest.raises(ValueError, match="day_number must be between 1 and 366"):
        generate_calendar_file(
            file_path=test_file,
            description="Invalid calendar",
            day_number=0
        )

def test_invalid_criterion_number(temp_dir):
    test_file = os.path.join(temp_dir, "test_invalid_criterion.cal")
    
    # Test with invalid criterion number
    with pytest.raises(ValueError, match="criterion_number must be one of: 1, 2, 3, 4, 11, 12, 13, 14"):
        generate_calendar_file(
            file_path=test_file,
            description="Invalid calendar",
            onset_mode=1,
            window_start_day=1,
            window_length=60,
            criterion_number=5,  # Invalid criterion number
            criterion_value=15.0,
            successive_days=5,
            occurrences=2
        )