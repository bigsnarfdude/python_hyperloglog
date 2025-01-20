from datetime import datetime
import pytz

class DateUtility:
   @staticmethod
   def bucket(date: datetime) -> str:
       """
         
         Object uses downsampling method to create metadata from each 
         EventType log record. Parsing the ISO 8601 
         datetime stamp to the minute means downsampling aka reducing 
         precision.
         
         Bucketing
         A family of aggregations that build buckets, where each bucket 
         is associated with a key and an EventType criterion. When the 
         aggregation is executed, all the buckets criteria are evaluated 
         on every EventType in the context and when a criterion matches, 
         the EventType is considered to "fall in" the relevant bucket. 
         By the end of the aggregation process, we’ll end up with a 
         list of buckets - each one with a set of EventTypes that 
         "belong" to it.
       
       Args:
           date: datetime object to bucket
           
       Returns:
           ISO 8601 datetime string with minute precision
       """
       return date.strftime("%Y-%m-%dT%H:%M:00.000")
