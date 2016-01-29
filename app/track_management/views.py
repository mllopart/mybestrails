# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.gis.geos import Point, LineString, MultiLineString
from app.track_management.forms import UploadGpxForm
from app.track_management.models import mdlGPXPoint, mdlGPXTrack, mdlGPXFile, mdlTrack
from django.conf import settings
from lib import gpxpy
import logging
from django.contrib.contenttypes.models import ContentType
from app.logger_management.models import mdlLog
import uuid
import os
from django.core.urlresolvers import reverse


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

    gpx_file = open(settings.TMP_MEDIA_ROOT+fGPX)
    gpx = gpxpy.parse(gpx_file)
    
    #after loading the file in memory, we can delete the phisical one
    os.unlink(gpx_file.name)

    if gpx.waypoints:        
        for waypoint in gpx.waypoints:            
            new_waypoint = mdlGPXPoint()
            
            if waypoint.name:
                new_waypoint.name = waypoint.name
            else:
                new_waypoint.name = 'unknown'
                
            new_waypoint.point = Point(waypoint.longitude, waypoint.latitude)
            new_waypoint.gpx_file = file_instance
            new_waypoint.save()

    if gpx.tracks:
        for track in gpx.tracks:

            new_track = mdlGPXTrack()
            for segment in track.segments:
                
                track_list_of_points = []                
                for point in segment.points:
                    
                    point_in_segment = Point(point.longitude, point.latitude)
                    track_list_of_points.append(point_in_segment.coords)

                new_track_segment = LineString(track_list_of_points)               
            
            new_track.track = MultiLineString(new_track_segment)
            new_track.gpx_file = file_instance    
            new_track.save()


#view to upload the GPX files.
def upload_gpx(request):

    if request.method == 'POST':        
                
        form = UploadGpxForm(request.POST, request.FILES)
        
        if form.is_valid(): 
          
            file_instance = mdlGPXFile()
            track = mdlTrack()
            
            track.name = 'test1'
            track.creation_user = request.user
            track.type = 'gpx'            
            track.save()
            
            #file_instance.gpx_file = request.FILES['gpxfile']            
            file_instance.track = track
            
            try:
                fGPX = request.FILES['gpxfile']
            except Exception as e:
                logging.error(e)
                fGPX = None
                pass
            
            if fGPX:
                try:                                            
                    file_instance.gpx_file.save(fGPX.name, fGPX)
                except Exception as e:
                    logging.error(e)
            
            file_instance.save()  
            
            tmp_file_name = handle_uploaded_file(fGPX)         
            
            SaveGPXtoPostGIS(tmp_file_name, file_instance)
            
            try:
                lo = mdlLog()
                lo.user = request.user
                lo.content_type = ContentType.objects.get(model = 'mdltrack')
                lo.object_id = request.user.id
                lo.action = 'add new track - GPX'
                lo.save()
                
            except Exception as e:
                print(e)
                logging.error(e)

            return HttpResponseRedirect(reverse('homepage'))

    else:
        form = UploadGpxForm()

    return render(request,'form.html', {'form':form})
