import os
import pytest
import tempfile
from aquacrop.file_generators.DATA.plu_generator import generate_rainfall_file

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_daily_rainfall_file(temp_dir):
    test_file = os.path.join(temp_dir, "test_daily_rainfall.plu")
    location = "Daily rainfall of Location (Country)"
    rainfall_values = [0.0, 0.0, 16.6, 5.2, 0.0, 0.0, 10.3]
    
    # Generate the file with daily records
    generate_rainfall_file(
        file_path=test_file,
        location=location,
        rainfall_values=rainfall_values,
        record_type=1,  # Daily records
        first_day=1,
        first_month=1,
        first_year=2000
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Expected content based on Table 2.23h example
    expected_content = (
        f"{location}\n"
        f"     1  : Daily records (1=daily, 2=10-daily and 3=monthly data)\n"
        f"     1  : First day of record (1, 11 or 21 for 10-day or 1 for months)\n"
        f"     1  : First month of record\n"
        f"  2000  : First year of record (1901 if not linked to a specific year)\n"
        f"\n"
        f"  Total Rain (mm)\n"
        f"=======================\n"
        f"0.0\n"
        f"0.0\n"
        f"16.6\n"
        f"5.2\n"
        f"0.0\n"
        f"0.0\n"
        f"10.3"
    )
    assert content == expected_content

def test_10day_rainfall_file(temp_dir):
    test_file = os.path.join(temp_dir, "test_10day_rainfall.plu")
    location = "10-day rainfall of Location (Country)"
    rainfall_values = [25.0, 40.5, 15.0]
    
    # Generate the file with 10-day records
    generate_rainfall_file(
        file_path=test_file,
        location=location,
        rainfall_values=rainfall_values,
        record_type=2,  # 10-day records
        first_day=1,    # First day of 10-day period
        first_month=1,
        first_year=2000
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Expected content
    expected_content = (
        f"{location}\n"
        f"     2  : Daily records (1=daily, 2=10-daily and 3=monthly data)\n"
        f"     1  : First day of record (1, 11 or 21 for 10-day or 1 for months)\n"
        f"     1  : First month of record\n"
        f"  2000  : First year of record (1901 if not linked to a specific year)\n"
        f"\n"
        f"  Total Rain (mm)\n"
        f"=======================\n"
        f"25.0\n"
        f"40.5\n"
        f"15.0"
    )
    assert content == expected_content

def test_monthly_rainfall_file(temp_dir):
    test_file = os.path.join(temp_dir, "test_monthly_rainfall.plu")
    location = "Mean monthly rainfall for Region (Country)"
    monthly_values = [10.2, 15.5, 30.6, 45.9, 25.4, 5.8, 0.5, 0.2, 5.1, 20.2, 35.4, 20.0]
    
    # Generate the file with monthly records
    generate_rainfall_file(
        file_path=test_file,
        location=location,
        rainfall_values=monthly_values,
        record_type=3,  # Monthly records
        first_day=1,
        first_month=1,
        first_year=1901  # Not linked to a specific year
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Expected content
    expected_content = (
        f"{location}\n"
        f"     3  : Daily records (1=daily, 2=10-daily and 3=monthly data)\n"
        f"     1  : First day of record (1, 11 or 21 for 10-day or 1 for months)\n"
        f"     1  : First month of record\n"
        f"  1901  : First year of record (1901 if not linked to a specific year)\n"
        f"\n"
        f"  Total Rain (mm)\n"
        f"=======================\n"
        f"10.2\n"
        f"15.5\n"
        f"30.6\n"
        f"45.9\n"
        f"25.4\n"
        f"5.8\n"
        f"0.5\n"
        f"0.2\n"
        f"5.1\n"
        f"20.2\n"
        f"35.4\n"
        f"20.0"
    )
    assert content == expected_content

def test_invalid_record_type(temp_dir):
    test_file = os.path.join(temp_dir, "test_invalid_rainfall.plu")
    
    # Test with invalid record type
    with pytest.raises(ValueError, match="record_type must be 1, 2, or 3"):
        generate_rainfall_file(
            file_path=test_file,
            location="Invalid record type",
            rainfall_values=[10.0, 20.0],
            record_type=4  # Invalid record type
        )

def test_invalid_first_day_for_10day(temp_dir):
    test_file = os.path.join(temp_dir, "test_invalid_10day_rainfall.plu")
    
    # Test with invalid first day for 10-day records
    with pytest.raises(ValueError, match="first_day must be 1, 11, or 21 for 10-day records"):
        generate_rainfall_file(
            file_path=test_file,
            location="Invalid first day for 10-day",
            rainfall_values=[10.0, 20.0],
            record_type=2,  # 10-daily
            first_day=5     # Invalid first day for 10-day records
        )

def test_invalid_first_day_for_monthly(temp_dir):
    test_file = os.path.join(temp_dir, "test_invalid_monthly_rainfall.plu")
    
    # Test with invalid first day for monthly records
    with pytest.raises(ValueError, match="first_day must be 1 for monthly records"):
        generate_rainfall_file(
            file_path=test_file,
            location="Invalid first day for monthly",
            rainfall_values=[10.0, 20.0],
            record_type=3,  # Monthly
            first_day=2     # Invalid first day for monthly records
        )

def test_empty_rainfall_values(temp_dir):
    test_file = os.path.join(temp_dir, "test_empty_rainfall.plu")
    
    # Test with empty rainfall_values
    with pytest.raises(ValueError, match="rainfall_values must not be empty"):
        generate_rainfall_file(
            file_path=test_file,
            location="Empty rainfall values",
            rainfall_values=[]
        )