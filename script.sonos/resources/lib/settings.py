# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import logging

__addon__     = xbmcaddon.Addon(id='script.sonos')
__addonid__   = __addon__.getAddonInfo('id')

# Load the Sonos controller component
from sonos import Sonos

# Import the Mock Sonos class for testing where there is no live Sonos system
from mocksonos import TestMockSonos

# Common logging module
def log(txt):
    if __addon__.getSetting( "logEnabled" ) == "true":
        if isinstance (txt,str):
            txt = txt.decode("utf-8")
        message = u'%s: %s' % (__addonid__, txt)
        xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)

# Class used to supply XBMC logging to the soco scripts
class SocoLogging(logging.Handler):
    def emit(self, message):
        log(message.getMessage())
        
    @staticmethod
    def enable():
        xbmcLogHandler = SocoLogging()
        logger = logging.getLogger('soco')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(xbmcLogHandler)


##############################
# Stores Addon Settings
##############################
class Settings():
    # Value to calculate which version of XBMC we are using
    xbmcMajorVersion = 0

    @staticmethod
    def getXbmcMajorVersion():
        if Settings.xbmcMajorVersion == 0:
            xbmcVer = xbmc.getInfoLabel('system.buildversion')
            log("Settings: XBMC Version = %s" % xbmcVer)
            Settings.xbmcMajorVersion = 12
            try:
                # Get just the major version number
                Settings.xbmcMajorVersion = int(xbmcVer.split(".", 1)[0])
            except:
                # Default to frodo as the default version if we fail to find it
                log("Settings: Failed to get XBMC version")
            log("Settings: XBMC Version %d (%s)" % (Settings.xbmcMajorVersion, xbmcVer))
        return Settings.xbmcMajorVersion

    @staticmethod
    def getSonosDevice(ipAddress=None):
        # Set up the logging before using the Sonos Device
        SocoLogging.enable()
        sonosDevice = None
        if Settings.useTestData():
            sonosDevice = TestMockSonos()
        else:
            if ipAddress == None:
                ipAddress = Settings.getIPAddress()
            if ipAddress != "0.0.0.0":
                sonosDevice = Sonos(ipAddress)
        log("Sonos: IP Address = %s" % ipAddress)
        return sonosDevice

    @staticmethod
    def getIPAddress():
        return __addon__.getSetting("ipAddress")

    @staticmethod
    def setIPAddress(chosenIPAddress):
        # Set the selected item into the settings
        __addon__.setSetting("ipAddress", chosenIPAddress)

    @staticmethod
    def isNotificationEnabled():
        return __addon__.getSetting("notifEnabled") == 'true'

    @staticmethod
    def getNotificationDisplayDuration():
        # Convert to milliseconds before returning
        return int(float(__addon__.getSetting("notifDisplayDuration"))) * 1000

    @staticmethod
    def getNotificationCheckFrequency():
        # Value set in seconds
        return int(float(__addon__.getSetting("notifCheckFrequency")))

    @staticmethod
    def stopNotifIfVideoPlaying():
        return __addon__.getSetting("notifNotIfVideoPlaying") == 'true'

    @staticmethod
    def useXbmcNotifDialog():
        return __addon__.getSetting("xbmcNotifDialog") == 'true'

    @staticmethod
    def useTestData():
        return __addon__.getSetting("useTestData") == 'true'

    @staticmethod
    def getRefreshInterval():
        # Convert to milliseconds before returning
        return int(float(__addon__.getSetting("refreshInterval")) * 1000)

    @staticmethod
    def getAvoidDuplicateCommands():
        # Seconds (float)
        return float(__addon__.getSetting("avoidDuplicateCommands"))

    @staticmethod
    def getBatchSize():
        # Batch size to get items from the Sonos Speaker
        return int(float(__addon__.getSetting("batchSize")))

    @staticmethod
    def getMaxListEntries():
        # Maximum number of values to show in any plugin list
        return int(float(__addon__.getSetting("maxListEntries")))

    @staticmethod
    def displayArtistInfo():
        return __addon__.getSetting("displayArtistInfo") == 'true'

    @staticmethod
    def linkAudioWithSonos():
        return __addon__.getSetting("linkAudioWithSonos") == 'true'

    @staticmethod
    def switchSonosToLineIn():
        return __addon__.getSetting("switchSonosToLineIn") == 'true'

    @staticmethod
    def getVolumeChangeIncrements():
        # Maximum number of values to show in any plugin list
        return int(float(__addon__.getSetting("volumeChangeIncrements")))

