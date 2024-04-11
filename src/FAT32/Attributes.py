import os

class Attributes:
    READ_ONLY = 0x01
    HIDDEN = 0x02
    SYSTEM = 0x04
    VOLUME_LABEL = 0x08
    DIRECTORY = 0x10
    ARCHIVE = 0x20

    NAMES = {
        READ_ONLY: 'Read-only',
        HIDDEN: 'Hidden',
        SYSTEM: 'System',
        VOLUME_LABEL: 'Volume Label',
        DIRECTORY: 'Directory',
        ARCHIVE: 'Archive'
    }