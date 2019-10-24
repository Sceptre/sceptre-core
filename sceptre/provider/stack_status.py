# -*- coding: utf-8 -*-

"""
sceptre.provider.stack_status

This module implemets structs for simplified Stack status and simplified
ChangeSet status values.
"""


class StackStatus:
    """
    StackStatus stores simplified Stack statuses.
    """
    COMPLETE = "complete"
    FAILED = "failed"
    IN_PROGRESS = "in progress"
    PENDING = "pending"


class StackChangeSetStatus:
    """
    StackChangeSetStatus stores simplified ChangeSet statuses.
    """
    PENDING = "pending"
    READY = "ready"
    DEFUNCT = "defunct"
