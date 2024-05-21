#!/usr/bin/python3
"""Initialization file for models package"""
from models.engine.file_storage import FileStorage


store_instance = FileStorage()
store_instance.reload()
