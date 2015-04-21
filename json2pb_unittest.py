#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Note that json2pb.py does not support protobuf extension yet.
#
import json2pb
import simplejson as json
import test_pb2
import unittest
from google.protobuf import text_format

json_string = """
{
  "_str": "b",
  "_bin": "0a0a0a0a",
  "_bool": true,
  "_float": 1,
  "sub": {
    "field": "subfield",
    "echo": [
     {"text": "first"},
     {"text": "second"}
    ]
  },
  "_int": [10, 20, 30, 40],
  "_enum":  [10, 20],
  "str_list":["v0", "v1"],
  "test.e_bool":false
}
"""

proto_string = """
_str: "b"
_float: 1
_int: 10
_int: 20
_int: 30
_int: 40
_bin: "\321\255\032\321\255\032"
_bool: true
sub {
  field: "subfield"
  echo {
    text: "first"
  }
  echo {
    text: "second"
  }
}
_enum: VALUE1
_enum: VALUE2
str_list: "v0"
str_list: "v1"
"""

class TestJson2Pb(unittest.TestCase):
    def test_conversion(self):
        json_msg = test_pb2.ComplexMessage()
        json_msg.ParseFromJSON(json_string)

        proto_msg = test_pb2.ComplexMessage()
        text_format.Parse(proto_string, proto_msg)

        self.assertEqual(json_msg, proto_msg)

    def test_byte_base64(self):
        json_msg = test_pb2.ComplexMessage()
        json_msg.ParseFromJSON(json_string)
        json_dict = json.loads(json_string)

        json_msg_string = json_msg.SerializeToJSON()
        json_msg_dict = json.loads(json_msg_string);

        self.assertEqual(json_msg_dict['_bin'], json_dict['_bin'])
