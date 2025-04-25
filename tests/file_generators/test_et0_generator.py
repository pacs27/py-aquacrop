import os
import pytest
import tempfile
from aquacrop.file_generators.DATA.eto_generator import generate_eto_file

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_daily_eto_file(temp_dir):
    test_file = os.path.join(temp_dir, "test_daily_eto.eto")
    location = "Daily reference evapotranspiration (ETo) of Location (Country)"
    eto_values = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
    
    # Generate the file with daily records
    generate_eto_file(
        file_path=test_file,
        location=location,
        eto_values=eto_values,
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
    
    # Expected content based on Table 2.23f example
    expected_content = (
        f"{location}\n"
        f"     1  : Daily records (1=daily, 2=10-daily and 3=monthly data)\n"
        f"     1  : First day of record (1, 11 or 21 for 10-day or 1 for months)\n"
        f"     1  : First month of record\n"
        f"  2000  : First year of record (1901 if not linked to a specific year)\n"
        f"\n"
        f"  Average ETo (mm/day)\n"
        f"=======================\n"
        f"1.0\n"
        f"1.1\n"
        f"1.2\n"
        f"1.3\n"
        f"1.4\n"
        f"1.5\n"
        f"1.6"
    )
    assert content == expected_content

def test_10day_eto_file(temp_dir):
    test_file = os.path.join(temp_dir, "test_10day_eto.eto")
    location = "10-day reference evapotranspiration (ETo) of Location (Country)"
    eto_values = [2.0, 2.5, 3.0]
    
    # Generate the file with 10-day records
    generate_eto_file(
        file_path=test_file,
        location=location,
        eto_values=eto_values,
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
        f"  Average ETo (mm/day)\n"
        f"=======================\n"
        f"2.0\n"
        f"2.5\n"
        f"3.0"
    )
    assert content == expected_content

def test_monthly_eto_file(temp_dir):
    test_file = os.path.join(temp_dir, "test_monthly_eto.eto")
    location = "Mean monthly ETo for Axum (Ethiopia)"
    # Monthly ETo values from Table 2.23i example
    eto_values = [3.4, 3.5, 4.6, 4.9, 5.4, 4.8, 3.5, 3.2, 4.1, 4.2, 3.4, 3.0]
    
    # Generate the file with monthly records
    generate_eto_file(
        file_path=test_file,
        location=location,
        eto_values=eto_values,
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
    
    # Expected content based on Table 2.23i example
    expected_content = (
        f"{location}\n"
        f"     3  : Daily records (1=daily, 2=10-daily and 3=monthly data)\n"
        f"     1  : First day of record (1, 11 or 21 for 10-day or 1 for months)\n"
        f"     1  : First month of record\n"
        f"  1901  : First year of record (1901 if not linked to a specific year)\n"
        f"\n"
        f"  Average ETo (mm/day)\n"
        f"=======================\n"
        f"3.4\n"
        f"3.5\n"
        f"4.6\n"
        f"4.9\n"
        f"5.4\n"
        f"4.8\n"
        f"3.5\n"
        f"3.2\n"
        f"4.1\n"
        f"4.2\n"
        f"3.4\n"
        f"3.0"
    )
    assert content == expected_content

def test_invalid_record_type(temp_dir):
    test_file = os.path.join(temp_dir, "test_invalid_eto.eto")
    
    # Test with invalid record type
    with pytest.raises(ValueError, match="record_type must be 1, 2, or 3"):
        generate_eto_file(
            file_path=test_file,
            location="Invalid record type",
            eto_values=[1.0, 2.0],
            record_type=4  # Invalid record type
        )

def test_invalid_first_day_for_10day(temp_dir):
    test_file = os.path.join(temp_dir, "test_invalid_10day_eto.eto")
    
    # Test with invalid first day for 10-day records
    with pytest.raises(ValueError, match="first_day must be 1, 11, or 21 for 10-day records"):
        generate_eto_file(
            file_path=test_file,
            location="Invalid first day for 10-day",
            eto_values=[1.0, 2.0],
            record_type=2,  # 10-daily
            first_day=5     # Invalid first day for 10-day records
        )

def test_invalid_first_day_for_monthly(temp_dir):
    test_file = os.path.join(temp_dir, "test_invalid_monthly_eto.eto")
    
    # Test with invalid first day for monthly records
    with pytest.raises(ValueError, match="first_day must be 1 for monthly records"):
        generate_eto_file(
            file_path=test_file,
            location="Invalid first day for monthly",
            eto_values=[1.0, 2.0],
            record_type=3,  # Monthly
            first_day=2     # Invalid first day for monthly records
        )

def test_empty_eto_values(temp_dir):
    test_file = os.path.join(temp_dir, "test_empty_eto.eto")
    
    # Test with empty eto_values
    with pytest.raises(ValueError, match="eto_values must not be empty"):
        generate_eto_file(
            file_path=test_file,
            location="Empty ETo values",
            eto_values=[]
        )