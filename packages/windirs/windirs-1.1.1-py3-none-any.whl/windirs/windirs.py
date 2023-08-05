"""
Access Windows path locations using attributes of windirs object.
"""

from threading import Lock

# DO NOT USE FROM WIN_FX._KNOWN_PATHS. MUST IMPORT ENTIRE MODULE TO CORRECLY
# USE CTYPES
import _knownpaths


__all__ = ['windirs']


class _WindowsFolders:
    _lock = Lock()
    _cache = {}


    def __getitem__(self, item):
        try:
            return self._cache[item]
        except KeyError:
            self._lock.acquire()
            try:
                self._cache[item] = ret = _get_windows_path(item)
            finally:
                self._lock.release()
        return ret


    def __getattribute__(self, attr):
        if not attr.startswith('_'):
            try:
                return self[attr]
            except KeyError:
                raise AttributeError
        return super().__getattribute__(attr)


    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith('_'):
                yield attr


    CDBurning = None
    CommonAdminTools = None
    CommonOEMLinks = None
    CommonPrograms = None
    CommonStartMenu = None
    CommonStartup = None
    CommonTemplates = None
    Contacts = None
    Cookies = None
    Desktop = None
    DeviceMetadataStore = None
    Documents = None
    DocumentsLibrary = None
    Downloads = None
    Favorites = None
    Fonts = None
    GameTasks = None
    History = None
    ImplicitAppShortcuts = None
    InternetCache = None
    Libraries = None
    Links = None
    LocalAppData = None
    LocalAppDataLow = None
    LocalizedResourcesDir = None
    Music = None
    MusicLibrary = None
    NetHood = None
    OriginalImages = None
    PhotoAlbums = None
    PicturesLibrary = None
    Pictures = None
    Playlists = None
    PrintHood = None
    Profile = None
    ProgramData = None
    ProgramFiles = None
    ProgramFilesX64 = None
    ProgramFilesX86 = None
    ProgramFilesCommon = None
    ProgramFilesCommonX64 = None
    ProgramFilesCommonX86 = None
    Programs = None
    Public = None
    PublicDesktop = None
    PublicDocuments = None
    PublicDownloads = None
    PublicGameTasks = None
    PublicLibraries = None
    PublicMusic = None
    PublicPictures = None
    PublicRingtones = None
    PublicUserTiles = None
    PublicVideos = None
    QuickLaunch = None
    Recent = None
    ResourceDir = None
    RoamingAppData = None
    RoamedTileImages = None
    RoamingTiles = None
    SavedGames = None
    SavedSearches = None
    Screenshots = None
    SearchHistory = None
    SearchTemplates = None
    SendTo = None
    SidebarDefaultParts = None
    SidebarParts = None
    SkyDrive = None
    SkyDriveCameraRoll = None
    SkyDriveDocuments = None
    SkyDrivePictures = None
    StartMenu = None
    Startup = None
    System = None
    SystemX86 = None
    Templates = None
    UserPinned = None
    UserProfiles = None
    UserProgramFiles = None
    UserProgramFilesCommon = None
    Videos = None
    VideosLibrary = None
    Windows = None


windirs = _WindowsFolders()


def _get_windows_path(description):
    try:
        fid = getattr(_knownpaths.FOLDERID, description)
    except AttributeError:
        search_dict = {fp.lower(): fp for fp in dir(_knownpaths.FOLDERID)}
        fid = getattr(_knownpaths.FOLDERID, search_dict[description.lower()])
    try:
        ret = _knownpaths.get_path(fid)
        return ret
    except _knownpaths.PathNotFoundException:
        return None
