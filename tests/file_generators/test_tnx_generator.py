import os
import pytest
import tempfile
from aquacrop.file_generators.DATA.tnx_generator import generate_temperature_file

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_daily_temperature_file(temp_dir):
    test_file = os.path.join(temp_dir, "test_daily_temperature.tnx")
    location = "Daily air temperature data of Location (Country)"
    
    # Temperature data as (tmin, tmax) tuples
    temperature_values = [
        (7.0, 15.0),
        (8.0, 16.0),
        (9.0, 18.0),
        (7.5, 17.2),
        (8.2, 16.8)
    ]
    
    # Generate the file with daily records
    generate_temperature_file(
        file_path=test_file,
        location=location,
        temperatures=temperature_values,
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
    
    # Expected content based on Table 2.23d example
    expected_content = (
        f"{location}\n"
        f"     1  : Daily records (1=daily, 2=10-daily and 3=monthly data)\n"
        f"     1  : First day of record (1, 11 or 21 for 10-day or 1 for months)\n"
        f"     1  : First month of record\n"
        f"  2000  : First year of record (1901 if not linked to a specific year)\n"
        f"\n"
        f"  Tmin (C)   TMax (C)\n"
        f"========================\n"
        f"7.0\t15.0\n"
        f"8.0\t16.0\n"
        f"9.0\t18.0\n"
        f"7.5\t17.2\n"
        f"8.2\t16.8"
    )
    assert content == expected_content

def test_10day_temperature_file(temp_dir):
    test_file = os.path.join(temp_dir, "test_10day_temperature.tnx")
    location = "10-day air temperature data of Location (Country)"
    
    # 10-day average temperature data
    temperature_values = [
        (5.0, 15.0),
        (6.5, 16.5),
        (8.0, 18.0)
    ]
    
    # Generate the file with 10-day records
    generate_temperature_file(
        file_path=test_file,
        location=location,
        temperatures=temperature_values,
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
        f"  Tmin (C)   TMax (C)\n"
        f"========================\n"
        f"5.0\t15.0\n"
        f"6.5\t16.5\n"
        f"8.0\t18.0"
    )
    assert content == expected_content

def test_monthly_temperature_file(temp_dir):
    test_file = os.path.join(temp_dir, "test_monthly_temperature.tnx")
    location = "Mean monthly temperature for Region (Country)"
    
    # Monthly average temperature data
    monthly_values = [
        (2.0, 10.0),
        (3.0, 12.0),
        (5.0, 15.0),
        (8.0, 18.0),
        (12.0, 22.0),
        (15.0, 26.0),
        (18.0, 30.0),
        (17.0, 28.0),
        (14.0, 25.0),
        (10.0, 20.0),
        (5.0, 15.0),
        (3.0, 12.0)
    ]
    
    # Generate the file with monthly records
    generate_temperature_file(
        file_path=test_file,
        location=location,
        temperatures=monthly_values,
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
        f"  Tmin (C)   TMax (C)\n"
        f"========================\n"
        f"2.0\t10.0\n"
        f"3.0\t12.0\n"
        f"5.0\t15.0\n"
        f"8.0\t18.0\n"
        f"12.0\t22.0\n"
        f"15.0\t26.0\n"
        f"18.0\t30.0\n"
        f"17.0\t28.0\n"
        f"14.0\t25.0\n"
        f"10.0\t20.0\n"
        f"5.0\t15.0\n"
        f"3.0\t12.0"
    )
    assert content == expected_content

def test_invalid_record_type(temp_dir):
    test_file = os.path.join(temp_dir, "test_invalid_temperature.tnx")
    
    # Test with invalid record type
    with pytest.raises(ValueError, match="record_type must be 1, 2, or 3"):
        generate_temperature_file(
            file_path=test_file,
            location="Invalid record type",
            temperatures=[(10.0, 20.0), (12.0, 22.0)],
            record_type=4  # Invalid record type
        )

def test_invalid_first_day_for_10day(temp_dir):
    test_file = os.path.join(temp_dir, "test_invalid_10day_temperature.tnx")
    
    # Test with invalid first day for 10-day records
    with pytest.raises(ValueError, match="first_day must be 1, 11, or 21 for 10-day records"):
        generate_temperature_file(
            file_path=test_file,
            location="Invalid first day for 10-day",
            temperatures=[(10.0, 20.0), (12.0, 22.0)],
            record_type=2,  # 10-daily
            first_day=5     # Invalid first day for 10-day records
        )

def test_invalid_first_day_for_monthly(temp_dir):
    test_file = os.path.join(temp_dir, "test_invalid_monthly_temperature.tnx")
    
    # Test with invalid first day for monthly records
    with pytest.raises(ValueError, match="first_day must be 1 for monthly records"):
        generate_temperature_file(
            file_path=test_file,
            location="Invalid first day for monthly",
            temperatures=[(10.0, 20.0), (12.0, 22.0)],
            record_type=3,  # Monthly
            first_day=2     # Invalid first day for monthly records
        )