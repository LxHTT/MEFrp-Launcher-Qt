from PyQt5.QtCore import qVersion, qRegisterResourceData, qUnregisterResourceData

qt_resource_data = b"\
\x00\x00\x00\x9a\
\x51\
\x4c\x61\x62\x65\x6c\x23\x74\x69\x74\x6c\x65\x4c\x61\x62\x65\x6c\
\x20\x7b\x0d\x0a\x20\x20\x20\x20\x62\x61\x63\x6b\x67\x72\x6f\x75\
\x6e\x64\x3a\x20\x74\x72\x61\x6e\x73\x70\x61\x72\x65\x6e\x74\x3b\
\x0d\x0a\x20\x20\x20\x20\x66\x6f\x6e\x74\x3a\x20\x31\x33\x70\x78\
\x20\x27\x53\x65\x67\x6f\x65\x20\x55\x49\x27\x2c\x20\x27\x4d\x69\
\x63\x72\x6f\x73\x6f\x66\x74\x20\x59\x61\x48\x65\x69\x27\x2c\x20\
\x27\x50\x69\x6e\x67\x46\x61\x6e\x67\x20\x53\x43\x27\x3b\x0d\x0a\
\x20\x20\x20\x20\x70\x61\x64\x64\x69\x6e\x67\x3a\x20\x30\x20\x34\
\x70\x78\x3b\x0d\x0a\x20\x20\x20\x20\x63\x6f\x6c\x6f\x72\x3a\x20\
\x77\x68\x69\x74\x65\x3b\x0d\x0a\x7d\
\x00\x00\x00\x99\
\x51\
\x4c\x61\x62\x65\x6c\x23\x74\x69\x74\x6c\x65\x4c\x61\x62\x65\x6c\
\x20\x7b\x0d\x0a\x20\x20\x20\x20\x63\x6f\x6c\x6f\x72\x3a\x20\x62\
\x6c\x61\x63\x6b\x3b\x0d\x0a\x20\x20\x20\x20\x62\x61\x63\x6b\x67\
\x72\x6f\x75\x6e\x64\x3a\x20\x74\x72\x61\x6e\x73\x70\x61\x72\x65\
\x6e\x74\x3b\x0d\x0a\x20\x20\x20\x20\x66\x6f\x6e\x74\x3a\x20\x31\
\x33\x70\x78\x20\x27\x53\x65\x67\x6f\x65\x20\x55\x49\x27\x2c\x20\
\x27\x4d\x69\x63\x72\x6f\x73\x6f\x66\x74\x20\x59\x61\x48\x65\x69\
\x27\x2c\x20\x27\x50\x69\x6e\x67\x46\x61\x6e\x67\x20\x53\x43\x27\
\x3b\x0d\x0a\x20\x20\x20\x20\x70\x61\x64\x64\x69\x6e\x67\x3a\x20\
\x30\x20\x34\x70\x78\x0d\x0a\x7d\
"

qt_resource_name = b"\
\x00\x0b\
\x07\xcf\xb8\xc3\
\x00\x62\
\x00\x75\x00\x69\x00\x6c\x00\x74\x00\x2d\x00\x49\x00\x6e\x00\x51\x00\x73\x00\x73\
\x00\x12\
\x0d\x60\x19\x03\
\x00\x74\
\x00\x69\x00\x74\x00\x6c\x00\x65\x00\x5f\x00\x62\x00\x61\x00\x72\x00\x5f\x00\x64\x00\x61\x00\x72\x00\x6b\x00\x2e\x00\x71\x00\x73\
\x00\x73\
\x00\x13\
\x00\xd3\x33\xe3\
\x00\x74\
\x00\x69\x00\x74\x00\x6c\x00\x65\x00\x5f\x00\x62\x00\x61\x00\x72\x00\x5f\x00\x6c\x00\x69\x00\x67\x00\x68\x00\x74\x00\x2e\x00\x71\
\x00\x73\x00\x73\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\
\x00\x00\x00\x46\x00\x00\x00\x00\x00\x01\x00\x00\x00\x9e\
\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x46\x00\x00\x00\x00\x00\x01\x00\x00\x00\x9e\
\x00\x00\x01\x8d\x06\x82\xe3\x32\
\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x8d\x06\x82\xd9\x8e\
"

qt_version = [int(v) for v in qVersion().split(".")]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2


def qInitResources():
    qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)


def qCleanupResources():
    qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)


qInitResources()
