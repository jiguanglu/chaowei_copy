# -*- coding:utf-8 -*-
from typing import List


class ResizePointList:
    def __init__(self, pointCreateTime, resizePointCreateTime, resizePointForword, resizePointHeight,resizePointId, resizePointName,resizePointWidth,
                 resizePointXmin, resizePointYmin, rightColorCode, rightColorName):
        self.pointCreateTime = pointCreateTime
        self.resizePointCreateTime = resizePointCreateTime
        self.resizePointForword = resizePointForword
        self.resizePointHeight = resizePointHeight
        self.resizePointId = resizePointId
        self.resizePointName = resizePointName
        self.resizePointWidth=resizePointWidth
        self.resizePointXmin = resizePointXmin
        self.resizePointYmin = resizePointYmin
        self.rightColorCode = rightColorCode
        self.rightColorName = rightColorName


def __repr__(self):
        return repr((self.pointCreateTime, self.resizePointCreateTime, self.resizePointForword, self.resizePointHeight, self.resizePointId,
                     self.resizePointName, self.resizePointWidth, self.resizePointXmin, self.resizePointYmin, self.rightColorCode,
                     self.rightColorName))


class PicContentList:
    def __init__(self, innerPointCount, innerTopDegreeName, picId, picIndex, picUrl, pointCount,resizePointList: List[ResizePointList],sideScal, topPointCount,
                 topTopDegreeName):
        self.innerPointCount = innerPointCount
        self.innerTopDegreeName = innerTopDegreeName
        self.picId = picId
        self.picIndex = picIndex
        self.picUrl = picUrl
        self.pointCount = pointCount
        self.resizePointList = resizePointList
        self.sideScal = sideScal
        self.topPointCount = topPointCount
        self.topTopDegreeName = topTopDegreeName


    def __repr__(self):
        return repr((self.innerPointCount, self.innerTopDegreeName, self.picId, self.picIndex, self.picUrl,
                     self.pointCount, self.resizePointList,self.sideScal,self.topPointCount,self.topTopDegreeName))


class ori_info:
    def __init__(self, cabinetId, cabinetName, picContentList: List[PicContentList],resizePointCreateTime, resizePointId, resizePointName):
        self.cabinetId = cabinetId
        self.cabinetName = cabinetName
        self.picContentList = picContentList
        self.resizePointCreateTime = resizePointCreateTime
        self.resizePointId = resizePointId
        self.resizePointName = resizePointName

    def __repr__(self):
        return repr((self.cabinetId, self.cabinetName, self.picContentList, self.resizePointCreateTime, self.resizePointId, self.resizePointName))


