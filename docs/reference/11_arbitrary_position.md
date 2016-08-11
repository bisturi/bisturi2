Until now, all our fields in a packet are packed/unpacked sequentially.
This is fine, but in some cases it is desired to control where a field begins.

```python
>>> from bisturi.packet import Packet
>>> from bisturi.field  import Data, Int 

>>> class Folder(Packet):
...   offset_of_file = Int(1)
...
...   file_data = Data(4).at(offset_of_file) # TODO revisar el default de esto

```

The data between 'offset_of_file' and 'file_data' is saved in an internal field
that can be accessed and modified: '_shift_to_file_data'.
The name will have the form of '_shift_to_...'.

```python
>>> s = '\x04XXXABCD'
>>> p = Folder(s)

>>> p.offset_of_file
4

>>> p._shift_to_file_data
'XXX'

>>> p.file_data
'ABCD'

```

```python
>>> p = Folder(offset_of_file=1)

>>> p.offset_of_file
1
>>> p._shift_to_file_data
''
>>> p.file_data
'\x00\x00\x00\x00'
>>> str(p.pack())
'\x01\x00\x00\x00\x00'

>>> p = Folder(offset_of_file=4, file_data='ABCD')
>>> str(p.pack())
'\x04...ABCD'

>>> p._shift_to_file_data = 'XX'
>>> str(p.pack())
'\x04XX.ABCD'

```

Moving to back is possible too, even reading the same piece of raw data already
parsed by another field, but at the packing time you will receive an error.
We can't know how to put two diferent set of data at the same position!

```python

>>> class Folder(Packet):
...   offset_of_file = Int(1)
...   
...   payload   = Data(8)
...   file_data = Data(4).at(offset_of_file) # TODO revisar el default de esto

```

```python
>>> s = '\x04XXXABCDX'
>>> p = Folder(s)

>>> p.offset_of_file
4

>>> p.payload
'XXXABCDX'

>>> p._shift_to_file_data
''

>>> p.file_data
'ABCD'

```

So good so far, but if we try to pack this...

```python
>>> p = Folder(offset_of_file=4, file_data='ABCD')

>>> p.offset_of_file
4
>>> p.payload
'\x00\x00\x00\x00\x00\x00\x00\x00'

>>> p._shift_to_file_data
''

>>> p.file_data
'ABCD'

>>> p.pack()                                # doctest: +ELLIPSIS
Traceback (most recent call last):
Exception: Error when packing field 'file_data' of packet Folder at 00000004...Collision detected with previous fragment 00000000-00000009...

```

The problem is that the file_data is trying to put its packed data in the same place where the data of payload is already there.
For that reason we get an exception.
