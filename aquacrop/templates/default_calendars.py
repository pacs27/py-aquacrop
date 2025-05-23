from aquacrop import Calendar

# Ottawa May 21 calendar based on test reference
may_21_calendar = Calendar(
    name="May21",
    description="Onset: 21 May - spring alfalfa seeding",
    onset_mode=0,  # fixed date
    day_number=141  # day 141 of the year (May 21)
)

# Calendars for different growing periods
early_spring_calendar = Calendar(
    name="EarlySpring",
    description="Onset: 1 April - early spring planting",
    onset_mode=0,  # fixed date
    day_number=91  # day 91 of the year (April 1)
)

late_spring_calendar = Calendar(
    name="LateSpring",
    description="Onset: 1 June - late spring planting",
    onset_mode=0,  # fixed date
    day_number=152  # day 152 of the year (June 1)
)

summer_calendar = Calendar(
    name="Summer",
    description="Onset: 1 July - summer planting",
    onset_mode=0,  # fixed date
    day_number=182  # day 182 of the year (July 1)
)

# Rainfall dependent planting
rainfall_dependent = Calendar(
    name="RainfallDependent",
    description="Onset depends on 20mm cumulative rainfall",
    onset_mode=1,  # generated by criteria
    window_start_day=91,  # Start window on April 1
    window_length=90,  # 90-day window
    criterion_number=1,  # Criterion 1: Cumulative rainfall since start of time period
    criterion_value=20.0,  # 20mm of rainfall
    successive_days=1,  
    occurrences=1
)

# Temperature-based planting
temperature_dependent = Calendar(
    name="TemperatureDependent",
    description="Onset depends on average air temperature threshold",
    onset_mode=1,  # generated by criteria
    window_start_day=61,  # Start window on March 1
    window_length=120,  # 120-day window
    criterion_number=12,  # Criterion 12: Average air temperature threshold
    criterion_value=15.0,  # 15°C average temperature
    successive_days=5,  # Need 5 successive days
    occurrences=1
)