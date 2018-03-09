import struct
import sys
from io import BytesIO

WEAPONS = {
    "Faith": b"\xEB\x03\x00\x00",
    "Iron Pipe": b"\xF5\x03\x00\x00",
    "Beastbane": b"\xfc\x03\x00\x00",
    "Phoenix Dagger": b"\x10\x04\x00\x00",
    "Ancient Overlord": b"\x06\x04\x00\x00",
    "Type-40 Sword": b"\x1A\x04\x00\x00",
    "Type-3 Sword": b"\x24\x04\x00\x00",
    "Virtuous Contract": b"\x2E\x04\x00\x00",
    "Cruel Oath": b"\x2F\x04\x00\x00",
    "YoRHa-issue Blade": b"\x38\x04\x00\x00",
    "Machine Sword": b"\x42\x04\x00\x00",
    "Iron Will": b"\xB3\x04\x00\x00",
    "Fang of the Twins": b"\xBD\x04\x00\x00",
    "Beastlord": b"\xC4\x04\x00\x00",
    "Phoenix Sword": b"\xCE\x04\x00\x00",
    "Type-40 Blade": b"\xD8\x04\x00\x00",
    "Type-3 Blade": b"\xE2\x04\x00\x00",
    "Virtuous Treaty": b"\xEC\x04\x00\x00",
    "Cruel Blood Oath": b"\xED\x04\x00\x00",
    "Machine Axe": b"\xF6\x04\x00\x00",
    "Phoenix Lance": b"\x78\x05\x00\x00",
    "Beastcurse": b"\x8C\x05\x00\x00",
    "Dragoon Lance": b"\x96\x05\x00\x00",
    "Spear of the Usurper": b"\xA0\x05\x00\x00",
    "Type-40 Lance": b"\xAA\x05\x00\x00",
    "Type-3 Lance": b"\xB4\x05\x00\x00",
    "Virtuous Dignity": b"\xBE\x05\x00\x00",
    "Cruel Arrogance": b"\xBF\x05\x00\x00",
    "Machine Spear": b"\xC8\x05\x00\x00",
    "Angel's Folly": b"\x68\x06\x00\x00",
    "Demon's Cry": b"\x5E\x06\x00\x00",
    "Type-40 Fists": b"\x4A\x06\x00\x00",
    "Type-3 Fists": b"\x40\x06\x00\x00",
    "Virtuous Grief": b"\x54\x06\x00\x00",
    "Cruel Lament": b"\x55\x06\x00\x00",
    "Machine Heads": b"\x72\x06\x00\x00",
    "Engine Blade": b"\x53\x07\x00\x00",
    "Cypress Stick": b"\x54\x07\x00\x00",
    "Emil Heads": b"\x55\x07\x00\x00",
    " ":b"\xFF\xFF\xFF\xFF",
}


class ItemsMap(object):
    def __init__(self):
        self.name_to_bytes_map = dict()

        for k, v in WEAPONS.items():
            self.name_to_bytes_map[k] = v
			
        self.bytes_to_name_map = dict()	
        for k, v in WEAPONS.items():
            self.bytes_to_name_map[v[:20]] = k

    def __getitem__(self, key):
        if isinstance(key, bytes) or isinstance(key, bytearray):
            return self.bytes_to_name_map.get(bytes(key)[:4], ("Invalid Weapon"))  #self.bytes_to_name_map.get(bytes(key)[:2], "Invalid Item")
        elif isinstance(key, str):
            return self.name_to_bytes_map.get(key, (b"\xFF" * 8, 0))  # self.name_to_bytes_map.get(key, b"\xFF" * 2)

# Format: Item ID (2 bytes) 00 00 00 00 07 00 Amount(1 Bytes) 00 00 00
# Example: B7 03 00 00 00 00 07 00 01 00 00 00
class ItemsRecord(object):
    """Represent a item record"""
    ITEMS_MAP = ItemsMap()
    AVAILABLE_ITEMS = tuple(ITEMS_MAP.name_to_bytes_map.keys())
    EMPTY_RECORD = b"\xFFFF"

    def __init__(self, name, item_id, item_level, item_kills):
        self.name = name
        self.item_id = item_id
        self.item_kills = item_kills
        self.item_level = item_level
        print(item_kills)
    def __str__(self):
        return "<ItemsRecord name:{0} level:{1} kills:{2}>".format(self.item_name, self.item_level, self.item_kills)

    def pack(self):
        """Convert to bytes"""
        #return struct.pack("<4h", self.item_id, 0, 0, 7) + struct.pack("<2b", self.item_count, 0) + struct.pack("<1h", 0)
        asd = struct.pack("<4h", self.item_id, 0, 0) + struct.pack("h", 2,0,0,0) + struct.pack("h", 3,0,0,0) + struct.pack("h", 4,0,0,0) + struct.pack("h", 5,0,0,0)
        return asd

    @staticmethod
    def unpack(bs):
        """ Convert from bytes """
        name = ItemsRecord.ITEMS_MAP[bs]
        record = struct.unpack("<10h", bs)
        if record[0] == record[1] == record[2] == record[3] == -1:
            return ItemsRecord.EMPTY_RECORD
        return ItemsRecord(name, record[0], record[2], record[8])

    @classmethod
    def from_name(cls, name):
        item = cls.ITEMS_MAP[name]
        bs = item[0]
        uq = int(item[1])
        record = struct.unpack("<1h", bs)
        return cls(name, *record, 0, uq)


class WeaponsRecordManager(object):
    SAVE_DATA_ITEMS_OFFSET = 0x31D70
    SAVE_DATA_ITEMS_OFFSET_END = 0x3207C
    SAVE_DATA_ITEMS_SIZE = SAVE_DATA_ITEMS_OFFSET_END - SAVE_DATA_ITEMS_OFFSET
    SAVE_DATA_ITEMS_COUNT = SAVE_DATA_ITEMS_SIZE // 20

    def __init__(self, buf=None):
        if buf is not None:
            self.blocks = bytearray(
                buf[WeaponsRecordManager.SAVE_DATA_ITEMS_OFFSET:WeaponsRecordManager.SAVE_DATA_ITEMS_OFFSET_END])
        else:
            return
        #    self.blocks = bytearray(ItemsRecordManager.SAVE_DATA_CHIPS_SIZE * 20)
        #    self.blocks[0:20] = b"\x22\x01\x00\x00\x0A\x0D\x00\x00\x2A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    def export(self):
        return bytes(self.blocks)

    def get_all_items(self):
        for i in range(self.SAVE_DATA_ITEMS_COUNT):
            yield ItemsRecord.unpack(self.blocks[i * 20: (i + 1) * 20])
            #yield ItemsRecord.unpack(self.blocks[i * 20: i * 20 + 1])

    def get_item_at(self, index):
        if not 0 <= index < WeaponsRecordManager.SAVE_DATA_ITEMS_COUNT:
            raise IndexError
        return ItemsRecord.unpack(self.blocks[index * 20: (index + 1) * 20])

    def set_item_at(self, index, record):
        if not 0 <= index < WeaponsRecordManager.SAVE_DATA_ITEMS_COUNT:
            raise IndexError
        if record == ItemsRecord.EMPTY_RECORD:
            self.blocks[index * 20: (index + 1) * 20] = b"\xFF" * 4 + b"\x00" * 10
        else:
            tmp = record.pack()
            print(tmp)
            print(self.blocks[index * 20: (index + 1) * 20])
            self.blocks[index * 20: (index + 1) * 20] = tmp
            print(self.blocks[index * 20: (index + 1) * 20])

    def __getitem__(self, index):
        return self.get_item_at(index)

    def __setitem__(self, index, item):
        self.set_item_at(index, item)
