from datetime import datetime, timedelta

async def convert_datetime_for_influx(year: int, month: int, day: int, hour: int, minutes: int) -> dict:
    try:
        date_obj = datetime(year, month, day, hour, minutes)
        new_date_obj = date_obj - timedelta(hours=2)
        datetime_dict = {
            "year": f"{new_date_obj.year}",
            "month": f"{new_date_obj:%m}",
            "day": f"{new_date_obj:%d}",
            "hour": f"{new_date_obj:%H}",
            "minutes": f"{new_date_obj:%M}"
        }
        
        return datetime_dict
    except Exception as e:
        raise Exception("Error durning converting datetime.")