import struct
import sys
from item_list import COMMON_ITEMS
from  item_list import UNIQUE_ITEMS


class ItemsMap(object):
    def __init__(self):
        self.name_to_bytes_map = dict()
        self.bytes_to_name_map = dict()
        for k, v in COMMON_ITEMS.items():
            v_swap = struct.pack(">h", struct.unpack("<h", v)[0])
            self.name_to_bytes_map[k] = (v_swap, 0)  # + b"\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00"
            self.bytes_to_name_map[v_swap] = (k, 0)
        for k, v in UNIQUE_ITEMS.items():
            v_swap = struct.pack(">h", struct.unpack("<h", v)[0])
            # v_swap = int.from_bytes(v, byteorder='big').to_bytes(2, byteorder=sys.byteorder)
            self.name_to_bytes_map['[unique]'+k] = (v_swap, 1)  # + b"\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00"
            self.bytes_to_name_map[v_swap] = ('[unique]'+k, 1)

    def __getitem__(self, key):
        if isinstance(key, bytes) or isinstance(key, bytearray):
            return self.bytes_to_name_map.get(bytes(key)[:2], ("Invalid Item", 0))  #self.bytes_to_name_map.get(bytes(key)[:2], "Invalid Item")
        elif isinstance(key, str):
            return self.name_to_bytes_map.get(key, (b"\xFF" * 2, 0))  # self.name_to_bytes_map.get(key, b"\xFF" * 2)


# Format: Item ID (2 bytes) 00 00 00 00 07 00 Amount(1 Bytes) 00 00 00
# Example: B7 03 00 00 00 00 07 00 01 00 00 00
class ItemsRecord(object):
    """Represent a item record"""
    ITEMS_MAP = ItemsMap()
    AVAILABLE_ITEMS = tuple(sorted(ITEMS_MAP.name_to_bytes_map.keys()))
    EMPTY_RECORD = -1

    def __init__(self, name, item_id, item_count, uq):
        self.name = name
        self.item_id = item_id
        self.item_count = item_count
        self.uq = uq

    def __str__(self):
        return "<ItemsRecord name:{0} count:{1}>".format(self.name, self.item_count)

    def pack(self):
        """Convert to bytes"""
        return struct.pack("<4h", self.item_id, 0, 0, 7) + struct.pack("<2b", self.item_count, 0) + struct.pack("<1h", 0)

    @staticmethod
    def unpack(bs):
        """ Convert from bytes """
        item = ItemsRecord.ITEMS_MAP[bs]
        name = item[0]
        uq = int(item[1])
        record = struct.unpack("<6h", bs)
        if record[0] == record[1] == record[2] == record[3] == -1:
            return ItemsRecord.EMPTY_RECORD
        return ItemsRecord(name, record[0], record[4], uq)

    @classmethod
    def from_name(cls, name):
        item = cls.ITEMS_MAP[name]
        bs = item[0]
        uq = int(item[1])
        record = struct.unpack("<1h", bs)
        return cls(name, *record, 0, uq)


class ItemsRecordManager(object):
    SAVE_DATA_ITEMS_OFFSET = 0x30570
    SAVE_DATA_ITEMS_OFFSET_END = 0x31D70
    SAVE_DATA_ITEMS_SIZE = SAVE_DATA_ITEMS_OFFSET_END - SAVE_DATA_ITEMS_OFFSET
    SAVE_DATA_ITEMS_COUNT = SAVE_DATA_ITEMS_SIZE // 12

    def __init__(self, buf=None):
        if buf is not None:
            self.blocks = bytearray(
                buf[ItemsRecordManager.SAVE_DATA_ITEMS_OFFSET:ItemsRecordManager.SAVE_DATA_ITEMS_OFFSET_END])
        else:
            return
        #    self.blocks = bytearray(ItemsRecordManager.SAVE_DATA_CHIPS_SIZE * 12)
        #    self.blocks[0:12] = b"\x22\x01\x00\x00\x0A\x0D\x00\x00\x2A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    def export(self):
        return bytes(self.blocks)

    def get_all_items(self):
        for i in range(self.SAVE_DATA_ITEMS_COUNT):
            yield ItemsRecord.unpack(self.blocks[i * 12: (i + 1) * 12])
            #yield ItemsRecord.unpack(self.blocks[i * 12: i * 12 + 1])

    def get_item_at(self, index):
        if not 0 <= index < ItemsRecordManager.SAVE_DATA_ITEMS_COUNT:
            raise IndexError
        return ItemsRecord.unpack(self.blocks[index * 12: (index + 1) * 12])

    def set_item_at(self, index, record):
        if not 0 <= index < ItemsRecordManager.SAVE_DATA_ITEMS_COUNT:
            raise IndexError
        if record == ItemsRecord.EMPTY_RECORD:
            self.blocks[index * 12: (index + 1) * 12] = b"\xFF" * 8 + b"\x00" * 4
        else:
            tmp = record.pack()
            print(tmp)
            print(self.blocks[index * 12: (index + 1) * 12])
            self.blocks[index * 12: (index + 1) * 12] = tmp
            print(self.blocks[index * 12: (index + 1) * 12])

    def __getitem__(self, index):
        return self.get_item_at(index)

    def __setitem__(self, index, item):
        self.set_item_at(index, item)
