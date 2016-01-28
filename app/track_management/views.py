# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.contrib.gis.geos import Point, LineString, MultiLineString
from app.track_management.forms import UploadGpxForm
from app.track_management.models import mdlGPXPoint, mdlGPXTrack, mdlGPXFile, mdlTrack
from django.conf import settings
import gpxpy
import gpxpy.gpx
#from sessioninstaller.core import track_usage


def SaveGPXtoPostGIS(f, file_instance):
    
    gpx_file = open(settings.MEDIA_ROOT+ '/uploaded_gpx_files'+'/' + f.name)
    gpx = gpxpy.parse(gpx_file)

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


def upload_gpx(request):
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        file_instance = mdlGPXFile()
        track = mdlTrack()
        track.name = 'test1'
        track.creation_user = request.user
        track.type = 'gpx'
                
        form = UploadGpxForm(request.POST, request.FILES, instance=file_instance)
        
        args['form'] = form
        
        if form.is_valid():    
            
            track.save()
            form.track = track
            form.save()            
            
            SaveGPXtoPostGIS(request.FILES['gpx_file'], file_instance)

            return HttpResponseRedirect('success/')

    else:
        args['form'] = UploadGpxForm()

    return render(request,'form.html', args)

def upload_success(request):
    return render(request, 'success.html')