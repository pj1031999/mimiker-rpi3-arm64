#!/usr/bin/env python2

from __future__ import print_function

import os.path
import struct
import argparse
import logging

from array import array
from collections import Mapping


PSF1_MAGIC = '\x36\x04'
PSF1_MODE512 = 0x01
PSF1_MODEHASTAB = 0x02
PSF1_MODEHASSEQ = 0x04
PSF1_SEPARATOR = u'\uFFFF'
PSF1_STARTSEQ = u'\uFFFE'

PSF2_MAGIC = '\x72\xb5\x4a\x86'
PSF2_HAS_UNICODE_TABLE = 0x01
PSF2_SEPARATOR = '\xFF'
PSF2_STARTSEQ = '\xFE'


class PSF(Mapping):
  def __init__(self):
    self.height = 0
    self._char = []
    self._char_map = {}

  def __getitem__(self, key):
    return self._char[self._char_map[key]]

  def __iter__(self):
    return self._char_map.keys()

  def __len__(self):
    return len(self._char_map)

  def readPSF1(self, f):
    mode, self.height = struct.unpack('BB', f.read(2))

    if mode & PSF1_MODE512:
      glyphs = 512
    else:
      glyphs = 256

    self._char = [array('B', f.read(self.height)) for i in range(glyphs)]

    if mode & PSF1_MODEHASTAB:
      index = 0

      while True:
        uchar = f.read(2).decode('utf-16')
        if uchar == '':
          break
        if uchar == PSF1_SEPARATOR:
          index += 1
        else:
          self._char_map[uchar] = index

  def readPSF2(self, f):
    (flags, glyphs, self.height) = struct.unpack('8xIII8x', f.read(28))

    self._char = [array('B', f.read(self.height)) for i in range(glyphs)]

    if flags & PSF2_HAS_UNICODE_TABLE:
      index = 0
      ustr = ''

      while True:
        uchar = f.read(1)
        if uchar == '':
          break
        if uchar == PSF2_SEPARATOR:
          for uchar in ustr.decode('utf-8'):
            self._char_map[uchar] = index
          index += 1
          ustr = ''
        else:
          ustr += uchar

  def fromFile(self, path):
    with open(path) as f:
      if f.read(2) == PSF1_MAGIC:
        return self.readPSF1(f)
      logging.info('Data does not start with PSF1 magic prefix.')

    with open(path) as f:
      if f.read(4) == PSF2_MAGIC:
        return self.readPSF2(f)
      logging.info('Data does not start with PSF2 magic prefix.')

    raise SystemExit('"%s" is not PC Screen Font file!')


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

  parser = argparse.ArgumentParser(
    description='Convert PSF font file to PNG image.')
  parser.add_argument('input', metavar='INPUT', type=str,
                      help='PC Screen Font file.')
  args = parser.parse_args()

  if not os.path.isfile(args.input):
    raise SystemExit('Input file does not exists!')

  output = os.path.splitext(args.input)[0] + '.png'

  psf = PSF()
  psf.fromFile(args.input)

  fontname = os.path.splitext(args.input)[0].replace('-', '_')

  print('#include "font.h"')
  print('')
  print('static uint8_t _char[%d][%d] = {' % (len(psf._char), psf.height))
  for i, data in enumerate(psf._char):
    print('  {' + ', '.join(map(lambda x: '0x%02x' % x, data)) + '},')
  print('};')
  print('')
  print('font_t %s = {' % fontname)
  print('  .width = %d,' % 8)
  print('  .height = %d,' % psf.height)
  print('  .map = {')
  for char, index in sorted(psf._char_map.items()):
    print('    {.code = 0x%04x, .data = _char[%d]},' % (ord(char), index))
  print('  }')
  print('};')

# vim:expandtab ts=2 sw=2:
