﻿import QtQuick 2.0
IGuiDialogView
{
	id: q687865857
	objId: 687865857
	x: 160
	y: 126
	width: 480
	height: 228
	qm_FillRectWidth: 480
	qm_FillRectHeight: 228
	qm_FontSize: 8
	qm_FontFamilyName: "Tahoma"
	qm_BorderCornerRadius: 0
	qm_BorderWidth: 1
	qm_ValueVarBorder: 1
	qm_BorderColor: "#ff1c1f30"
	qm_ImageID: 5
	qm_TileTop: 2
	qm_TileBottom: 2
	qm_TileRight: 2
	qm_TileLeft: 2
	qm_FillColor: "#fff4f4f5"
	z:205
	captionrectX: 0
	captionrectY: 0
	captionrectWidth: 480
	captionrectHeight: 34
	captionrectBackgroundColor: "#ff3e414f"
	captionrectForegroundColor: "#ffffffff"
	captionTextX: 12
	captionTextY: 8
	captionTextWidth: 290
	captionTextHeight: 20
	qm_DisplayText: "Info text"
	IGuiListCtrl
	{
		id: qu687865857
		objectName: "qu687865857"
		x: 3
		y: 34
		width: 480
		height: 160
		totalColumnWidth: 474
		qm_tableBackColor: "#00000000"
		qm_tableTextColor: "#ff13192c"
		qm_tableValueVarTextAlignmentHorizontal: Text.AlignLeft
		qm_tableValueVarTextAlignmentVertical: Text.AlignTop
		qm_tableValueVarTextOrientation: 0
		qm_tableMarginLeft: 1
		qm_tableMarginRight: 1
		qm_tableMarginBottom: 1
		qm_tableMarginTop: 1
		qm_noOfColumns: 1
		qm_tableRowHeight: 13
		qm_tableHeaderHeight: 13
		qm_hasHeader: false
		qm_hasGridLines: false
		qm_hasBorder: false
		qm_hasDisplayFocusLine: false
		qm_hasVerticalScrolling: true
		qm_hasVerticalScrollBar: false
		qm_hasHorizontalScrollBar: false
		qm_hasColumnOrdering: false
		qm_hasHighLightFullRow: false
		qm_hasVerUpDownPresent: true
		qm_hasVerPgUpDownPresent: true
		qm_hasHighlight: false
		qm_hasUpDownAsPageUpDown: true
		qm_hasLongAlarmButton: false
		qm_hasExtraPixelForLineHeight: false
		qm_hasRowEditable: false
		qm_hasRowJustification: false
		qm_hasRowJustificationBottom: false
		qm_linesPerRow: 0
		IGuiListColumnView
		{
			id: qc129000001
			colIndex: 0
			x: 0
			y: 0
			width: 474
			height: 128
			columnType: 0
		}
	}
	modalityWidth: 320
	modalityHeight: 252
	IGuiModality{ }
	IGuiGraphicButton
	{
		id: q486539265
		objId: 486539265
		x: 446
		y: 0
		width: 34
		height: 34
		qm_FillRectWidth: 34
		qm_FillRectHeight: 34
		qm_BorderCornerRadius: 0
		qm_BorderWidth: 1
		qm_ValueVarBorder: 1
		qm_BorderColor: "#ff1c1f30"
		qm_ImageID: 3
		qm_TileTop: 2
		qm_TileBottom: 2
		qm_TileRight: 2
		qm_TileLeft: 2
		qm_FillColor: "#ff464b5a"
		qm_TextColor: "#ffffffff"
		qm_ValueVarTextAlignmentHorizontal: Image.AlignHCenter
		qm_ValueVarTextAlignmentVertical: Image.AlignVCenter
		qm_ValueVarTextOrientation: 0
		qm_MarginLeft: 1
		qm_MarginRight: 1
		qm_MarginBottom: 1
		qm_MarginTop: 1
		qm_FocusWidth: 2
		qm_FocusColor: "#ff55bfff"
		qm_Streached :false
		qm_ButtonImageId :4
		qm_ContentVisibility : false
		Component.onCompleted:
		{
			proxy.initProxy(q486539265,486539265)
		}
	}
	IGuiQmlRectangle
	{
		id: q671088640
		objId: 671088640
		qm_Height: 34
		qm_Width: 478
		qm_BorderWidth: 0
		qm_TextColor: "#ff000000"
		qm_FillColor: "#ff3e414f"
		Component.onCompleted:
		{
			proxy.initProxy(q671088640,671088640)
		}
	}
	Component.onCompleted:
	{
		proxy.initProxy(q687865857,687865857)
	}
}
