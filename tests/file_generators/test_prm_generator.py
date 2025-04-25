import os
import pytest
import tempfile
from aquacrop.file_generators.LIST.prm_generator import generate_project_file
from unittest.mock import patch

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture
def mock_date_converter():
    with patch('aquacrop.file_generators.LIST.prm_generator.convertJulianToDateString') as mock:
        # Mock function to return a formatted date string
        mock.side_effect = lambda day_number: f"{day_number // 365 + 1901}-01-01"
        yield mock

def test_single_period_project_file(temp_dir, mock_date_converter):
    test_file = os.path.join(temp_dir, "test_single_period.pro")
    description = "Single period project file test"
    
    # Define a single simulation period
    periods = [
        {
            'year': 1,
            'first_day_sim': 36281,  # May 1, 2000 (example)
            'last_day_sim': 36515,   # December 21, 2000 (example)
            'first_day_crop': 36281, # May 1, 2000 (example)
            'last_day_crop': 36515,  # December 21, 2000 (example)
            'is_seeding_year': True,
            'cli_file': "Bru76-05.CLI",
            'tnx_file': "Bru76-05.TMP",
            'eto_file': "Bru76-05.ETo",
            'plu_file': "Bru76-05.PLU",
            'co2_file': "MaunaLoa.CO2",
            'cal_file': "1May.CAL",
            'cro_file': "Maize.CRO",
            'irr_file': "(None)",
            'man_file': "(None)",
            'sol_file': "Loam.SOL",
            'gwt_file': "(None)",
            'sw0_file': "(None)",
            'off_file': "(None)",
            'obs_file': "(None)"
        }
    ]
    
    # Generate the file
    generate_project_file(
        file_path=test_file,
        description=description,
        periods=periods
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check basic structure based on Table 2.23w-6
    assert description in content
    assert "1" in content  # Year number
    assert "cultivation" in content
    assert "Seeding" in content  # Should contain "Seeding" for seeding year
    # Check file references
    assert "Bru76-05.CLI" in content
    assert "Bru76-05.TMP" in content
    assert "Bru76-05.ETo" in content
    assert "Bru76-05.PLU" in content
    assert "MaunaLoa.CO2" in content
    assert "1May.CAL" in content
    assert "Maize.CRO" in content
    assert "(None)" in content  # For missing files
    assert "Loam.SOL" in content

def test_multiple_period_project_file(temp_dir, mock_date_converter):
    test_file = os.path.join(temp_dir, "test_multiple_period.prm")
    description = "5 years of alfalfa"
    
    # Define multiple simulation periods based on Table 2.23w-6
    periods = [
        {
            'year': 1,
            'first_day_sim': 36281,  # May 1, 2000
            'last_day_sim': 36515,   # December 21, 2000
            'first_day_crop': 36281, # May 1, 2000
            'last_day_crop': 36515,  # December 21, 2000
            'is_seeding_year': True,
            'cli_file': "Bru76-05.CLI",
            'tnx_file': "Bru76-05.TMP",
            'eto_file': "Bru76-05.ETo",
            'plu_file': "Bru76-05.PLU",
            'co2_file': "MaunaLoa.CO2",
            'cal_file': "1May.CAL",
            'cro_file': "alfalfa.CRO",
            'irr_file': "(None)",
            'man_file': "(None)",
            'sol_file': "Loam.SOL",
            'gwt_file': "(None)",
            'sw0_file': "(None)",
            'off_file': "(None)",
            'obs_file': "(None)"
        },
        {
            'year': 2,
            'first_day_sim': 36516,  # December 22, 2000
            'last_day_sim': 36845,   # November 16, 2001
            'first_day_crop': 36565, # February 9, 2001
            'last_day_crop': 36845,  # November 16, 2001
            'is_seeding_year': False,
            'cli_file': "Bru76-05.CLI",
            'tnx_file': "Bru76-05.TMP",
            'eto_file': "Bru76-05.ETo",
            'plu_file': "Bru76-05.PLU",
            'co2_file': "MaunaLoa.CO2",
            'cal_file': "1May.CAL",
            'cro_file': "alfalfa.CRO",
            'irr_file': "(None)",
            'man_file': "(None)",
            'sol_file': "Loam.SOL",
            'gwt_file': "(None)",
            'sw0_file': "KeepSWC",  # Keep soil water content from previous run
            'off_file': "(None)",
            'obs_file': "(None)"
        }
    ]
    
    # Generate the file
    generate_project_file(
        file_path=test_file,
        description=description,
        periods=periods
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check basic structure for multiple periods
    assert description in content
    assert "1" in content  # Year 1
    assert "2" in content  # Year 2
    assert "Seeding" in content  # First year should be seeding year 
    assert "Non-seeding" in content  # Second year should be non-seeding
    
    # Check first period details
    assert "36281" in content  # First day simulation (May 1, 2000)
    assert "36515" in content  # Last day simulation (December 21, 2000)
    
    # Check second period details
    assert "36516" in content  # First day second period
    assert "36845" in content  # Last day second period
    assert "36565" in content  # First day cropping period
    
    # Check for KeepSWC in second period
    assert "KeepSWC" in content
    assert "Keep soil water profile of previous run" in content

def test_project_file_with_various_file_states(temp_dir, mock_date_converter):
    test_file = os.path.join(temp_dir, "test_various_files.pro")
    description = "Project with various file states"
    
    # Define a period with some files present and some missing
    periods = [
        {
            'year': 1,
            'first_day_sim': 40000,
            'last_day_sim': 40100,
            'first_day_crop': 40000,
            'last_day_crop': 40100,
            'is_seeding_year': True,
            'cli_file': "Custom.CLI",
            'tnx_file': "Custom.TMP",
            'eto_file': "(None)",  # Missing ETo file
            'plu_file': "Custom.PLU",
            'co2_file': "(None)",  # Missing CO2 file
            'cal_file': "Custom.CAL",
            'cro_file': "Custom.CRO",
            'irr_file': "Custom.IRR",
            'man_file': "Custom.MAN",
            'sol_file': "(None)",  # Missing soil file
            'gwt_file': "Custom.GWT",
            'sw0_file': "Custom.SW0",
            'off_file': "Custom.OFF",
            'obs_file': "Custom.OBS"
        }
    ]
    
    # Generate the file
    generate_project_file(
        file_path=test_file,
        description=description,
        periods=periods
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check presence and absence of files
    assert "Custom.CLI" in content
    assert "Custom.TMP" in content
    assert "(None)" in content  # Missing files
    assert "Custom.PLU" in content
    assert "Custom.CAL" in content
    assert "Custom.CRO" in content
    assert "Custom.IRR" in content
    assert "Custom.MAN" in content
    assert "Custom.GWT" in content
    assert "Custom.SW0" in content
    assert "Custom.OFF" in content
    assert "Custom.OBS" in content

def test_project_file_path_handling(temp_dir, mock_date_converter):
    test_file = os.path.join(temp_dir, "test_paths.pro")
    description = "Project with different file paths"
    
    # Define a period with different paths for files
    periods = [
        {
            'year': 1,
            'first_day_sim': 40000,
            'last_day_sim': 40100,
            'first_day_crop': 40000,
            'last_day_crop': 40100,
            'is_seeding_year': True,
            # Various path formats should be handled correctly
            'cli_file': "Climate/Custom.CLI",
            'tnx_file': "Climate\\Custom.TMP",
            'eto_file': "ETo.dat",
            'plu_file': "/full/path/to/Rain.PLU",
            'co2_file': "C:\\CO2\\MaunaLoa.CO2",
            'cal_file': "../Calendar/Date.CAL",
            'cro_file': "..\\Crop\\Maize.CRO",
            'irr_file': "(None)",
            'man_file': "(None)",
            'sol_file': "(None)",
            'gwt_file': "(None)",
            'sw0_file': "(None)",
            'off_file': "(None)",
            'obs_file': "(None)"
        }
    ]
    
    # Generate the file
    generate_project_file(
        file_path=test_file,
        description=description,
        periods=periods
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check that paths are preserved
    assert "Climate/Custom.CLI" in content
    assert "Climate\\Custom.TMP" in content
    assert "ETo.dat" in content
    assert "/full/path/to/Rain.PLU" in content
    assert "MaunaLoa.CO2" in content
    assert "../Calendar/Date.CAL" in content
    assert "..\\Crop\\Maize.CRO" in content