# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from autoslug.fields import AutoSlugField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.gis import admin as geoadmin
import uuid

def _createHash():
    uid = uuid.uuid4()
    return uid.hex

def GPX_Folder(instance, filename):
    return "uploaded_gpx_files/%s" % (filename)

class mdlTrack(models.Model):
    
    TRACK_TYPES = (
        ('gpx', _('GPX')),
        ('klm', _('KLM')), 
        ('fir', _('FIT')),
    )
    
    name = models.CharField(max_length=4000, help_text=_('GPS name of track.'))
    description = models.TextField(null=True, blank=True, help_text=_('User description of track.'))
    type= models.CharField(max_length=3, choices=TRACK_TYPES, blank=True, null=True, help_text=_('Track type.'))
    creation_user = models.ForeignKey(User, db_index=True)
    slug = AutoSlugField(populate_from='name', always_update=False, unique_with='name', null=True, blank=True, db_index=True)
    hash_code = models.UUIDField(null=True, blank=True,db_index=True, default=uuid.uuid4, editable=False)
    deleted = models.BooleanField(default=False, help_text=_('Is the track deleted?'))
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'track'
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'
        ordering = ('name',)
        
class mdlGPXFile(models.Model):
    track = models.ForeignKey(mdlTrack, db_index=True)
    title = models.CharField("Title", max_length=4000,blank=True, null=True)
    gpx_file = models.FileField(upload_to=GPX_Folder, blank=True, null=True)
    version = models.CharField("XML Version", max_length=10,blank=True, null=True)
    creator = models.CharField("Creator", max_length=255,blank=True, null=True)
    name = models.CharField("The name of the GPX file.", max_length=255,blank=True, null=True)
    description = models.CharField("A description of the contents of the GPX file.", max_length=4000,blank=True, null=True)	   
    time = models.DateTimeField("The creation date of the file.",blank=True, null=True)
    keywords = models.TextField("Keywords associated with the file.", blank=True, null=True)    
    bound_min = models.PointField("Minimum coordinates which describe the extent of the coordinates in the file.", blank=True, null=True)
    bound_max = models.PointField("Maximum coordinates which describe the extent of the coordinates in the file.", blank=True, null=True)
    author_name= models.CharField("The person or organization who created the GPX file.", max_length=10,blank=True, null=True)
    author_email= models.EmailField("GPX author email", max_length=10,blank=True, null=True)
    author_link= models.URLField("GPX author link", max_length=255,blank=True, null=True)
    author_link_text = models.CharField("Text of the GPX author link.", max_length=255,blank=True, null=True)
    author_link_type = models.CharField("Mime type of GPX author link", max_length=100,blank=True, null=True)   
    copyright_author = models.CharField("Copyright holder.", max_length=255,blank=True, null=True)
    copyright_year = models.CharField("Year of copyright.", max_length=4,blank=True, null=True)
    copyright_license= models.URLField("Link to external file containing license text.", max_length=255,blank=True, null=True)
    extensions = models.TextField("Extensions.", blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'GPX_File'
        verbose_name = 'GPX File'
        verbose_name_plural = 'GPX Files'


class mdlGPXFileLinks(models.Model):   
    gpx_file = models.ForeignKey(mdlGPXFile)
    link = models.URLField("URLs associated with the location described in the file.", max_length=255,blank=True, null=True)  
    link_text = models.CharField("Text of the GPX location link.", max_length=255,blank=True, null=True)
    link_type = models.CharField("Mime type of GPX location link", max_length=100,blank=True, null=True)  

    class Meta:
        db_table = 'GPX_File_Link'
        verbose_name = 'GPX File Link'
        verbose_name_plural = 'GPX File Links'


class mdlGPXTrack(models.Model):    
    gpx_file = models.ForeignKey(mdlGPXFile)
    name = models.CharField("GPS name of track.", max_length=10,blank=True, null=True)
    comment = models.CharField("GPS comment for track.", max_length=4000,blank=True, null=True)
    description = models.CharField("User description of track.", max_length=4000,blank=True, null=True)
    source = models.CharField("Source of data", max_length=50,blank=True, null=True)	 
    number = models.DecimalField("GPS track number.", max_digits = 10,  decimal_places = 2, default = 0)
    type = models.CharField("Type (classification) of track.", max_length=255,blank=True, null=True)
    extensions = models.TextField("Extensions.", blank=True, null=True)	
    trackLine= models.MultiLineStringField(blank=True, null=True)
#    objects = models.GeoManager()

    class Meta:
        db_table = 'GPX_Track'
        verbose_name = 'GPX Track'
        verbose_name_plural = 'GPX Tracks'

class mdlGPXTrackLinks(models.Model):   
    gpx_track = models.ForeignKey(mdlGPXTrack)
    link = models.URLField("Links to external information about track.", max_length=255,blank=True, null=True)  
    link_text = models.CharField("Text of the GPX track link.", max_length=255,blank=True, null=True)
    link_type = models.CharField("Mime type of GPX track link", max_length=100,blank=True, null=True)  

    class Meta:
        db_table = 'GPX_Track_Link'
        verbose_name = 'GPX Track Link'
        verbose_name_plural = 'GPX Track Links'

class mdlGPXTrackSegment(models.Model):    
    gpx_track = models.ForeignKey(mdlGPXTrack)	
    extensions = models.TextField("Extensions.", blank=True, null=True)
    segmentLine= models.LineStringField(blank=True, null=True)

    class Meta:
        db_table = 'GPX_Track_Segment'
        verbose_name = 'GPX Track Segment'
        verbose_name_plural = 'GPX Track Segments'


class mdlGPXTrackSegmentPoint(models.Model):

    GPS_FIX = (
        ('none', 'none'),
        ('2d', '2d'),
        ('3d', '3d'),
        ('dgps', 'dgps'),
        ('pps', 'pps'),
    )

    gpx_track_segment = models.ForeignKey(mdlGPXTrackSegment,blank=True, null=True)
    point = models.PointField("The latitude and longitude of the point.")
    elevation = models.FloatField("Elevation (in meters) of the point",blank=True, null=True)
    time = models.DateTimeField("Creation/modification timestamp for element (UTC)",blank=True, null=True)
    magnetic_variation = models.FloatField("Magnetic variation (in degrees) at the point",blank=True, null=True)
    geoid_height  = models.FloatField("Height (in meters) of geoid (mean sea level) above WGS84 earth ellipsoid. ",blank=True, null=True) 
    name = models.CharField("The GPS name of the waypoint.", max_length=255,blank=True, null=True)
    comment = models.CharField("GPS waypoint comment.", max_length=500,blank=True, null=True)
    description = models.CharField("A text description of the element.", max_length=500,blank=True, null=True)
    source = models.CharField("Source of data.", max_length=50,blank=True, null=True)
    symbol = models.CharField("Text of GPS symbol name.", max_length=50,blank=True, null=True)
    type = models.CharField("Type (classification) of the waypoint", max_length=50,blank=True, null=True)
    type_of_gpx_fix = models.CharField("Type of GPX fix.", choices=GPS_FIX, max_length=4,blank=True, null=True)
    satellites = models.DecimalField("Number of satellites used to calculate the GPX fix.", max_digits = 6,  decimal_places = 0,blank=True, null=True)
    horizontal_dilution= models.FloatField("Horizontal dilution of precision.",blank=True, null=True) 
    vertical_dilution= models.FloatField("Vertical dilution of precision.",blank=True, null=True) 
    position_dilution= models.FloatField("Position dilution of precision.",blank=True, null=True) 
    age_of_dgps_data = models.DecimalField("Number of seconds since last DGPS update.", max_digits = 10,  decimal_places = 2 ,blank=True, null=True)
    dgps_id = models.DecimalField("ID of DGPS station used in differential correction.", max_digits = 10,  decimal_places = 2 ,blank=True, null=True)
    extensions = models.TextField("Extensions.", blank=True, null=True)
    heart_rate = models.DecimalField("HR represents the heart rate in beats per minute.", max_digits = 3,  decimal_places = 0 ,blank=True, null=True)
    cadence = models.DecimalField("Cadence represents the cadence in revolutions per minute..", max_digits = 6,  decimal_places = 0 ,blank=True, null=True)
    temperature = models.FloatField("Temp represents the temperature in degrees celcius",blank=True, null=True) 
    distance = models.FloatField("Distance in meters as measured by GPS or wheel sensor",blank=True, null=True) 
    altitude = models.DecimalField("Altitude in meters", max_digits = 10,  decimal_places = 2 ,blank=True, null=True)
    sea_level_pressure = models.DecimalField("Sea level pressure", max_digits = 10,  decimal_places = 2 ,blank=True, null=True)
    speed = models.FloatField("Horitzontal Speed in meters per second (m/s)", blank=True, null=True)
    vertical_speed = models.FloatField("Vertical Speed in meters per second (m/s)", blank=True, null=True)
    energy = models.FloatField("Energy in Calories", blank=True, null=True)

    class Meta:
        db_table = 'GPX_Track_Segment_Point'
        verbose_name = 'GPX Track Segment Point'
        verbose_name_plural = 'GPX Track Segment Points'


class mdlGPXTrackSegmentPointLinks(models.Model):   
    gpx_track_segment_point = models.ForeignKey(mdlGPXTrackSegmentPoint)
    link = models.URLField("Links to external information about track.", max_length=255,blank=True, null=True)  
    link_text = models.CharField("Text of the GPX track link.", max_length=255,blank=True, null=True)
    link_type = models.CharField("Mime type of GPX track link", max_length=100,blank=True, null=True)  

    class Meta:
        db_table = 'GPX_Track_Segment_Point_Link'
        verbose_name = 'GPX Track Segment Point Link'
        verbose_name_plural = 'GPX Track Segment Point Links'

class mdlGPXWaypoint(models.Model):
    
    GPS_FIX = (
        ('none', 'none'),
        ('2d', '2d'),
        ('3d', '3d'),
        ('dgps', 'dgps'),
        ('pps', 'pps'),
    )

    gpx_file = models.ForeignKey(mdlGPXFile)
    point = models.PointField("The latitude and longitude of the point.")
    elevation = models.FloatField("Elevation (in meters) of the point",blank=True, null=True)
    time = models.DateTimeField("Creation/modification timestamp for element (UTC)",blank=True, null=True)
    magnetic_variation = models.FloatField("Magnetic variation (in degrees) at the point",blank=True, null=True)
    geoid_height  = models.FloatField("Height (in meters) of geoid (mean sea level) above WGS84 earth ellipsoid. ",blank=True, null=True) 
    name = models.CharField("The GPS name of the waypoint.", max_length=255,blank=True, null=True)
    comment = models.CharField("GPS waypoint comment.", max_length=500,blank=True, null=True)
    description = models.CharField("A text description of the element.", max_length=500,blank=True, null=True)
    source = models.CharField("Source of data.", max_length=50,blank=True, null=True)
    symbol = models.CharField("Text of GPS symbol name.", max_length=50,blank=True, null=True)
    type = models.CharField("Type (classification) of the waypoint", max_length=50,blank=True, null=True)
    type_of_gpx_fix = models.CharField("Type of GPX fix.", choices=GPS_FIX, max_length=4,blank=True, null=True)
    satellites = models.DecimalField("Number of satellites used to calculate the GPX fix.", max_digits = 6,  decimal_places = 0,blank=True, null=True)
    horizontal_dilution= models.FloatField("Horizontal dilution of precision.",blank=True, null=True) 
    vertical_dilution= models.FloatField("Vertical dilution of precision.",blank=True, null=True) 
    position_dilution= models.FloatField("Position dilution of precision.",blank=True, null=True) 
    age_of_dgps_data = models.DecimalField("Number of seconds since last DGPS update.", max_digits = 10,  decimal_places = 2 ,blank=True, null=True)
    dgps_id = models.DecimalField("ID of DGPS station used in differential correction.", max_digits = 10,  decimal_places = 2 ,blank=True, null=True)
    extensions = models.TextField("Extensions.", blank=True, null=True)
    heart_rate = models.DecimalField("HR represents the heart rate in beats per minute.", max_digits = 3,  decimal_places = 0 ,blank=True, null=True)
    cadence = models.DecimalField("Cadence represents the cadence in revolutions per minute..", max_digits = 6,  decimal_places = 0 ,blank=True, null=True)
    temperature = models.FloatField("Temp represents the temperature in degrees celcius",blank=True, null=True) 
    distance = models.FloatField("Distance in meters as measured by GPS or wheel sensor",blank=True, null=True) 
    altitude = models.DecimalField("Altitude in meters", max_digits = 10,  decimal_places = 2 ,blank=True, null=True)
    sea_level_pressure = models.DecimalField("Sea level pressure", max_digits = 10,  decimal_places = 2 ,blank=True, null=True)
    speed = models.FloatField("Horitzontal Speed in meters per second (m/s)", blank=True, null=True)
    vertical_speed = models.FloatField("Vertical Speed in meters per second (m/s)", blank=True, null=True)
    energy = models.FloatField("Energy in Calories", blank=True, null=True)

    class Meta:
        db_table = 'GPX_Waypoint'
        verbose_name = 'GPX Waypoint'
        verbose_name_plural = 'GPX Waypoints'


class mdlGPXWaypointLinks(models.Model):   
    gpx_waypoint = models.ForeignKey(mdlGPXWaypoint)   
    link = models.URLField("Links to external information about Waypoint.", max_length=255,blank=True, null=True)  
    link_text = models.CharField("Text of the GPX Waypoint link.", max_length=255,blank=True, null=True)
    link_type = models.CharField("Mime type of GPX Waypoint link", max_length=100,blank=True, null=True)  

    class Meta:
        db_table = 'GPX_Waypoint_Link'
        verbose_name = 'GPX Waypoint Link'
        verbose_name_plural = 'GPX Waypoint Links'


class mdlGPXRoute(models.Model):    
    gpx_file = models.ForeignKey(mdlGPXFile)
    name = models.CharField("GPS name of route.", max_length=10,blank=True, null=True)
    comment = models.CharField("GPS comment for route.", max_length=4000,blank=True, null=True)
    description = models.CharField("User description of route.", max_length=4000,blank=True, null=True)
    source = models.CharField("Source of data", max_length=50,blank=True, null=True)	 
    number = models.DecimalField("GPS route  number.", max_digits = 10,  decimal_places = 2, default = 0 )
    type = models.CharField("Type (classification) of route .", max_length=255,blank=True, null=True)
    extensions = models.TextField("Extensions.", blank=True, null=True)	
    trackLine= models.MultiLineStringField(blank=True, null=True)
#    objects = models.GeoManager()

    class Meta:
        db_table = 'GPX_Route'
        verbose_name = 'GPX Route'
        verbose_name_plural = 'GPX Routes'

class mdlGPXRouteLinks(models.Model):   
    gpx_route = models.ForeignKey(mdlGPXRoute)
    link = models.URLField("Links to external information about route.", max_length=255,blank=True, null=True)  
    link_text = models.CharField("Text of the GPX route link.", max_length=255,blank=True, null=True)
    link_type = models.CharField("Mime type of GPX route link", max_length=100,blank=True, null=True)  

    class Meta:
        db_table = 'GPX_Route_Link'
        verbose_name = 'GPX Route Link'
        verbose_name_plural = 'GPX Route Links'


class mdlGPXRoutePoint(models.Model):
    
    GPS_FIX = (
        ('none', 'none'),
        ('2d', '2d'),
        ('3d', '3d'),
        ('dgps', 'dgps'),
        ('pps', 'pps'),
    )

    gpx_route = models.ForeignKey(mdlGPXRoute)
    point = models.PointField("The latitude and longitude of the point.")
    elevation = models.FloatField("Elevation (in meters) of the point",blank=True, null=True)
    time = models.DateTimeField("Creation/modification timestamp for element (UTC)",blank=True, null=True)
    magnetic_variation = models.FloatField("Magnetic variation (in degrees) at the point",blank=True, null=True)
    geoid_height  = models.FloatField("Height (in meters) of geoid (mean sea level) above WGS84 earth ellipsoid. ",blank=True, null=True) 
    name = models.CharField("The GPS name of the waypoint.", max_length=255,blank=True, null=True)
    comment = models.CharField("GPS waypoint comment.", max_length=500,blank=True, null=True)
    description = models.CharField("A text description of the element.", max_length=500,blank=True, null=True)
    source = models.CharField("Source of data.", max_length=50,blank=True, null=True)
    symbol = models.CharField("Text of GPS symbol name.", max_length=50,blank=True, null=True)
    type = models.CharField("Type (classification) of the waypoint", max_length=50,blank=True, null=True)
    type_of_gpx_fix = models.CharField("Type of GPX fix.", choices=GPS_FIX, max_length=4,blank=True, null=True)
    satellites = models.DecimalField("Number of satellites used to calculate the GPX fix.", max_digits = 6,  decimal_places = 0,blank=True, null=True)
    horizontal_dilution= models.FloatField("Horizontal dilution of precision.",blank=True, null=True) 
    vertical_dilution= models.FloatField("Vertical dilution of precision.",blank=True, null=True) 
    position_dilution= models.FloatField("Position dilution of precision.",blank=True, null=True) 
    age_of_dgps_data = models.DecimalField("Number of seconds since last DGPS update.", max_digits = 10,  decimal_places = 2 ,blank=True, null=True)
    dgps_id = models.DecimalField("ID of DGPS station used in differential correction.", max_digits = 10,  decimal_places = 2 ,blank=True, null=True)
    extensions = models.TextField("Extensions.", blank=True, null=True)
    heart_rate = models.DecimalField("HR represents the heart rate in beats per minute.", max_digits = 3,  decimal_places = 0 ,blank=True, null=True)
    cadence = models.DecimalField("Cadence represents the cadence in revolutions per minute..", max_digits = 6,  decimal_places = 0 ,blank=True, null=True)
    temperature = models.FloatField("Temp represents the temperature in degrees celcius",blank=True, null=True) 
    distance = models.FloatField("Distance in meters as measured by GPS or wheel sensor",blank=True, null=True) 
    altitude = models.DecimalField("Altitude in meters", max_digits = 10,  decimal_places = 2 ,blank=True, null=True)
    sea_level_pressure = models.DecimalField("Sea level pressure", max_digits = 10,  decimal_places = 2 ,blank=True, null=True)
    speed = models.FloatField("Horitzontal Speed in meters per second (m/s)", blank=True, null=True)
    vertical_speed = models.FloatField("Vertical Speed in meters per second (m/s)", blank=True, null=True)
    energy = models.FloatField("Energy in Calories", blank=True, null=True)

    class Meta:
        db_table = 'GPX_Route_Point'
        verbose_name = 'GPX Route Point'
        verbose_name_plural = 'GPX Route Points'


class mdlGPXRoutePointLinks(models.Model):   
    gpx_track_segment_point = models.ForeignKey(mdlGPXTrackSegmentPoint)
    link = models.URLField("Links to external information about route.", max_length=255,blank=True, null=True)  
    link_text = models.CharField("Text of the GPX route link.", max_length=255,blank=True, null=True)
    link_type = models.CharField("Mime type of GPX route link", max_length=100,blank=True, null=True)  

    class Meta:
        db_table = 'GPX_Route_Point_Link'
        verbose_name = 'GPX Route Point Link'
        verbose_name_plural = 'GPX Route Point Links'
        

geoadmin.site.register(mdlGPXRoutePoint, geoadmin.OSMGeoAdmin)
geoadmin.site.register(mdlGPXWaypoint, geoadmin.OSMGeoAdmin)
geoadmin.site.register(mdlGPXTrackSegmentPoint, geoadmin.OSMGeoAdmin)

geoadmin.site.register(mdlGPXRoute, geoadmin.OSMGeoAdmin)
geoadmin.site.register(mdlGPXTrack, geoadmin.OSMGeoAdmin)
geoadmin.site.register(mdlGPXTrackSegment, geoadmin.OSMGeoAdmin)

admin.site.register(mdlGPXFile)

