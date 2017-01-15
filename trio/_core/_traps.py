# These are the only 3 functions that ever yield back to the task runner.

import types
import enum

from . import _hazmat

__all__ = ["yield_briefly", "yield_briefly_no_cancel", "Cancel"]

@_hazmat
@types.coroutine
def yield_briefly():
    return (yield (yield_briefly,))

@_hazmat
@types.coroutine
def yield_briefly_no_cancel():
    return (yield (yield_briefly_no_cancel,))

# Return values for cancel functions
@_hazmat
class Cancel(enum.Enum):
    SUCCEEDED = 1
    FAILED = 2

# This one is so tricky to use that we don't even make it a hazmat function;
# we only use it internally within this module. ParkingLot provides a much
# more pleasant abstraction on top of it.
#
# Basically, before calling this make arrangements for the current task to be
# rescheduled "eventually".
#
# cancel_func gets called if we want to cancel the wait (e.g. a
# timeout). It should attempt to cancel whatever arrangements were made, and
# must return either Interupt.SUCCEEDED, in which case the task will be
# rescheduled immediately with the exception raised, or else Cancel.FAILED,
# in which case no magic happens and you still have to make sure that
# reschedule will be called eventually.
@types.coroutine
def yield_indefinitely(cancel_func):
    return (yield (yield_indefinitely, cancel_func))