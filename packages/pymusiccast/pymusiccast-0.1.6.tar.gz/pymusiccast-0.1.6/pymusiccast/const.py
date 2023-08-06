#!/usr/bin/env python
"""This file defines constants."""

ENDPOINTS = {
    "getDeviceInfo": "http://{}/YamahaExtendedControl/v1/system/getDeviceInfo",
    "getFeatures": "http://{}/YamahaExtendedControl/v1/system/getFeatures",
    "getLocationInfo": ("http://{}/YamahaExtendedControl"
                        "/v1/system/getLocationInfo"),
    "getNetworkStatus": ("http://{}/YamahaExtendedControl"
                         "/v1/system/getNetworkStatus"),
    "getPlayInfo": "http://{}/YamahaExtendedControl/v1/netusb/getPlayInfo",
    "setPlayback": "http://{}/YamahaExtendedControl/v1/netusb/setPlayback",
    "getStatus": "http://{}/YamahaExtendedControl/v1/{}/getStatus",
    "setInput": "http://{}/YamahaExtendedControl/v1/{}/setInput",
    "setMute": "http://{}/YamahaExtendedControl/v1/{}/setMute",
    "setPower": "http://{}/YamahaExtendedControl/v1/{}/setPower",
    "setVolume": "http://{}/YamahaExtendedControl/v1/{}/setVolume",
}

STATE_UNKNOWN = "unknown"
STATE_ON = "on"
STATE_OFF = "off"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_IDLE = "idle"
