from constants import (
    FPATH, # file path
    TPNAME, # tuplename
    TPFIELDS, # tuplename
    DTYPES, # data types
    MASK, # bool filter to compress imputs
    # COMBINE, # which other configs to combine
)
from utilparse import iso_datetime

cfg_employment = {
    FPATH: 'data/employment.csv',
    DTYPES: (str,        str,      str,     str),
        # (employer, department, employee_id, ssn)
}

cfg_personal_info = {
    FPATH: 'data/personal_info.csv',
    DTYPES:  (str,    str,       str,       str,     str)
            # (ssn, first_name, last_name, gender, language
}

cfg_update_status = {
    FPATH: 'data/update_status.csv',
    DTYPES: ( str,  iso_datetime,   iso_datetime)
            # (ssn, last_updated,    created)
}

cfg_vehicles = {
    FPATH: 'data/vehicles.csv',
    DTYPES: ( str,   str,           str,         str)
            # (ssn, vehicle_make, vehicle_model, model_year)
}

configs = (
    cfg_employment,
    cfg_personal_info,
    cfg_update_status,
    cfg_vehicles
)

# cfg_employee = {
#     TPNAME: 'Employee',
#     COMBINE: configs,
# }