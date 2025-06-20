# -- coding: utf-8 --

import sys
import os
import msvcrt
import ctypes
import time
import numpy as np
import cv2
import keyboard 
from ctypes import c_ubyte, byref

sys.path.append(os.getenv('MVCAM_COMMON_RUNENV') + "/Samples/Python/MvImport")
# from MvImport.MvCameraControl_class import *
from MvCameraControl_class import *


if __name__ == "__main__":

    # ch:初始化SDK | en: initialize SDK
    MvCamera.MV_CC_Initialize()

    deviceList = MV_CC_DEVICE_INFO_LIST()
    t_layer_type = (MV_GIGE_DEVICE | MV_USB_DEVICE | MV_GENTL_CAMERALINK_DEVICE
                    | MV_GENTL_CXP_DEVICE | MV_GENTL_XOF_DEVICE)

    # ch:枚举设备 | en:Enum device
    ret = MvCamera.MV_CC_EnumDevices(t_layer_type, deviceList)
    if ret != 0:
        print("error: enum devices fail! ret[0x%x]" % ret)
        sys.exit()

    if deviceList.nDeviceNum == 0:
        print("find no device!")
        sys.exit()

    print("find %d devices!" % deviceList.nDeviceNum)

    for i in range(0, deviceList.nDeviceNum):
        mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
        if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE or mvcc_dev_info.nTLayerType == MV_GENTL_GIGE_DEVICE:
            print("gige device: [%d]" % i)
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                if 0 == per:
                    break
                strModeName = strModeName + chr(per)
            print("device model name: %s" % strModeName)

            nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
            nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
            nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
            nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
            print("current ip: %d.%d.%d.%d" % (nip1, nip2, nip3, nip4))
            
            chUserDefinedName = ""
            for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chUserDefinedName:
                if 0 == per:
                    break
                chUserDefinedName = chUserDefinedName + chr(per)
            print("device user define name: %s" % chUserDefinedName)
        elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
            print("u3v device: [%d]" % i)
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                if per == 0:
                    break
                strModeName = strModeName + chr(per)
            print("device model name: %s" % strModeName)

            strSerialNumber = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                if per == 0:
                    break
                strSerialNumber = strSerialNumber + chr(per)
            print("user serial number: %s" % strSerialNumber)
            
            strUserDefinedName = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chUserDefinedName:
                if per == 0:
                    break
                strUserDefinedName = strUserDefinedName + chr(per)
            print("device user define name: %s" % strUserDefinedName)
        elif mvcc_dev_info.nTLayerType == MV_GENTL_XOF_DEVICE:
            print("XoF device: [%d]" % i)
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stXoFInfo.chModelName:
                if per == 0:
                    break
                strModeName = strModeName + chr(per)
            print("device model name: %s" % strModeName)

            strSerialNumber = ""
            for per in mvcc_dev_info.SpecialInfo.stXoFInfo.chSerialNumber:
                if per == 0:
                    break
                strSerialNumber = strSerialNumber + chr(per)
            print("user serial number: %s" % strSerialNumber)

            strUserDefinedName = ""
            for per in mvcc_dev_info.SpecialInfo.stXoFInfo.chUserDefinedName:
                if per == 0:
                    break
                strUserDefinedName = strUserDefinedName + chr(per)
            print("device user define name: %s" % strUserDefinedName)
        elif mvcc_dev_info.nTLayerType == MV_GENTL_CXP_DEVICE:
            print("CXP device: [%d]" % i)
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stCXPInfo.chModelName:
                if per == 0:
                    break
                strModeName = strModeName + chr(per)
            print("device model name: %s" % strModeName)

            strSerialNumber = ""
            for per in mvcc_dev_info.SpecialInfo.stCXPInfo.chSerialNumber:
                if per == 0:
                    break
                strSerialNumber = strSerialNumber + chr(per)
            print("user serial number: %s" % strSerialNumber)

            strUserDefinedName = ""
            for per in mvcc_dev_info.SpecialInfo.stCXPInfo.chUserDefinedName:
                if per == 0:
                    break
                strUserDefinedName = strUserDefinedName + chr(per)
            print("device user define name: %s" % strUserDefinedName)
        elif mvcc_dev_info.nTLayerType == MV_GENTL_CAMERALINK_DEVICE:
            print("CML device: [%d]" % i)
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stCMLInfo.chModelName:
                if per == 0:
                    break
                strModeName = strModeName + chr(per)
            print("device model name: %s" % strModeName)

            strSerialNumber = ""
            for per in mvcc_dev_info.SpecialInfo.stCMLInfo.chSerialNumber:
                if per == 0:
                    break
                strSerialNumber = strSerialNumber + chr(per)
            print("user serial number: %s" % strSerialNumber)

            strUserDefinedName = ""
            for per in mvcc_dev_info.SpecialInfo.stCMLInfo.chUserDefinedName:
                if per == 0:
                    break
                strUserDefinedName = strUserDefinedName + chr(per)
            print("device user define name: %s" % strUserDefinedName)

    nConnectionNum = input("Select camera number to connect: ")

    if int(nConnectionNum) >= deviceList.nDeviceNum:
        print("error: input error!")
        sys.exit()

    # ch:创建相机实例 | en:Creat Camera Object
    cam = MvCamera()

    # ch:选择设备并创建句柄 | en:Select device and create handle
    stDeviceList = cast(deviceList.pDeviceInfo[int(nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)).contents

    ret = cam.MV_CC_CreateHandle(stDeviceList)
    if ret != 0:
        print("error: create handle fail! ret[0x%x]" % ret)
        sys.exit()

    # ch:打开设备 | en:Open device
    ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
    if ret != 0:
        print("error: open device fail! ret[0x%x]" % ret)
        sys.exit()

    # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
    if stDeviceList.nTLayerType == MV_GIGE_DEVICE or stDeviceList.nTLayerType == MV_GENTL_GIGE_DEVICE:
        nPacketSize = cam.MV_CC_GetOptimalPacketSize()
        if int(nPacketSize) > 0:
            ret = cam.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
            if ret != 0:
                print("warning: Set Packet Size fail! ret[0x%x]" % ret)
        else:
            print("warning: Get Packet Size fail! ret[0x%x]" % nPacketSize)
    
    # Parameters
    gain = 23.9
    exposure_time = 3000
    line_rate = 17000
    pixel_format = 35127316  # RGB8Packed
    img_buffr = 7000
    height = 20

    ret = cam.MV_CC_SetIntValue("Height", height)
    if ret != 0:
        print("error: set height fail! ret[0x%x]" % ret)
    else:
        print(f"Height set to {height}")
    
    # Exposure tme
    ret = cam.MV_CC_SetFloatValue("ExposureTime", exposure_time)
    if ret != 0:
        print("error: set exposure time fail! ret[0x%x]" % ret)
    else:
        print(f"Exposure time set to {exposure_time}")
    
    # Gain
    ret = cam.MV_CC_SetFloatValue("Gain", gain)
    if ret != 0:
        print("error: set gain fail! ret[0x%x]" % ret)
    else:
        print(f"Gain set to {gain}")

    # Pixel format
    ret = cam.MV_CC_SetEnumValue("PixelFormat", pixel_format)
    if ret != 0:
        print(f"Error: Failed to set pixel format ret[0x{ret:x}]")
    else:
        print("Pixel format set")

    # # ch 设置数字增益 | en: Set digital shift
    # ret = cam.MV_CC_SetBoolValue("DigitalShiftEnable", False)
    # if ret != 0:
    #     print("error: set digital shift enable fail! ret[0x%x]" % ret)

    # ret = cam.MV_CC_SetFloatValue("DigitalShift", 0)
    # if ret != 0:
    #     print("error: set digital shift fail! ret[0x%x]" % ret)

    ret = cam.MV_CC_SetBoolValue("AcquisitionLineRateEnable", True)
    if ret != 0:
        print("error: set acquisition line rate enable fail! ret[0x%x]" % ret)

    # ch 设置行频 | en: Set  acquisition line rate
    ret = cam.MV_CC_SetIntValue("AcquisitionLineRate", line_rate)
    if ret != 0:
        print("error: set acquisition line rate fail! ret[0x%x]" % ret)
    else:
        print(f"Acquisition line rate set to {line_rate}")

    # ch 设置HB模式 | en: Set image compression mode:HB
    # ret = cam.MV_CC_SetEnumValueByString("ImageCompressionMode", "HB")
    # if ret != 0:
    #     print("error: set  image compression mode: HB fail! ret[0x%x]" % ret)
    #     sys.exit()

    stEnumValue = MVCC_ENUMVALUE()
    memset(byref(stEnumValue), 0, sizeof(MVCC_ENUMVALUE))
    # ch:获取数据包大小 | en:Get payload size
    stParam = MVCC_INTVALUE()
    memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))

    stOutFrame = MV_FRAME_OUT()
    memset(byref(stOutFrame), 0, sizeof(stOutFrame))

    # Image folder
    output_folder = "imgs"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Frame counter
    frame_counter = 0

    # Callback function to handle frames
    def frame_callback(pData, pFrameInfo, pUser):
        global frame_counter
        start = time.time()
        # Cast the frame info to the appropriate structure
        frame_info = ctypes.cast(pFrameInfo, ctypes.POINTER(MV_FRAME_OUT_INFO_EX)).contents

        print("---------- Received a frame ----------")
        print(f"Width: {frame_info.nWidth}")
        print(f"Height: {frame_info.nHeight}")
        print(f"Frame Number: {frame_info.nFrameNum}")
        print(f"Frame Length: {frame_info.nFrameLen}")

        # Check pixel format
        if frame_info.enPixelType == 35127316:  # RGB8Packed
            print("Pixel format is RGB8Packed. Processing frame.")

            # Convert the frame buffer to an image
            frame_data = ctypes.cast(pData, ctypes.POINTER(c_ubyte * frame_info.nFrameLen)).contents
            image = np.ctypeslib.as_array(frame_data).reshape((frame_info.nHeight, frame_info.nWidth, 3))

            # Save the image with a unique filename
            filename = os.path.join(output_folder, f"image_{frame_info.nFrameNum}.bmp")
            cv2.imwrite(filename, image)
            print(f"Image saved as {filename}.")
        else:
            print(f"Unsupported pixel format: {frame_info.enPixelType}")
        end = time.time()
        print(f"Frame processing time: {end - start:.4f} seconds")
        frame_counter += 1

    # Register the callback function
    CALLBACK_FUNC = ctypes.CFUNCTYPE(None, ctypes.POINTER(c_ubyte), ctypes.POINTER(MV_FRAME_OUT_INFO_EX), ctypes.c_void_p)
    frame_callback_func = CALLBACK_FUNC(frame_callback)

    try:
        # Set trigger mode to continuous
        ret = cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)  # Continuous mode
        if ret != 0:
            print(f"Error: Failed to set trigger mode to continuous! ret[0x{ret:x}]")

        # Start grabbing in asynchronous mode
        ret = cam.MV_CC_RegisterImageCallBackEx(frame_callback_func, None)
        if ret != 0:
            print(f"Error: Failed to register callback! ret[0x{ret:x}]")
            raise Exception("Failed to register callback.")

        ret = cam.MV_CC_StartGrabbing()
        if ret != 0:
            print(f"Error: Failed to start grabbing! ret[0x{ret:x}]")
            raise Exception("Failed to start grabbing.")

        print("Press 'q' to stop the program.")
        while True:
            # Check if the user pressed 'q' to stop
            if keyboard.is_pressed('q'):
                print("Stopping image capture...")
                break

    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        print("Releasing resources...")
        cam.MV_CC_StopGrabbing()
        cam.MV_CC_CloseDevice()
        cam.MV_CC_DestroyHandle()

        # ch:停止取流 | en:Stop grab image
        ret = cam.MV_CC_StopGrabbing()
        if ret != 0:
            print("error: stop grabbing fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:关闭设备 | Close device
        ret = cam.MV_CC_CloseDevice()
        if ret != 0:
            print("error: close device fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:销毁句柄 | Destroy handle
        ret = cam.MV_CC_DestroyHandle()
        if ret != 0:
            print("error: destroy handle fail! ret[0x%x]" % ret)
            sys.exit()

        # ch:反初始化SDK | en: finalize SDK
        MvCamera.MV_CC_Finalize()


