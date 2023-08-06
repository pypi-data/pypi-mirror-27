# -*- coding: utf-8 -*-

#
# Copyright (C) 2013-2017 Red Hat, Inc.
#	This copyrighted material is made available to anyone wishing to use,
#  modify, copy, or redistribute it subject to the terms and conditions of
#  the GNU General Public License v.2.
#
#	This application is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#	General Public License for more details.
#
# Authors:
#	Guy Streeter <guy.streeter@gmail.com>
#
__package_name = 'python-libnuma'
__author = 'Guy Streeter'
__author_email = 'guy.streeter@gmail.com'
__license = 'GPLv2+'
__version = '2.2'
__description = 'Python bindings for libnuma'
__URL = 'https://git.fedorahosted.org/cgit/python-libnuma.git/'

from posix.unistd cimport pid_t
from libc.stdlib cimport malloc as CMalloc
from libc.stdlib cimport free as CFree
from libc.errno cimport errno as CErrno
from libc.string cimport strerror as CStrerror

import gettext
try:
    # for un-installed testing...
    import os.path
    try:
        ld = os.path.dirname(__file__)+'/../po'
        if not os.path.isdir(ld):
            ld = None
    except:
        ld = None
    t = gettext.translation('python-libnuma', ld, fallback=True)
    _ = t.gettext
except IOError as e:
    print(str(e))
    def _(_s):
        return _s

from cpython cimport PY_MAJOR_VERSION

def _utfate(text):
    if isinstance(text, unicode):
        return text.encode('utf8')
    if (PY_MAJOR_VERSION < 3) and isinstance(text, str):
        return text.decode('ASCII')
    # TRANSLATORS: An internal error from unexpected libnuma returned string
    raise ValueError(_("requires text input, got %s") % type(text))

class NumaError(Exception):
    pass

class Unimplemented(NumaError):
    pass

class ParseError(NumaError):
    def __init__(self, line):
        # TRANSLATORS: an error parsing a CPU list supplied to the Bitmask class
        self.msg = _('error parsing line:\n{line}').format(line=line)
    def __str__(self):
        return self.msg

cdef extern from "numa.h":

    struct bitmask:
        pass

    bint numa_available()

    int numa_max_possible_node()
    int numa_num_possible_nodes()

    int numa_max_node()
    int numa_num_configured_nodes()
    bitmask *numa_get_mems_allowed()

    int numa_num_configured_cpus()
    bitmask *numa_all_nodes_ptr
    bitmask *numa_no_nodes_ptr
    bitmask *numa_all_cpus_ptr

    int numa_num_task_cpus()
    int numa_num_task_nodes()

    bitmask *numa_parse_nodestring(char *string)
    bitmask *numa_parse_cpustring(char *string)

    long numa_node_size(int node, long *freep)
    long long numa_node_size64(int node, long long *freep)

    int numa_preferred()
    void numa_set_preferred(int node)
    int numa_get_interleave_node()
    bitmask *numa_get_interleave_mask()
    void numa_set_interleave_mask(bitmask *nodemask)
    void  numa_interleave_memory(void  *start,  size_t size, bitmask *nodemask)
    void numa_bind(bitmask *nodemask)
    void numa_set_localalloc()
    void numa_set_membind(bitmask *nodemask)
    bitmask *numa_get_membind()

    void *numa_alloc_onnode(size_t size, int node)
    void *numa_alloc_local(size_t size)
    void *numa_alloc_interleaved(size_t size)
    void *numa_alloc_interleaved_subset(size_t size,  bitmask *nodemask)
    void *numa_alloc(size_t size)
    void *numa_realloc(void *old_addr, size_t old_size, size_t new_size)
    void numa_free(void *start, size_t size)

    int numa_run_on_node(int node)
    int numa_run_on_node_mask(bitmask *nodemask)
    bitmask *numa_get_run_node_mask()

    void numa_tonode_memory(void *start, size_t size, int node)
    void numa_tonodemask_memory(void *start, size_t size, bitmask *nodemask)
    void numa_setlocal_memory(void *start, size_t size)
    void numa_police_memory(void *start, size_t size)
    void numa_set_bind_policy(int strict)
    void numa_set_strict(int strict)

    int numa_distance(int node1, int node2)

    int numa_sched_getaffinity(pid_t pid, bitmask *mask)
    int numa_sched_setaffinity(pid_t pid, bitmask *mask)
    int numa_node_to_cpus(int node, bitmask *mask)
    int numa_node_of_cpu(int cpu)

    bitmask *numa_allocate_cpumask()
    void numa_free_cpumask()

    bitmask *numa_allocate_nodemask() # library calls exit(1) on error
    void numa_free_nodemask()

    bitmask *numa_bitmask_alloc(unsigned int n) # library calls exit(1) on error
    bitmask *numa_bitmask_clearall(bitmask *bmp)
    bitmask *numa_bitmask_clearbit(bitmask *bmp, unsigned int n)
    bint numa_bitmask_equal(const bitmask *bmp1, const bitmask *bmp2)
    void numa_bitmask_free(bitmask * bmp)
    int numa_bitmask_isbitset(const bitmask *bmp, unsigned int n)
    unsigned int numa_bitmask_nbytes(bitmask *bmp)
    bitmask *numa_bitmask_setall(bitmask *bmp)
    bitmask *numa_bitmask_setbit(bitmask *bmp, unsigned  int n)
    void  copy_bitmask_to_bitmask(bitmask *bmpfrom, bitmask *bmpto)
    unsigned int numa_bitmask_weight(const bitmask *bmp)

    int numa_move_pages(int pid, unsigned long count, void **pages, const int *nodes, int *status, int flags)
    int numa_migrate_pages(int pid, bitmask *fromnodes, bitmask *tonodes)

    void numa_error(char *where)

    extern int numa_exit_on_error
    extern int numa_exit_on_warn
    void numa_warn(int number, char *where, ...)

def Available():
    return True # numa_available()

def MaxPossibleNode():
    return numa_max_possible_node()

def NumPossibleNodes():
    return numa_num_possible_nodes()

def NodeOfCpu(cpu):
    return numa_node_of_cpu(cpu)

def MaxNode():
    return numa_max_node()

def NumConfiguredNodes():
    return numa_num_configured_nodes()

def NumConfiguredCpus():
    return numa_num_configured_cpus()

cdef class BPtr:
    cdef bitmask* ptr

    def Ptr(self):
        return int(<unsigned long>self.ptr)

    cdef NewPtr(self, bitmask* newmask):
        if self.ptr != NULL:
            raise NumaError
        self.ptr = newmask

    def SetPtr(self, unsigned long ptr):
        self.NewPtr(<bitmask*>ptr)

    def __dealloc__(self):
        if not self.isnull:
            numa_bitmask_free(self.ptr)
            self.ptr = NULL

#	def __str__(self):
#		return '0x%lX' % (<unsigned long>self.ptr,)

    property isnull:
        def __get__(self):
            return self.ptr == NULL

    property weight:
        def __get__(self):
            return numa_bitmask_weight(self.ptr)

    def __nonzero__(self):
        return bool(self.weight)

    def iszero(self):
        return not self.__nonzero__()

    def clearall(self):
        numa_bitmask_clearall(self.ptr)

    def clearbit(self, unsigned int n):
        numa_bitmask_clearbit(self.ptr, n)

    def __richcmp__(BPtr self, BPtr other not None, op):
        if op not in [2,3]:
            raise NumaError
        res = numa_bitmask_equal(<bitmask*>self.ptr, <bitmask*>other.ptr)
        if op == 2:
            return res
        return not res

    def isbitset(self, unsigned int n):
        return numa_bitmask_isbitset(self.ptr, n)

    property nbytes:
        def __get__(self):
            return numa_bitmask_nbytes(self.ptr)

    def setall(self):
        numa_bitmask_setall(self.ptr)

    def setbit(self, unsigned int n):
        numa_bitmask_setbit(self.ptr, n)

    property size:
        def __get__(self):
            if self.isnull:
                return 0
            return self.nbytes * sizeof(char)

    property all_set_bits:
        def __get__(self):
            for i in range(self.size):
                if self.isbitset(i):
                    yield i

cdef class Bitmask(BPtr):
    def __init__(self, nodestring=None, cpustring=None):
        if nodestring is not None:
            nodestring = _utfate(nodestring)
            self.ptr = numa_parse_nodestring(nodestring)
            if self.ptr == NULL:
                raise ParseError(nodestring)
            return
        if cpustring is not None:
            cpustring = _utfate(cpustring)
            self.ptr = numa_parse_cpustring(cpustring)
            if self.ptr == NULL:
                raise ParseError(cpustring)
            return

cdef class StaticBPtr(Bitmask):
    def __dealloc__(self):
        self.ptr = NULL

cdef BPtr _newSB(bitmask* ptr):
    bp = StaticBPtr()
    bp.NewPtr(ptr)
    return bp

def GetMemsAllowed():
    b = Bitmask()
    b.NewPtr(numa_get_mems_allowed())
    return b

AllNodes = _newSB(numa_all_nodes_ptr)
NoNodes = _newSB(numa_no_nodes_ptr)
AllCpus = _newSB(numa_all_cpus_ptr)

def AllocateNodemask():
    n = Bitmask()
    n.NewPtr(<bitmask*>numa_allocate_nodemask())
    return n

def Alloc(size_t size):
    return <unsigned long>numa_alloc(size)

def Free(unsigned long start, size_t size):
    numa_free(<void *>start, size)

def Realloc(unsigned long old_addr, size_t old_size, size_t new_size):
    return <unsigned long>numa_realloc(<void *>old_addr, old_size, new_size)

def AllocInterleaved(size_t size):
    return <unsigned long>numa_alloc_interleaved(size)

def AllocInterleavedSubset(size_t size, BPtr nodemask):
    return <unsigned long>numa_alloc_interleaved_subset(size, nodemask.ptr)

def AllocOnnode(size_t size, int node):
    return <unsigned long>numa_alloc_onnode(size, node)

def Bind(BPtr bitmask):
    numa_bind(bitmask.ptr)

def BitmaskAlloc(int n):
    b = Bitmask()
    b.NewPtr(numa_bitmask_alloc(n))
    return b

def BitmaskClearall(BPtr bmp):
    numa_bitmask_clearall(bmp.ptr)

def BitmaskClearbit(BPtr bmp, int n):
    numa_bitmask_clearbit(bmp.ptr, n)

def BitmaskEqual(BPtr bmp1, BPtr bmp2):
    return numa_bitmask_equal(bmp1.ptr, bmp2.ptr)

def BitmaskIsbitset(BPtr bmp, int n):
    return numa_bitmask_isbitset(bmp.ptr, n)

def BitmaskNbytes(BPtr bmp):
    return numa_bitmask_nbytes(bmp.ptr)

def BitmaskSetall(BPtr bmp):
    numa_bitmask_setall(bmp.ptr)

def BitmaskSetbit(BPtr bmp, int n):
    numa_bitmask_setbit(bmp.ptr, n)

def BitmaskToNodeMask(BPtr bmp):
    raise Unimplemented

def NodemaskToBitmask(unsigned long nodemask, int size=0):
    raise Unimplemented

def CopyBitmask(BPtr bmpfrom, int size=0):
    if size == 0:
        size = bmpfrom.size
    bmpto = <Bitmask>BitmaskAlloc(size)
    copy_bitmask_to_bitmask(bmpfrom.ptr, bmpto.ptr)
    return bmpto

def BitmaskWeight(BPtr bmp):
    return numa_bitmask_weight(bmp.ptr)

def RunOnNode(int node):
    if numa_run_on_node(node) == -1:
        raise OSError(CErrno, CStrerror(CErrno))

def RunOnNodeMask(BPtr nodemask):
    if numa_run_on_node_mask(nodemask.ptr) == -1:
        raise OSError(CErrno, CStrerror(CErrno))

def GetRunNodeMask():
    b = numa_get_run_node_mask()
    bp = Bitmask()
    bp.NewPtr(b)
    return bp

def TonodeMemory(unsigned long start, size_t size, int node):
    numa_tonode_memory(<void*>start, size, node)

def TonodemaskMemory(unsigned long start, size_t size, BPtr nodemask):
    numa_tonodemask_memory(<void*>start, size, nodemask.ptr)

def SetlocalMemory(unsigned long start, size_t size):
    numa_setlocal_memory(<void*>start, size)

def PoliceMemory(unsigned long start, size_t size):
    numa_police_memory(<void*>start, size)

def SetBindPolicy(int strict):
    numa_set_bind_policy(strict)

def SetStrict(int strict):
    numa_set_strict(strict)

def Distance(int node1, int node2):
    d = numa_distance(node1, node2)
    if d == 0:
        raise OSError(CErrno, CStrerror(CErrno))
    return d

def SchedGetaffinity(pid):
    c = <Bitmask>AllocateCpumask()
    numa_sched_getaffinity(pid, c.ptr)
    return c

def SchedSetaffinity(int pid, BPtr mask):
    if numa_sched_setaffinity(pid, mask.ptr) == -1:
        raise OSError(CErrno, CStrerror(CErrno))

def AllocateCpumask():
    b = numa_allocate_cpumask()
    bp = Bitmask()
    bp.NewPtr(b)
    return bp

def NodeToCpus(int node):
    c = <Bitmask>AllocateCpumask()
    if numa_node_to_cpus(node, c.ptr) == -1:
        raise OSError(CErrno, CStrerror(CErrno))
    return c

def NodeOfCpu(int cpu):
    return numa_node_of_cpu(cpu)

def GetExitOnError():
    global numa_exit_on_error
    return int(numa_exit_on_error != 0)

def SetExitOnError(val=True):
    global numa_exit_on_error
    if val:
        numa_exit_on_error = 1
    else:
        numa_exit_on_error = 0

def GetExitOnWarn():
    global numa_exit_on_warn
    return numa_exit_on_warn != 0

def SetExitOnWarn(val=True):
    global numa_exit_on_warn
    if val:
        numa_exit_on_warn = 1
    else:
        numa_exit_on_warn = 0

def GetInterleaveMask():
    b = numa_get_interleave_mask()
    bp = Bitmask()
    bp.NewPtr(b)
    return bp

def SetInterleaveMask(BPtr bitmask):
    numa_set_interleave_mask(bitmask.ptr)

def InterleaveMemory(unsigned long start, size_t size, BPtr bitmask):
    numa_interleave_memory(<void*>start, size, bitmask.ptr)

def Bind(BPtr bitmask):
    numa_bind(bitmask.ptr)

def SetLocalalloc():
    numa_set_localalloc()

def SetMembind(BPtr bitmask):
    numa_set_membind(bitmask.ptr)

def GetMembind():
    b = numa_get_membind()
    bp = Bitmask()
    bp.NewPtr(b)
    return bp

def BitmaskWeight(BPtr bmp):
    return numa_bitmask_weight(bmp.ptr)

def MovePages(int pid, pages, nodes, int flags):
    cdef int count = len(pages)
    assert count <= len(nodes)
    cdef void** p = <void**>CMalloc(count * sizeof(void*))
    cdef int* n = <int*>CMalloc(count * sizeof(int))
    cdef int* s = <int*>CMalloc(count * sizeof(int))
    for i in range(count):
        p[i] = <void*>pages[i]
        n[i] = nodes[i]
        s[i] = 0
    if numa_move_pages(pid, count, p, n, s, flags) == -1:
        raise OSError(CErrno, CStrerror(CErrno))
    statuses = []
    for i in range(count):
        statuses.append(int(s[i]))
    CFree(p)
    CFree(n)
    CFree(s)
    return statuses

def MigratePages(int pid, BPtr fromnodes, BPtr tonodes):
    return numa_migrate_pages(pid, fromnodes.ptr, tonodes.ptr)

def NodeSize(int node):
    cdef long long free
    size = numa_node_size64(node, &free)
    return size, int(free)

def Preferred():
    return numa_preferred()

def SetPreferred(int node):
    numa_set_preferred(node)

def NumTaskCpus():
    return  numa_num_task_cpus()

def NumTaskNodes():
    return  numa_num_task_nodes()

def ParseNodestring(str string not None):
    return Bitmask(nodestring=string)

def ParseCpustring(str string not None):
    return Bitmask(cpustring=string)
