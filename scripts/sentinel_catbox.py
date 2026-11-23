#!/usr/bin/env python3
import sys
import os

# Adiciona o diretório atual ao sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from catbox_sentinel import main

if __name__ == '__main__':
    main()
