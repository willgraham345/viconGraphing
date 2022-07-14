# This is a sample Python script.
from __future__ import print_function
from vicon_dssdk import ViconDataStream
import numpy as np
from flightObjectGrapher import flightObjectGrapher
import time

t_duration = 15;
orientationMode = 'euler'
if __name__ == '__main__':
    # Create instance of python objects, and custom flightobject stuff
    client = ViconDataStream.RetimingClient()
    cf1 = flightObjectGrapher(orientationMode)
    try:
        client.Connect("localhost:801")
        print("Vicon is connected...", client.IsConnected())
        # Check the version
        print('Version #: ', client.GetVersion())
        client.SetAxisMapping(ViconDataStream.Client.AxisMapping.EForward, ViconDataStream.Client.AxisMapping.ELeft,
                              ViconDataStream.Client.AxisMapping.EUp)
        xAxis, yAxis, zAxis = client .GetAxisMapping()
        print('X Axis', xAxis, 'Y Axis', yAxis, 'Z Axis', zAxis)
        t_begin = time.time()
        while(time.time() < t_begin + t_duration):
            t_current = time.time()
            try:
                frame = client.UpdateFrame()
                # print('frame = ', frame)
                subjectNames = client.GetSubjectNames()
                for subjectName in subjectNames:
                    segmentNames = client.GetSegmentNames(subjectName)
                    for segmentName in segmentNames:
                        # print('current time = ', t_current)

                        if orientationMode == 'euler':
                            [(X,Y,Z), occlusion2] = client.GetSegmentGlobalTranslation(subjectName, segmentName)
                            [(roll, pitch, yaw), occlusion1] = client.GetSegmentGlobalRotationEulerXYZ(subjectName,
                                                                                                       segmentName)
                            XYZ = (X, Y, Z)
                            orientation = (roll, pitch, yaw)
                        elif orientationMode == 'quaternion':
                            [(X,Y,Z), occlusion2] = client.GetSegmentGlobalTranslation(subjectName, segmentName)
                            [(q_x, q_y, q_z, q_w), occlusion3] = client.GetSegmentGlobalRotationQuaternion(subjectName, segmentName)
                            XYZ = (X, Y, Z)
                            orientation = (roll, pitch, yaw)
                        t_current = time.time()
                        cf1.addPoseVals(XYZ, orientation, frame, t_current-t_begin)
                        # cf1.attitudeControl(orientation, desOrientation, timeStep, gainVals)
                        print('Added')


            except ViconDataStream.DataStreamException as e:
                print('Handled data stream error (Nested)... ERROR:', e)
                print('cf1 t', cf1.t)
                print('cf1 omemga_pitch', cf1.omega_pitch)
        t_last = time.time()
        cf1.graphPoseVals()
    except ViconDataStream.DataStreamException as e:
        print('Handled data stream error (Global)... ERROR:', e)