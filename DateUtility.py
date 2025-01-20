from datetime import datetime
import pytz

class DateUtility:
   @staticmethod
   def bucket(date: datetime) -> str:
       """
       Bucket a datetime by reducing precision to the minute.
       Downsamples datetime to minute precision in ISO 8601 format.
       
       Args:
           date: datetime object to bucket
           
       Returns:
           ISO 8601 datetime string with minute precision
       """
       return date.strftime("%Y-%m-%dT%H:%M:00.000")
