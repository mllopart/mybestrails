# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.gis.geos import Point, LineString, MultiLineString
from app.track_management.forms import UploadGpxForm
from app.track_management.models import mdlGPXTrackSegmentPoint,mdlGPXTrack,mdlGPXFile,mdlGPXWaypoint,mdlGPXTrackLinks,mdlGPXTrackSegment,mdlTrack,mdlGPXWaypointLinks,mdlGPXRoute,mdlGPXRouteLinks,mdlGPXRoutePoint,mdlGPXRoutePointLinks
from django.conf import settings
from lib import gpxpy
import logging
from django.contrib.contenttypes.models import ContentType
from app.logger_management.models import mdlLog
import uuid
import os
import pytz
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


#function that temporarily stores the file at the disk so we can play with it.
#it creates a totally random file name
def handle_uploaded_file(f):
    tmp_file_name = str(uuid.uuid4().hex)

    with open(settings.TMP_MEDIA_ROOT+tmp_file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            
    return tmp_file_name

#function to process the GPX file
#it reads all file properties and store the points in the database 
def SaveGPXtoPostGIS(fGPX, file_instance):

    try:
        #opening the GPX file, loaded by the user
        gpx_file = open(settings.TMP_MEDIA_ROOT+fGPX)
    
        #parsing the GPX file
        #we store all the file contents within the gpx variable
        gpx = gpxpy.parse(gpx_file)
        
        #after loading the file in memory, we can delete the physical one
        os.unlink(gpx_file.name)
        
    except Exception as e:
        if settings.DEBUG: print(e)
        logging.error(e)
        
    try:
        ###### WAYPOINTS #######
        if gpx.waypoints:
                    
            for wp in gpx.waypoints:            
                nwp = mdlGPXWaypoint()
                
                #Assignation of all the parameters for each waypoint
                if wp.name:
                    nwp.name = wp.name
                else:
                    nwp.name = 'unk'
                    
                nwp.point = Point(wp.longitude, wp.latitude)
                nwp.gpx_file = file_instance
                nwp.elevation = wp.elevation
                if wp.time:
                    nwp.time = wp.time.replace(tzinfo=pytz.UTC)
                nwp.magnetic_variation = wp.magnetic_variation
                nwp.geoid_height = wp.geoid_height
                nwp.comment = wp.comment
                nwp.description = wp.description
                nwp.source = wp.source
                nwp.symbol = wp.symbol
                nwp.type = wp.type
                nwp.type_of_gpx_fix = wp.type_of_gpx_fix
                nwp.satellites = wp.satellites
                nwp.horizontal_dilution = wp.horizontal_dilution
                nwp.vertical_dilution = wp.vertical_dilution
                nwp.position_dilution = wp.position_dilution
                nwp.age_of_dgps_data = wp.age_of_dgps_data
                nwp.dgps_id = wp.dgps_id
                nwp.extensions = wp.extensions            
                nwp.save()
                
                if wp.link:
                    wpl = mdlGPXWaypointLinks()
                    wpl.link = wp.link
                    wpl.link_text = wp.link_text
                    wpl.link_type = wp.link_type
                    wpl.gpx_waypoint = nwp
                    wpl.save()
    
        ###### TRACK #######
        if gpx.tracks:
            
            for track in gpx.tracks:
    
                nt = mdlGPXTrack()
                nt.gpx_file = file_instance
                nt.name = track.name
                nt.comment = track.comment
                nt.description = track.description
                nt.source = track.source
                #po.link = None
                #po.link_text = None
                if (track.number):
                    nt.number = track.number
                    
                #po.link_type = None
                nt.type = track.type
                nt.extensions = track.extensions  
                nt.save()
                
                if track.link:
                    tl = mdlGPXTrackLinks()
                    tl.link = track.link
                    tl.link_text = track.link_text
                    tl.link_type = track.link_type
                    tl.gpx_track = nt
                    tl.save()
                
                for segment in track.segments:
                    
                    trs = mdlGPXTrackSegment()                
                    trs.gpx_track = nt
                    trs.extensions = segment.extensions
                    trs.save()
                    
                    track_list_of_points = []    
                                
                    for point in segment.points:
                        
                        po =  mdlGPXTrackSegmentPoint()                   
                        point_in_segment = Point(point.longitude, point.latitude)
                        track_list_of_points.append(point_in_segment.coords)
                        
                        po.gpx_track_segment = trs
                        po.point = point_in_segment
                        po.elevation = point.elevation
                        
                        if point.time:
                            po.time = point.time.replace(tzinfo=pytz.UTC)
                            
                        po.course = point.course
                        po.speed = point.speed
                        po.magnetic_variation = point.magnetic_variation
                        po.geoid_height = point.geoid_height
                        po.name = point.name
                        po.comment = point.comment
                        po.description = point.description
                        po.source = point.source
                        po.symbol = point.symbol
                        po.type = point.type
                        po.type_of_gpx_fix = point.type_of_gpx_fix
                        po.satellites = point.satellites
                        po.horizontal_dilution = point.horizontal_dilution
                        po.vertical_dilution = point.vertical_dilution
                        po.position_dilution = point.position_dilution
                        po.age_of_dgps_data = point.age_of_dgps_data
                        po.dgps_id = point.dgps_id
                        po.extensions = point.extensions
                        po.save()
    
                    new_track_segment = LineString(track_list_of_points)
                    
                    trs.segmentLine =   LineString(track_list_of_points)
                    trs.save()             
                
                nt.track = MultiLineString(new_track_segment)            
                nt.save()
    
    
        ###### ROUTES #######
        if gpx.routes:
            for route in gpx.routes:
                ro = mdlGPXRoute()
                ro.gpx_file = file_instance
                ro.name = route.name
                ro.comment = route.comment
                ro.description = route.description
                ro.source = route.source
                
                if route.number:
                    ro.number = route.number
                    
                ro.type = route.type
                ro.extensions = route.extensions
                ro.save()
                
                if route.link:
                    rl = mdlGPXRouteLinks()
                    rl.link = route.link
                    rl.link_text = route.link_text
                    rl.link_type = route.link_type
                    rl.gpx_route = ro
                    rl.save()
                
                route_list_of_points = []    
                                
                for point in segment.points:
                    
                    po =  mdlGPXRoutePoint()         
                    po.gpx_route = ro         
                    point_in_segment = Point(point.longitude, point.latitude)
                    route_list_of_points.append(point_in_segment.coords)
                    
                    po.elevation = point.elevation
                    
                    if point.time:
                            po.time = point.time.replace(tzinfo=pytz.UTC)
                            
                    po.magnetic_variation = point.magnetic_variation
                    po.geoid_height = point.geoid_height
                    po.name = point.name
                    po.comment = point.comment
                    po.description = point.description
                    po.source = point.source
                    po.symbol = point.symbol
                    po.type = point.type
                    po.type_of_gpx_fix = point.type_of_gpx_fix
                    po.satellites = point.satellites
                    po.horizontal_dilution = point.horizontal_dilution
                    po.vertical_dilution = point.vertical_dilution
                    po.position_dilution = point.position_dilution
                    po.age_of_dgps_data = point.age_of_dgps_data
                    po.dgps_id = point.dgps_id
                    po.link_type = point.link_type
                    po.extensions = point.extensions
                    po.save()
                    
                    if point.link:
                        rpl = mdlGPXRoutePointLinks()
                        rpl.link = point.link
                        rpl.link_text = point.link_text
                        rpl.link_type = point.link_type
                        rpl.gpx_route_point = po
                        rpl.save()
                
              
                ro.trackLine =   LineString(route_list_of_points)            
                ro.save()   
                     
    except Exception as e:
        if settings.DEBUG: print(e)
        logging.error(e)           

#view to upload the GPX files.
@login_required
def upload_gpx(request):

    if request.method == 'POST':        
                
        form = UploadGpxForm(request.POST, request.FILES)
        
        if form.is_valid(): 
            
            fCd= form.cleaned_data
          
            file_instance = mdlGPXFile()
            track = mdlTrack()
            
            if settings.DEBUG:print(fCd['title'])
            
            try:            
                track.name = fCd['title']
                track.description = fCd['description']
                track.creation_user = request.user
                track.type = 'gpx'            
                track.save()
            except Exception as e:
                if settings.DEBUG:print(e)
                logging.error(e)
                     
            file_instance.track = track
            
            try:
                fFileGPX = request.FILES['gpxfile']
            except Exception as e:
                if settings.DEBUG:print(e)
                logging.error(e)
                fFileGPX = None
                pass
            
            if fFileGPX:
                try:                                            
                    file_instance.gpx_file.save(fFileGPX.name, fFileGPX)
                except Exception as e:
                    if settings.DEBUG:print(e)
                    logging.error(e)
            
            file_instance.save()  
            
            tmp_file_name = handle_uploaded_file(fFileGPX)         
            
            SaveGPXtoPostGIS(tmp_file_name, file_instance)
            
            try:
                lo = mdlLog()
                lo.user = request.user
                lo.content_type = ContentType.objects.get(model = 'mdltrack')
                lo.object_id = request.user.id
                lo.action = 'add new track - GPX'
                lo.save()                
            except Exception as e:
                if settings.DEBUG:print(e)
                logging.error(e)

            return HttpResponseRedirect(reverse('general:homepage'))

    else:
        form = UploadGpxForm()

    return render(request,'uploads/form.html', {'form':form})
