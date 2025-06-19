# -- coding: utf-8 --

import sys
import os
import msvcrt
import ctypes

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

    # ch:设置触发模式为off | en:Set trigger mode as off
    ret = cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
    if ret != 0:
        print("error: set trigger mode fail! ret[0x%x]" % ret)
        sys.exit()
    else:
        print("Trigger mode set to continuous.")

    # Exposure tme
    ret = cam.MV_CC_SetFloatValue("ExposureTime", 3000)
    if ret != 0:
        print("error: set exposure time fail! ret[0x%x]" % ret)
    else:
        print("Exposure time set")
    
    # Gain
    ret = cam.MV_CC_SetFloatValue("Gain", 23)
    if ret != 0:
        print("error: set gain fail! ret[0x%x]" % ret)
    else:
        print("Gain set")

    # Pixel format
    # ret = cam.MV_CC_SetEnumValue("PixelFormat", 0x01080001)  # Mono8
    # if ret != 0:
    #     print(f"Error: Failed to set pixel format to Mono8! ret[0x{ret:x}]")
    # else:
    #     print("Pixel format set to Mono8.")

    # # ch 设置数字增益 | en: Set digital shift
    # ret = cam.MV_CC_SetBoolValue("DigitalShiftEnable", False)
    # if ret != 0:
    #     print("error: set digital shift enable fail! ret[0x%x]" % ret)

    # ret = cam.MV_CC_SetFloatValue("DigitalShift", 0)
    # if ret != 0:
    #     print("error: set digital shift fail! ret[0x%x]" % ret)

    # ch 设置行频 | en: Set  acquisition line rate
    ret = cam.MV_CC_SetIntValue("AcquisitionLineRate", 1000)
    if ret != 0:
        print("error: set acquisition line rate fail! ret[0x%x]" % ret)

    ret = cam.MV_CC_SetBoolValue("AcquisitionLineRateEnable", True)
    if ret != 0:
        print("error: set acquisition line rate enable fail! ret[0x%x]" % ret)

    # ch 设置HB模式 | en: Set image compression mode:HB
    # ret = cam.MV_CC_SetEnumValueByString("ImageCompressionMode", "HB")
    # if ret != 0:
    #     print("error: set  image compression mode: HB fail! ret[0x%x]" % ret)
    #     sys.exit()

    stEnumValue = MVCC_ENUMVALUE()
    memset(byref(stEnumValue), 0, sizeof(MVCC_ENUMVALUE))

    ret = cam.MV_CC_GetEnumValue("PixelFormat", stEnumValue)
    if ret == 0:
        print(f"Pixel Format: {stEnumValue.nCurValue}")
    else:
        print(f"Error: Failed to get pixel format! ret[0x{ret:x}]")

    # ch:获取数据包大小 | en:Get payload size
    stParam = MVCC_INTVALUE()
    memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))

    ret = cam.MV_CC_GetIntValue("PayloadSize", stParam)
    if ret != 0:
        print("get payload size fail! ret[0x%x]" % ret)
        sys.exit()
    nPayloadSize = stParam.nCurValue

    # ch:开始取流 | en:Start grab image
    ret = cam.MV_CC_StartGrabbing()
    if ret != 0:
        print("error: start grabbing fail! ret[0x%x]" % ret)
        sys.exit()
    else:
        print("Camera is grabbing!")

    stOutFrame = MV_FRAME_OUT()
    # print(f"Before memset: {stOutFrame}")
    memset(byref(stOutFrame), 0, sizeof(stOutFrame))
    # print(f"After memset: {stOutFrame}")

    ret = cam.MV_CC_GetImageBuffer(stOutFrame, 7000)
    if stOutFrame.pBufAddr is not None and ret == 0:        
        print(f"Received 1 frame: Width: %d \nHeight: %d \nnFrameNum: %d \nFrame length: %d \nFrame buffer address: {stOutFrame.pBufAddr}" % (
            stOutFrame.stFrameInfo.nWidth, stOutFrame.stFrameInfo.nHeight, stOutFrame.stFrameInfo.nFrameNum, stOutFrame.stFrameInfo.nFrameLen))

        if stOutFrame.stFrameInfo.enPixelType == 0x01080001:  # Mono8
            print("Pixel format is Mono8. Skipping high-bandwidth decode.")
            frame_data = (c_ubyte * stOutFrame.stFrameInfo.nFrameLen).from_address(stOutFrame.pBufAddr)

            # Save the raw frame data as an image (e.g., using OpenCV)
            import numpy as np
            import cv2

            image = np.ctypeslib.as_array(frame_data).reshape((stOutFrame.stFrameInfo.nHeight, stOutFrame.stFrameInfo.nWidth))
            cv2.imwrite("image_mono8.bmp", image)
            print("Image saved as Mono8.")
        else:
            # Perform high-bandwidth decode for other pixel formats
            dst_size = nPayloadSize
            HB_decode_param = MV_CC_HB_DECODE_PARAM()
            HB_decode_param.pSrcBuf = stOutFrame.pBufAddr
            HB_decode_param.nSrcLen = stOutFrame.stFrameInfo.nFrameLen
            HB_decode_param.nDstBufSize = dst_size
            HB_decode_param.pDstBuf = (c_ubyte * dst_size)()

            ret = cam.MV_CC_HBDecode(HB_decode_param)
            if ret != 0:
                print("error: high bandwidth decode fail! ret[0x%x]" % ret)
                sys.exit()
            else:
                print("high bandwidth decode ok, dst pixel type is [%d]" % HB_decode_param.enDstPixelType)

        # ch:保存图像 | en:Save image

        c_file_path = "image.bmp".encode('ascii')
        nRGBSize = stOutFrame.stFrameInfo.nWidth * stOutFrame.stFrameInfo.nHeight * 4 + 2048
        stSaveParam = MV_SAVE_IMAGE_TO_FILE_PARAM_EX()
        memset(byref(stSaveParam), 0, sizeof(stSaveParam))
        stSaveParam.nWidth = stOutFrame.stFrameInfo.nWidth
        stSaveParam.nHeight = stOutFrame.stFrameInfo.nHeight
        stSaveParam.pData = HB_decode_param.pDstBuf
        stSaveParam.enImageType = MV_Image_Bmp
        stSaveParam.nDataLen = HB_decode_param.nDstBufLen
        stSaveParam.enPixelType = HB_decode_param.enDstPixelType
        stSaveParam.nQuality = 80
        stSaveParam.iMethodValue = 3
        stSaveParam.pcImagePath = ctypes.create_string_buffer(c_file_path)
        ret = cam.MV_CC_SaveImageToFileEx(stSaveParam)
        if ret != 0:
            print("error: save image to file fail! ret[0x%x]" % ret)
            sys.exit()
        else:
            print("save image to file is OK")

        cam.MV_CC_FreeImageBuffer(stOutFrame)

    else:
        print("error: get one frame fail, ret[0x%x]" % ret)

    print("press a key to continue.")
    msvcrt.getch()

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
