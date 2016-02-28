# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render
import logging

from app.track_management.models import mdlTrack,mdlGPXFile,mdlGPXTrack,mdlGPXTrackSegment,mdlGPXTrackSegmentPoint

@login_required
#view that displays all the active tracks of the logged in user 
def vw_list_user_tracks(request):
    
    try:
        tracks = mdlTrack.objects.filter(creation_user=request.user, deleted=False).order_by('-created_timestamp')
        
    except Exception as e:
        if settings.DEBUG: print(e)
        logging.error(e)
        tracks = None
        pass
        
    
    return render(request,'user/trackList.html', {'tracks':tracks})
    
@login_required
def vw_view_user_track_detail(request,track_hash):
    
    track = None
    gpx = None
    gpxTrack = None
    trckObj = {}  
    
    
    trckObj['track_hash_code'] = track_hash
    
    
    try:
        track = mdlTrack.objects.get(hash_code=track_hash)
        
        trckObj['obj_trck'] = track
        
        if track.type == 'gpx':
            
            tracks = []
                        
            gpx = mdlGPXFile.objects.get(track=track)
            trckObj['obj_file'] = gpx
            
            gpxTracks = mdlGPXTrack.objects.filter(gpx_file=gpx)
            
            for trck in gpxTracks:
                
                trck_object = {}
                
                gpxSegments = mdlGPXTrackSegment.objects.filter(gpx_track=trck)
                
                segments = []                
                
                for seg in gpxSegments:
                    
                    segment = {}
                    
                    po = mdlGPXTrackSegmentPoint.objects.filter(gpx_track_segment = seg)
                    
                    segment['points'] = po
                    segment['obj'] = seg
                    segments.append(segment.copy())
                    print(segments)
                
                trck_object['obj'] = trck
                trck_object['segments'] = segments
                tracks.append(trck_object.copy())
                    
                    
            trckObj['tracks'] = tracks
        
                 
            
            
        
    except Exception as e:
        if settings.DEBUG: print(e)
        logging.error(e)
        return render(request,'user/trackNotFound.html', {'track_hash':track_hash})
        pass
    
    print (trckObj)
    return render(request,'user/trackDetails.html', {'track':track, 'gpx':gpx, 'gpxTrack':gpxTrack, 'trck_obj':trckObj})