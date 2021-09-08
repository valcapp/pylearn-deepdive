from datetime import datetime, timedelta, timezone

class TimeZone:
    """Class to create objects containing information about timezone"""
    def __init__(self, offset_hours:int=0, offset_minutes:int=0, tz_name:str='GMT')->None:
        offset = timedelta(hours=offset_hours, minutes=offset_minutes)
        self.tz = timezone(offset)
        self.name = tz_name
    
    def tell_time(self, dtime:datetime)->str:
        return (
            dtime.astimezone(self.tz).isoformat(sep=' ')
            + f" ({self.name})"
        )