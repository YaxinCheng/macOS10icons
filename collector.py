import plistlib
import os
import shutil

entry = [
        '/Applications',
        '/System/Applications',
        "/System/Library/CoreServices/Applications", 
        ]

ID_KEY = 'CFBundleIdentifier'
ICON_KEY = 'CFBundleIconFile'
APPLE_BUNDLE_ID_PREFIX = 'com.apple'

class Application:
    def __init__(self, path, bundleId, icon):
        self.path = path
        self.bundleId = bundleId
        self.icon = icon

def createVerifyApp(path):
    plistPath = path + '/Contents/info.plist'
    if not os.path.exists(plistPath): return None
    with open(plistPath, 'rb') as plistFile:
        plist = plistlib.loads(plistFile.read())
    bundleId = plist[ID_KEY]
    if not bundleId.startswith(APPLE_BUNDLE_ID_PREFIX): return None
    iconName = plist[ICON_KEY].replace('.icns', '')
    return Application(path, bundleId, iconName + '.icns')

FINDER = createVerifyApp("/System/Library/CoreServices/Finder.app")

def collectAppleApps(entry):
    queue = entry
    apps = []
    while queue:
        path = queue.pop(0)
        for fileName in os.listdir(path):
            filePath = path + '/' + fileName
            if fileName.endswith('.app'):
                app = createVerifyApp(filePath)
                if app: apps.append(app)
            elif os.path.isdir(filePath):
                queue.append(filePath)
    return apps

appleApps = collectAppleApps(entry) + [FINDER]

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def createFolders(apps):
    mkdir('docs')
    for app in apps:
        targetPath = 'docs/' + app.bundleId
        mkdir(targetPath)
        iconPath = app.path + '/Contents/Resources/' + app.icon
        shutil.copy(iconPath, targetPath)

createFolders(appleApps)
