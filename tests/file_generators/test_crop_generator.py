import os
import pytest
import tempfile
from aquacrop.file_generators.DATA.crop_generator import generate_crop_file
from aquacrop.constants import Constants

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

# Base parameter set with all required parameters
@pytest.fixture
def complete_crop_params():
    """Provides a complete set of parameters that all tests can start with"""
    return {
        # Basic crop classification
        'crop_type': 2,  # fruit/grain producing crop
        'is_sown': True,
        'cycle_determination': 0,  # calendar days
        'adjust_for_eto': True,
        
        # Temperature parameters
        'base_temp': 5.5,
        'upper_temp': 30.0,
        'gdd_cycle_length': 1920,
        'dormancy_eto_threshold': 600,
        
        # Water stress parameters
        'p_upper_canopy': 0.25,
        'p_lower_canopy': 0.60,
        'shape_canopy': 3.0,
        'p_upper_stomata': 0.50,
        'shape_stomata': 3.0,
        'p_upper_senescence': 0.85,
        'shape_senescence': 3.0,
        'p_upper_pollination': 0.90,
        'aeration_stress_threshold': 5,
        
        # Fertility stress parameters
        'fertility_stress_calibration': 50,
        'shape_fertility_canopy_expansion': 2.35,
        'shape_fertility_max_canopy': 0.79,
        'shape_fertility_water_productivity': -0.16,
        'shape_fertility_decline': 6.26,
        
        # Temperature stress parameters
        'cold_stress_for_pollination': 10,
        'heat_stress_for_pollination': 40,
        'minimum_growing_degrees_pollination': 8.0,
        
        # Salinity stress parameters
        'salinity_threshold_ece': 2,
        'salinity_max_ece': 16,
        'salinity_shape_factor': -9,
        'salinity_stress_cc': 25,
        'salinity_stress_stomata': 100,
        
        # Transpiration parameters
        'kc_max': 1.15,
        'kc_decline': 0.050,
        
        # Rooting parameters
        'min_rooting_depth': 0.30,
        'max_rooting_depth': 1.50,
        'root_expansion_shape': 15,
        'max_water_extraction_top': 0.048,
        'max_water_extraction_bottom': 0.012,
        'soil_evaporation_reduction': 60,
        
        # Canopy development parameters
        'canopy_cover_per_seedling': 6.5,
        'canopy_regrowth_size': 19.38,
        'plant_density': 75000,
        'max_canopy_cover': 0.96,
        'canopy_growth_coefficient': 0.16500,
        'canopy_thinning_years': 9,
        'canopy_thinning_shape': 0.50,
        'canopy_decline_coefficient': 0.12750,
        
        # Crop cycle parameters (Calendar days)
        'days_emergence': 7,
        'days_max_rooting': 65,
        'days_senescence': 91,
        'days_maturity': 110,
        'days_flowering': 60,
        'days_flowering_length': 15,
        'days_crop_determinancy': 1,
        'days_hi_start': 50,
        
        # Crop cycle parameters (Growing degree days)
        'gdd_emergence': 100,
        'gdd_max_rooting': 1000,
        'gdd_senescence': 1600,
        'gdd_maturity': 1920,
        'gdd_flowering': 900,
        'gdd_flowering_length': 150,
        'cgc_gdd': 0.012000,
        'cdc_gdd': 0.006000,
        'gdd_hi_start': 1000,
        
        # Biomass and yield parameters
        'water_productivity': 33.7,
        'water_productivity_yield_formation': 100,
        'co2_response_strength': 50,
        'harvest_index': 0.48,
        'water_stress_hi_increase': -9,
        'veg_growth_impact_hi': -9.0,
        'stomatal_closure_impact_hi': -9.0,
        'max_hi_increase': -9,
        'dry_matter_content': 20,
        
        # Perennial crop parameters
        'is_perennial': False,
        'first_year_min_rooting': 0.30,
        'assimilate_transfer': 1,
        'assimilate_storage_days': 100,
        'assimilate_transfer_percent': 65,
        'root_to_shoot_transfer_percent': 60,
        
        # Crop calendar for perennials
        'restart_type': 13,
        'restart_window_day': 1,
        'restart_window_month': 4,
        'restart_window_length': 120,
        'restart_gdd_threshold': 20.0,
        'restart_days_required': 8,
        'restart_occurrences': 2,
        'end_type': 63,
        'end_window_day': 31,
        'end_window_month': 10,
        'end_window_years_offset': 0,
        'end_window_length': 60,
        'end_gdd_threshold': 10.0,
        'end_days_required': 8,
        'end_occurrences': 1
    }

def test_crop_file_basic_parameters(temp_dir, monkeypatch, complete_crop_params):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_crop_basic.cro")
    description = "a generic crop"
    
    # Generate the file
    generate_crop_file(
        file_path=test_file,
        description=description,
        params=complete_crop_params
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check basic parameters
    assert description in content
    assert "7.1       : AquaCrop Version (August 2023)" in content
    assert "2         : fruit/grain producing crop" in content
    assert "1         : Crop is sown" in content
    assert "0         : Determination of crop cycle : by calendar days" in content
    assert "1         : Soil water depletion factors (p) are adjusted by ETo" in content
    assert "5.5       : Base temperature (degC) below which crop development does not progress" in content
    assert "30.0       : Upper temperature (degC) above which crop development no longer increases" in content
    assert "0.25      : Soil water depletion factor for canopy expansion (p-exp) - Upper threshold" in content
    assert "0.60      : Soil water depletion factor for canopy expansion (p-exp) - Lower threshold" in content
    assert "3.0       : Shape factor for water stress coefficient for canopy expansion (0.0 = straight line)" in content
    assert "0.50      : Soil water depletion fraction for stomatal control (p - sto) - Upper threshold" in content

def test_crop_file_annual_crop(temp_dir, monkeypatch, complete_crop_params):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_crop_annual.cro")
    description = "Annual crop (maize) example"
    
    # Modify base params for an annual crop like maize
    annual_params = complete_crop_params.copy()
    annual_params.update({
        'base_temp': 8.0,  # Specific to maize
        'max_rooting_depth': 1.50,
        'plant_density': 75000,
        'max_canopy_cover': 0.96,
        'days_emergence': 7,
        'days_max_rooting': 65,
        'days_senescence': 91,
        'days_maturity': 110,
        'days_flowering': 60,
        'days_flowering_length': 15,
        'days_crop_determinancy': 1,
        'water_productivity': 33.7,
        'harvest_index': 0.48,
        'is_perennial': False
    })
    
    # Generate the file
    generate_crop_file(
        file_path=test_file,
        description=description,
        params=annual_params
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check annual crop specific parameters
    assert description in content
    assert "2         : fruit/grain producing crop" in content
    assert "8.0       : Base temperature (degC)" in content
    assert "0.30      : Minimum effective rooting depth (m)" in content
    assert "1.50      : Maximum effective rooting depth (m)" in content
    assert "75000      : Number of plants per hectare" in content
    assert "0.96      : Maximum canopy cover (CCx) in fraction soil cover" in content
    assert "7         : Calendar Days: from sowing to emergence" in content
    assert "65         : Calendar Days: from sowing to maximum rooting depth" in content
    assert "91         : Calendar Days: from sowing to start senescence" in content
    assert "110         : Calendar Days: from sowing to maturity (length of crop cycle)" in content
    assert "60         : Calendar Days: from sowing to flowering" in content
    assert "15         : Length of the flowering stage (days)" in content
    assert "1         : Crop determinancy linked with flowering" in content
    assert "33.7       : Water Productivity normalized for ETo and CO2 (WP*) (gram/m2)" in content
    assert "48         : Reference Harvest Index (HIo) (%)" in content
    assert "0         : Crop is not sown in 1st year (for perennials)" in content

def test_crop_file_perennial_crop(temp_dir, monkeypatch, complete_crop_params):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_crop_perennial.cro")
    description = "Perennial crop (alfalfa) example"
    
    # Modify base params for a perennial crop like alfalfa
    perennial_params = complete_crop_params.copy()
    perennial_params.update({
        'crop_type': 4,  # forage crop
        'base_temp': 4.0,
        'upper_temp': 35.0,
        'dormancy_eto_threshold': 800,  # Increase from default 600
        'max_rooting_depth': 2.50,
        'plant_density': 250000,
        'max_canopy_cover': 0.90,
        'days_emergence': 7,
        'days_max_rooting': 50,
        'water_productivity': 15.0,
        'is_perennial': True,
        'first_year_min_rooting': 0.30,
        'assimilate_transfer': 1,
        'assimilate_storage_days': 100,
        'assimilate_transfer_percent': 65,
        'root_to_shoot_transfer_percent': 60
    })
    
    # Generate the file
    generate_crop_file(
        file_path=test_file,
        description=description,
        params=perennial_params
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check perennial crop specific parameters
    assert description in content
    assert "4         : forage crop" in content
    assert "800         : Sum(ETo) during dormant period to be exceeded before crop is permanently wilted" in content
    assert "2.50      : Maximum effective rooting depth (m)" in content
    assert "19.38      : Canopy size of individual plant (re-growth) at 1st day (cm2)" in content
    assert "250000      : Number of plants per hectare" in content
    assert "0.90      : Maximum canopy cover (CCx) in fraction soil cover" in content
    assert "9         : Number of years at which CCx declines to 90 % of its value due to self-thinning - for Perennials" in content
    assert "1         : Crop is sown in 1st year (for perennials)" in content
    assert "1         : Transfer of assimilates from above ground parts to root system is considered" in content
    assert "100         : Number of days at end of season during which assimilates are stored in root system" in content
    assert "65         : Percentage of assimilates transferred to root system at last day of season" in content
    assert "60         : Percentage of stored assimilates transferred to above ground parts in next season" in content
    
    # Check internal crop calendar for perennials
    assert "Internal crop calendar" in content
    assert "========================================================" in content
    assert "13         : The Restart of growth is generated by Growing-degree days" in content
    assert "1         : First Day for the time window (Restart of growth)" in content
    assert "4         : First Month for the time window (Restart of growth)" in content
    assert "120         : Length (days) of the time window (Restart of growth)" in content
    assert "20.0       : Threshold for the Restart criterion: Growing-degree days" in content
    assert "8         : Number of successive days for the Restart criterion" in content
    assert "2         : Number of occurrences before the Restart criterion applies" in content
    assert "63         : The End of growth is generated by Growing-degree days" in content
    assert "31         : Last Day for the time window (End of growth)" in content
    assert "10         : Last Month for the time window (End of growth)" in content

def test_crop_file_gdd_based_crop(temp_dir, monkeypatch, complete_crop_params):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_crop_gdd.cro")
    description = "GDD-based crop example"
    
    # Modify base params for a crop using growing degree days
    gdd_params = complete_crop_params.copy()
    gdd_params.update({
        'cycle_determination': 1,  # growing degree-days
        'base_temp': 8.0,
        'upper_temp': 30.0,
        'gdd_cycle_length': 1920,
        'max_canopy_cover': 0.90,
        'gdd_emergence': 100,
        'gdd_max_rooting': 1000,
        'gdd_senescence': 1600,
        'gdd_maturity': 1920,
        'gdd_flowering': 900,
        'gdd_flowering_length': 150,
        'cgc_gdd': 0.012000,
        'cdc_gdd': 0.006000,
        'gdd_hi_start': 1000,
        'water_productivity': 18.0,
        'harvest_index': 0.45
    })
    
    # Generate the file
    generate_crop_file(
        file_path=test_file,
        description=description,
        params=gdd_params
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check GDD-based crop specific parameters
    assert description in content
    assert "1         : Determination of crop cycle : by growing degree-days" in content
    assert "1920         : Total length of crop cycle in growing degree-days" in content
    
    # Check GDD-based development parameters
    assert "100         : GDDays: from sowing to emergence" in content
    assert "1000         : GDDays: from sowing to maximum rooting depth" in content
    assert "1600         : GDDays: from sowing to start senescence" in content
    assert "1920         : GDDays: from sowing to maturity (length of crop cycle)" in content
    assert "900         : GDDays: from sowing to flowering" in content
    assert "150         : Length of the flowering stage (growing degree days)" in content
    assert "0.012000  : CGC for GGDays: Increase in canopy cover (in fraction soil cover per growing-degree day)" in content
    assert "0.006000  : CDC for GGDays: Decrease in canopy cover (in fraction per growing-degree day)" in content
    assert "1000         : GDDays: building-up of Harvest Index during yield formation" in content

def test_crop_file_stress_responses(temp_dir, monkeypatch, complete_crop_params):
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_crop_stress.cro")
    description = "Crop with custom stress responses"
    
    # Modify base params for a crop with specific stress responses
    stress_params = complete_crop_params.copy()
    stress_params.update({
        'fertility_stress_calibration': 70,
        'shape_fertility_canopy_expansion': 2.16,
        'shape_fertility_max_canopy': 0.79,
        'shape_fertility_water_productivity': 1.67,
        'shape_fertility_decline': 1.67,
        'cold_stress_for_pollination': 8,
        'heat_stress_for_pollination': 40,
        'minimum_growing_degrees_pollination': 11.1,
        'salinity_threshold_ece': 2,
        'salinity_max_ece': 12,
        'salinity_stress_cc': 25,
        'salinity_stress_stomata': 100,
        'water_stress_hi_increase': 5,
        'veg_growth_impact_hi': 10.0,
        'stomatal_closure_impact_hi': 8.0,
        'max_hi_increase': 15
    })
    
    # Generate the file
    generate_crop_file(
        file_path=test_file,
        description=description,
        params=stress_params
    )
    
    # Check if file exists
    assert os.path.isfile(test_file)
    
    # Read and verify the content
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Check stress response parameters
    assert description in content
    assert "70         : Considered soil fertility stress for calibration of stress response (%)" in content
    assert "2.16      : Shape factor for the response of canopy expansion to soil fertility stress" in content
    assert "0.79      : Shape factor for the response of maximum canopy cover to soil fertility stress" in content
    assert "1.67      : Shape factor for the response of crop Water Productivity to soil fertility stress" in content
    assert "1.67      : Shape factor for the response of decline of canopy cover to soil fertility stress" in content
    assert "8         : Minimum air temperature below which pollination starts to fail (cold stress) (degC)" in content
    assert "40         : Maximum air temperature above which pollination starts to fail (heat stress) (degC)" in content
    assert "11.1       : Minimum growing degrees required for full crop transpiration (degC - day)" in content
    assert "2         : Electrical Conductivity of soil saturation extract at which crop starts to be affected by soil salinity (dS/m)" in content
    assert "12         : Electrical Conductivity of soil saturation extract at which crop can no longer grow (dS/m)" in content
    assert "25         : Calibrated distortion (%) of CC due to salinity stress (Range: 0 (none) to +100 (very strong))" in content
    assert "100         : Calibrated response (%) of stomata stress to ECsw (Range: 0 (none) to +200 (extreme))" in content
    assert "5         : Possible increase (%) of HI due to water stress before flowering" in content
    assert "10.0       : Impact of HI of restricted vegetative growth during yield formation" in content
    assert "8.0       : Effect of HI of stomatal closure during yield formation" in content
    assert "15         : Allowable maximum increase (%) of specified HI" in content

def test_crop_file_missing_key_error(temp_dir, monkeypatch):
    """Test that the generator raises a KeyError for missing parameters"""
    # Mock the Constants
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_NUMBER", "7.1")
    monkeypatch.setattr(Constants, "AQUACROP_VERSION_DATE", "August 2023")
    
    test_file = os.path.join(temp_dir, "test_crop_exception.cro")
    description = "Crop with missing parameters"
    
    # Create incomplete parameters 
    incomplete_params = {
        'crop_type': 1,
        'is_sown': True,
        # Missing many required parameters
    }
    
    # This should raise a KeyError since params are accessed directly without validation
    with pytest.raises(KeyError):
        generate_crop_file(
            file_path=test_file,
            description=description,
            params=incomplete_params
        )
    
    # The file should not exist due to the exception
    assert not os.path.isfile(test_file)