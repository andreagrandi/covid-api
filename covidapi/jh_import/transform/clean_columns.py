def clean_extra_whitespace(record):
    """
    Fix column names like '\ufeffFIPS'
    """
    return {k.strip('\ufeff'):v for k, v in record.items()}
