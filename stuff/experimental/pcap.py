import sys
sys.path.append(".")

from bisturi.packet import Packet
from bisturi.field  import Int, Data, Ref


class Header(Packet):
    __bisturi__ = {'endianness': 'little'}
    magic = Int(4, default=0xa1b2c3d4)
    major = Int(2)
    minor = Int(2)

    thiszone = Int(4, signed=True)
    sigfigs = Int(4)

    spanlen = Int(4)
    network = Int(4, default=1)

    def is_swap_needed(self):
        return self.magic in (0xd4c3b2a1, 0x4d3cb2a1)

    def has_nsec_resolution(self):
        return self.magic in (0xa1b23c4d, 0x4d3cb2a1)

class Record(Packet):
    __bisturi__ = {'endianness': 'little'}
    ts_sec  = Int(4)
    ts_usec = Int(4)

    incl_len = Int(4)
    orig_len = Int(4)

    raw_packet = Data(incl_len)

class PcapFile(Packet):
    header  = Ref(Header, embeb=True)
    records = Ref(Record).repeated(until=lambda raw, offset, **k: len(raw) - offset <= 0)


if __name__ == '__main__':
    from base64 import b16decode

    # from arp-storm.pcap, https://wiki.wireshark.org/SampleCaptures
    raw_file = b16decode(b'D4C3B2A1020004000000000000000000FFFF00000100000021A96241903304003C0000003C000000FFFFFFFFFFFF00070DAFF4540806000108000604000100070DAFF45418A6AC0100000000000018A6AD9F06010400000000020100030200000501030121A96241B2B405003C0000003C000000FFFFFFFFFFFF00070DAFF4540806000108000604000100070DAFF45418A6AC0100000000000018A6AC8D01000010000100000000000020434B41414121A96241A9E305003C0000003C000000FFFFFFFFFFFF00070DAFF4540806000108000604000100070DAFF45418A6AC0100000000000018A6ADA102010400000005020100030200000501010221A96241DF6E07003C0000003C000000FFFFFFFFFFFF00070DAFF4540806000108000604000100070DAFF454411C4E01000000000000411C4E4C01000010000100000000000020434B41414121A96241388207003C0000003C000000FFFFFFFFFFFF00070DAFF4540806000108000604000100070DAFF45418A6AC0100000000000018A6ADA301010400000000020100030200000501030321A9624155E608003C0000003C000000FFFFFFFFFFFF00070DAFF4540806000108000604000100070DAFF45418A6AC0100000000000018A6AF7B02010400000000020100030200000501030121A96241513E09003C0000003C000000FFFFFFFFFFFF00070DAFF4540806000108000604000100070DAFF45418A6AC0100000000000018A6ADA501010400000000020111030200000501030321A962417C6F0A003C0000003C000000FFFFFFFFFFFF00070DAFF4540806000108000604000100070DAFF45418A6AC0100000000000018A6AF5204010400000000020100030200000501030121A9624150250B003C0000003C000000FFFFFFFFFFFF00070DAFF4540806000108000604000100070DAFF454454CD801000000000000454CDC8301010400000000020100030200000501030121A962419AA00B003C0000003C000000FFFFFFFFFFFF00070DAFF4540806000108000604000100070DAFF45418A6AC0100000000000018A6ADA8010104000000000201000302000005010301', True)
    pcap_file = PcapFile.unpack(raw_file)

    import bisturi.util as _utils
    _utils.inspect(pcap_file)

