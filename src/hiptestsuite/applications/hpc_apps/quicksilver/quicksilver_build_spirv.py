# Copyright (c) 2021 Advanced Micro Devices, Inc. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import tempfile
import os
from hiptestsuite.common.hip_shell import execshellcmd_largedump, execshellcmd
from hiptestsuite.applications.hpc_apps.quicksilver.quicksilver_parser_common import QuicksilverParser

class BuildRunSpirv():
    def __init__(self, thistestpath, logFile):
        self.thistestpath = thistestpath
        self.logFile = logFile
        self.resultlogFile = None
        self.runlog = ""

    def buildtest(self):
        # In this function put the build steps for test cases
        # which differ across platforms (amd/nvidia/intel)
        print("Building Quicksilver..")
        # if not os.path.exists("/opt/rocm"):
        #     print("Rocm backend is not installed under /opt/. Exiting Test!")
        #     return False
        env = "export ROCM_PATH=${HIP_PATH};"
        cmdcd = "cd " + self.thistestpath + ";"
        cmd_build = "cd src; make -j;"
        cmdexc = env + cmdcd + cmd_build
        runlogdump = tempfile.TemporaryFile("w+")
        execshellcmd_largedump(cmdexc, self.logFile, runlogdump, None)
        runlogdump.close()
        if not os.path.exists(os.path.join(self.thistestpath, "src/qs")):
            print("Quicksilver Build Failed. Exiting Test!")
            return False
        return True

    def runtest(self):
        print("Running Quicksilver Test..")
        cmdcd = "cd " + self.thistestpath + ";" + "cd src;"
        cmdrun = "./qs -i ../Examples/CORAL2_Benchmark/Problem1/Coral2_P1.inp -X 16 -Y 16 -Z 16 -x 16 -y 16 -z 16 -I 1 -J 1 -K 1 -b 2 -n 2621440;"
        cmdexc = cmdcd + cmdrun
        self.resultlogFile = tempfile.TemporaryFile("w+")
        execshellcmd_largedump(cmdexc, self.logFile, self.resultlogFile, None)

    def clean(self):
        print("Cleaning Quicksilver..")
        if self.resultlogFile != None:
            self.resultlogFile.close()
        cmdcd = "cd " + self.thistestpath + ";" + "cd src;"
        cmdrm = "make clean;"
        cmdexc = cmdcd + cmdrm
        execshellcmd(cmdexc, None, None)

    def parse_result(self):
        return QuicksilverParser(self.resultlogFile).parse()
