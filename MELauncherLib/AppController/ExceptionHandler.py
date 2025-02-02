#     Copyright 2025, MCSL Team, mailto:services@mcsl.com.cn
#
#     Part of "MCSL2", a simple and multifunctional Minecraft server launcher.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/MCSLTeam/MCSL2/raw/master/LICENSE
#
################################################################################

import enum
from types import TracebackType
from typing import Type


class ExceptionFilterMode(enum.Enum):
    RAISE_AND_PRINT = enum.auto()  # 过滤：弹框提示，也会抛出异常
    RAISE = enum.auto()  # 过滤：不弹框提示，但是会抛出异常
    PASS = enum.auto()  # 过滤：不弹框提示，也不抛出异常，就当做什么都没发生


def exceptionFilter(
    ty: Type[BaseException], value: BaseException, _traceback: TracebackType
) -> ExceptionFilterMode:
    """
    过滤异常
    """
    if isinstance(value, AttributeError) and "MessageBox" in str(value):
        return ExceptionFilterMode.PASS
        return ExceptionFilterMode.RAISE
    if isinstance(value, RuntimeError) and "wrapped C/C++ object of type" in str(value):
        return ExceptionFilterMode.PASS
    if isinstance(value, Exception) and "raise test" in str(value):
        return ExceptionFilterMode.RAISE
    if isinstance(value, Exception) and "pass test" in str(value):
        return ExceptionFilterMode.PASS
    if isinstance(value, Exception) and "print test" in str(value):
        return ExceptionFilterMode.RAISE_AND_PRINT

    return ExceptionFilterMode.RAISE_AND_PRINT
