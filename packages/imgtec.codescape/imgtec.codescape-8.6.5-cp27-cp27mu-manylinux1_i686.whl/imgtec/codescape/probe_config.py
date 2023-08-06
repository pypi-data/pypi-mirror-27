#  This module is a copy of the module in DialDLLs\da, but I don't want to
# create a dependency on DialDLLs from codescape at the moment, so this is cogged
# in.
# [[[cog
# from imgbuild.SConsPaths import sw
# with open(sw('comms', 'comms', 'config.py')) as f:
#    contents = f.read()
# cog.out(contents)
# ]]]
from collections import namedtuple
from imgtec.lib import namedenum
from imgtec.test import *
from textwrap import dedent
from pprint import pformat, pprint
import re

Format = namedenum.namedenum('Format', 'decimal hex')
Namespace = namedenum.namedenum('Namespace', 'unknown probe meta mips dbu ejtag')
AllNamespaces = set([Namespace(x) for x in Namespace._keys()])
ConfigImpl = namedtuple('ConfigImpl', 'name default category subcategory display_name doc danet sysprobe namespace format')

def indent(s, width=2):
    s = dedent(s)
    pre = ' ' * width
    return '\n'.join(pre + line for line in s.split('\n'))

def guess_namespace(category):
    try:
        category = 'probe' if category == 'Global' else category
        return Namespace(category.lower())
    except ValueError:
        return Namespace.unknown


keywords = frozenset(''''
    alignas alignof and and_eq asm auto bitand bitor bool break case catch char 
    char16_t char32_t class compl concept const constexpr const_cast continue 
    decltype default delete do double dynamic_cast else enum explicit export 
    extern false float for friend goto if inline int long mutable namespace new
    noexcept not not_eq nullptr operator or or_eq private protected public 
    register reinterpret_cast requires return short signed sizeof static 
    static_assert static_cast struct switch template this thread_local throw 
    true try typedef typeid typename union unsigned using(1) virtual void 
    volatile wchar_t while xor xor_eq
    
    mips
    '''.split())

def cname(name):
    '''Return a valid C name for the given name.
    
    >>> cname('auto')
    'auto_'
    >>> cname('IMG jtag v1.2')
    'img_jtag_v1_2'
    '''
    name = re.sub('\W', '_', name).lower()
    return name + '_' if name in keywords else name

class Config(ConfigImpl):
    def __new__(cls, name, default=0, category='', subcategory='', display_name=None, doc='', danet=True, sysprobe=True, namespace=None, format=Format.decimal):
        if display_name is None:
            display_name = name
        if namespace is None:
            namespace = guess_namespace(category)
        if namespace == Namespace.unknown and name:
            print "WARNING: Can't guess namespace for option %s in category %s" % (name, category)
        return ConfigImpl.__new__(cls, name, default, category, subcategory, display_name, doc, danet, sysprobe, namespace, format)

    @property
    def type(self):
        return typeof(self.default)
        
    @property
    def ctype(self):
        t = self.type
        if t == bool:
            return 'bool'
        elif t == int:
            return 'uint32_t'
        elif hasattr(t, '_items'):
            return t.__name__ + '::type'
        raise ValueError('No good C mapping for %r' % (t,))

    @property
    def cname(self):
        '''Return a valid C name for the config item.'''
        return cname(self.name)
        
    @property
    def cdefault(self):
        '''Return an expression for the default value in C.'''
        return self.cvalue(self.default)
        
    def cvalue(self, value):
        '''Return an expression for the given value in C.'''
        t = self.type
        if t == bool:
            return str(value).lower()
        elif t == int:
            formatter = '%d' if self.format == Format.decimal else '0x%08x'
            return formatter % (value,)
        elif hasattr(t, '_items'):
            return '%s::%s' % (t.__name__, cname(str(value)))
        raise ValueError('No good C mapping for %r' % (t,))

    def __repr__(self):
        kw = []
        if self.name != self.display_name:  kw.append(', display_name=%r' % (self.display_name,))
        if self.subcategory:                kw.append(', subcategory=%r' % (self.subcategory,))
        if self.doc:                        kw.append(", doc='''\\\n" + indent(self.doc) + "'''")
        if not self.danet:                  kw.append(', danet=False')
        if not self.sysprobe:               kw.append(', sysprobe=False')
        if guess_namespace(self.category) != self.namespace: kw.append(', namespace=%r' % (self.namespace,))
        return '%s(%r, %r, %r%s)' % (
            self.__class__.__name__, self.name, self.default, self.category, ''.join(kw))

def typeof(value):
    if isinstance(value, namedenum.Value):
        return value._cls
    if isinstance(value, bool):
        return bool
    if isinstance(value, (int, long)):
        return int
    return type(value)

MetaDebugRoute = namedenum.namedenum('MetaDebugRoute', 
    ('auto', 0, 'Debug Route is chosen based on address range of accesses and run status to minimize intrusiveness of debug'),
    ('around', 1, 'Route accesses around the core (i.e. post cache)'),
    ('through', 2, 'Route all accesses through the core')
)

DANetJtagClocks = namedenum.namedenum('DANetJtagClocks',
    ('khz_20000', 0, '20MHz'),
    ('khz_10000', 1, '10MHz'),
    ('khz_5000', 2, '5MHz'),
    ('khz_2500', 3, '2.5MHz'),
    ('khz_1250', 4, '1.25MHz'),
    ('khz_625', 5, '625KHz'),
    ('khz_312', 6, '312KHz'),
    ('khz_156', 7, '156KHz'),
)
def JtagSpeed(hertz):
    hr = '%dkHz' % (hertz/1000,)
    return ('khz_%d' % (hertz/1000,), hertz, hr)
SysProbeJtagClocks = namedenum.namedenum('SysProbeJtagClocks',
    JtagSpeed(2000),
    JtagSpeed(5000),
    JtagSpeed(10000),
    JtagSpeed(25000),
    JtagSpeed(50000),
    JtagSpeed(100000),
    JtagSpeed(250000),
    JtagSpeed(500000),
    JtagSpeed(1000000),
    JtagSpeed(1250000),
    JtagSpeed(2500000),
    JtagSpeed(5000000),
    JtagSpeed(10000000),
    JtagSpeed(20000000),
    JtagSpeed(31250000),
)

FastMonCacheMode = namedenum.namedenum('FastMonCacheMode',
    ('write_through', 0, 'Write through, No write allocate'),
    ('write_back', 3, 'Write Back, Write Allocate'),
)

LazyFreezeMode = namedenum.namedenum('LazyFreezeMode', 
   ('no_freeze', 0, 'No lazy Freeze (old behaviour) freeze performed after every command'),
   ('default', 1, 'Lazy freeze when other vpe is halted. improves performance when other vpe is halted'),
   ('always', 2, 'Lazy freeze whenever possible at the cost of independent run control, ie when one vpe is halted the other cannot execute instructions'),
)
UseAllRegisterMode = namedenum.namedenum('UseAllRegisterMode',
   ('off', 0, 'Use the ECR/Data/Address registers'),
   ('on', 1, 'Use the ALL register'),
   ('adaptive', 2, 'Use ALL register or ECR/Data/Address registers based on empirical evidence of #TAPs and TCK rate.'),
)


UNKNOWN_CONFIG = Config('', doc='No documentation available', category='Advanced', namespace=Namespace.unknown)

FastReadMode = namedenum.namedenum('FastReadMode', 
   ('off', 0, 'No Fast Reads at all'),
   ('on',  1, 'All reads greater than 16 x 32bit words are fast reads'),
   ('adaptive', 2, 'Fast reads are used if the fast monitor is already loaded (due to a fast write) or for reads greater than 4KB (1024 x 32bit words)'),
)

iCacheCoherencyMode = namedenum.namedenum('iCacheCoherencyMode', 
  ('flush_on_write', 0, '(default), issues a synci after each write'),
  ('flush_on_resume',1, 'maintain a list of all written memory locations and flush (D$ W.B. + I$ Inv) on resume (go)'),
)

TapProtocol = namedenum.namedenum('TapProtocol',
  ('auto', 0, '(default), on an autodetect command the probe will attempt to determine the TAP protocol, for scan-only and table-mode normal 4wire JTAG is used'),
  ('jtag', 1, 'Normal ieee1194.1 4 wire JTAG'),
  ('cjtag',2, 'ieee1149.7 (2 wire) compact JTAG (cJTAG)'),
  ('swd',  3, 'ARM, Serial Wire Debug (SWD)'),
  ('icsp', 4, 'Microchip, In Circuit Serial Programming (2 wire)'),
)

TracePLLMode = namedenum.namedenum('TracePLLMode', 
   ('off', 0, 'No MMCM PLLs, only oversampling'),
   ('on',  1, 'Only MMCM PLLs, no oversampling'),
   ('auto', 2, 'Use MMCM PLLs when the trace clock is >=20MHz else use oversampling'),
)

JTAGEdge = namedenum.namedenum('JTAGEdge',
  ('rising',  0,'TCK Rising Edge'),
  ('falling', 1,'TCK Falling Edge'),
)


""" when taps know which soc.core they are then busblaster taps could use this for fast support:
 Config('FTDI Fast Read Delay', 0xffffffff, 'MIPS', subcategory='Advanced', namespace=Namespace.ejtag, doc='''\
  FTDI taps only: Configures the delay in TCK clocks before the FASTDATA SPrAcc
  bit is assumed to be 1 after a FASTDATA read. When 0xffffffff fast reads are
  disabled.''', danet=False),
 Config('FPGA Fast Write Delay', 0xffffffff, 'MIPS', subcategory='Advanced', namespace=Namespace.ejtag, doc='''\
  FTDI taps only: Configures the delay in TCK clocks before the FASTDATA SPrAcc
  bit is assumed to be 1 after a FASTDATA write. When 0xffffffff fast writes are
  disabled.''', danet=False),
"""

_known_configs = [
 Config('JTAG Clock', DANetJtagClocks.khz_20000, 'Global', subcategory='General', doc='''\
  Selects JTAG clock frequency, this must be one of:

  0 = 20MHz, 1 = 10MHz, 2 = 5MHz, 3 = 2.5MHz, 
  4 = 1.25MHz, 5 = 625KHz, 6 = 312KHz, 7 = 156KHz.
  ''', sysprobe=False),
  
 Config('JTAG Clock', 31250000, 'Global', subcategory='General', doc='''\
  Selects JTAG clock frequency in Hertz.''', danet=False),
  
 Config('Halt After Reset', False, 'Global', subcategory='General', doc='''\
  When True on a HardReset an EJTAG boot is performed.  This stops the core
  from running from the Boot Exception Vector and goes straight into debug mode.

  Codescape Debugger also controls this option through the Halt After Reset
  option in Target Debug Options.'''),
  
 Config('Log Level', 0, 'Global', subcategory='General', doc='''\
  Controls the level at which debug messages get sent
  to the main log file (info log) and live logging.''', danet=False),
  
 Config('Verbose Logging', False, 'Global', subcategory='General', doc='''\
  Enables verbose logging, enabling this gives a small reduction in performance''', sysprobe=False),
  
 # reset... 
 Config('Reset Duration', 500, 'Global', subcategory='Reset', doc='''\
  The time in ms that the nRESETOUT signal is assert on hard reset''', danet=False),
 Config('Post Reset Delay', 0, 'Global', subcategory='Reset', doc='''\
  Time in ms to wait after a hard reset to allow bootrom to run before
  attempting any access from the probe''', danet=False),
 Config('Reset on Connect', False, 'Global', subcategory='Reset', doc='''\
  Issue Hard Reset on probe connection.'''),
 Config('Reset Tap Too', True, 'Global', subcategory='Reset', doc='''\
  After a hard reset CPC systems need a TAP reset to get the CPC into probe
  mode, so it'll power up all cores.''', danet=False),
  
 # profiling...
 Config('Sampling Duration', 0, 'Global', subcategory='Profiling', doc='''\
  The number of ms between statistical profiling samples. If zero no
  statistical profiling is performed.''', danet=False),
 Config('Sampling SoC Num', 0, 'Global', subcategory='Profiling', doc='''\
  The soc index on which statistical profiling samples should be collected.''', danet=False),
 Config('Sampling Core Num', 0, 'Global', subcategory='Profiling', doc='''\
  The core index on which statistical profiling samples should be collected.''', danet=False),
 Config('Sampling Threads', 0, 'Global', subcategory='Profiling', doc='''\
  A mask of the threads on which statistical profiling samples should be
  collected. For example 0b11 indicates threads 0 and 1.''', danet=False),
 Config('Sampling Oversamples', 0, 'Global', subcategory='Profiling', doc='''\
  The number of additional samples performed at each sample point.  Oversampling 
  allows more data to be collected each sampling point.''', danet=False),

 # advanced...
 Config('APB Timeout', 100, 'Global', subcategory='Advanced', doc='''\
  Timeout applied to debug transactions on devices which implement an APB
  (parallel) debug bus.''', danet=False),
 Config('Assert DINT', False, 'Global', subcategory='Advanced', doc='''\
  Override for the DINT Signal''', danet=False),
 Config('Assert nHardReset', True, 'Global', subcategory='Advanced', doc='''\
  Override for the nRESETOUT signal'''),
 Config('Assert nTRST', True, 'Global', subcategory='Advanced', doc='''\
  Override for the nTRST Signal'''),
 Config('Assert nTRST during tap reset', True, 'Global', subcategory='Advanced', doc='''\
  When set on a tap reset nTRST in assert then the JTAG state machine is
  walked to the reset state then nTRST is released, when cleared only a
  synchronous tap reset is performed (walking state machine to reset state). ''', sysprobe=False),
 Config('JTAG Logging', False, 'Global', subcategory='Advanced', doc='''\
  Enables logging of all JTAG scans, causes significant performance
  degradation and Codescape Debugger will probably time out.  This option
  should only be used for debugging low level JTAG scan issues in Codescape
  Console.'''),
 Config('Polling', True, 'Global', subcategory='Advanced', doc='''\
  Disable / Enable ALL background polling of All targets'''),
 Config('Timeout Scale', 50, 'Global', subcategory='Advanced', doc='''\
  Controls the scaling factor for timeouts, increasing this value
  increased the probes timeout (at the risk of lack of responsiveness on
  broken systems) usually only needed by very slow targets running on
  emulation platforms.'''),
 Config('Tap Protocol',TapProtocol.auto,'Global',subcategory='Advanced', doc='''\
  Configures the serial protocol used by the probe.
  When auto is selected the protocol is discovered during the tap topology \
  discovery phase of the autodetect command. If the user supplies the tap \
  topology for autodetect, protocol discovery will not occur and the protocol \
  will default to 4 wire.
  It is only possible to change Tap Protocol when in uncommitted or scan-only modes.'''),   
 Config('cJTAG OAC Length', 12, 'Global',subcategory='Advanced', doc='''\ 
  Set the length of the cJTAG Online Activation Code, the short form is typically 12 bits,\
  the longer form is typically 36 bits, see the ieee1149.7 spec for more details,\
  See cJTAG OAC Data 0/1 for the data values to use'''),
 Config('cJTAG OAC Data 0', 0x8c, 'Global',subcategory='Advanced', doc='''\ 
  Lower 32bits (or less depending on cJTAG OAC Length) of the cJTAG Online \
  Activation Code / Selection Sequence, data is transmitted LSB first.'''),
 Config('cJTAG OAC Data 1', 0x00, 'Global',subcategory='Advanced', doc='''\ 
  bits 63-32 (or less depending on cJTAG OAC Length) of the cJTAG Online \
  Activation Code / Selection Sequence, data is transmitted LSB first.'''),
 Config('JTAG Input Edge', JTAGEdge.falling, 'Global', subcategory='Advanced', doc='''\
  The TCK Edge on which TDI input is registered.'''),
 Config('JTAG Output Edge', JTAGEdge.falling,  'Global', subcategory='Advanced', doc='''\
  The TCK Edge on which TMS/TDO outputs transition.'''),
 Config('MDH valid retry step', 100, 'Global', subcategory='Advanced', doc='''\
  The time in uS which the valid retry timer gets incremented by on a valid=0 retry.
  When accessing the APB bus of slow targets via the MDH's JTAG interface a delay is needed 
  between issuing the APB access and checking the response, the probe automatically increases 
  this delay every 10th scan which requires a retry (up to a max of 'APB Timeout').
  This setting controls how big the increase is, bigger values are useful on very slow targets where it may take 
  hundreds of retries until the correct delay is tuned in.''', danet=False),
  
 # MIPS General
 Config('PC Sample', True, 'MIPS', subcategory='General', doc='''\
  Enable PC Sampling on connection'''),
  
 # MIPS/memory access...
 Config('Allow FixedMap Accesses', False, 'MIPS', subcategory='Memory Access', doc='''\
  With a Fixed Map MMU all mapped accesses proceed with a simple address
  translation, thus when enabled its easy to lock up targets using this MMU
  if HSPs have not been set correctly'''),
 Config('Allow KUSEG Accesses', False, 'MIPS', subcategory='Memory Access', doc='''\
  When Status ERL+EXL =1, USEG gets a 1:1 mapping between virt and phys space
  (ignoring MMU) if set probe accesses are allowed to proceed in USEG in this
  state.'''),
 Config('Allow Mapped Accesses', True, 'MIPS', subcategory='Memory Access', doc='''\
  Allows access to mapped regions (eg useg, kseg2/3) note access may still
  fail if address not mapped in MMU'''),
 Config('Disable MMU Checking', False, 'MIPS', subcategory='Memory Access', doc='''\
  Prevent any checking of the MMU to see if mapped accesses will work, risky
  to set will cause exceptions in debug mode if access not mapped'''),
 Config('Fast Monitor Address', 0x80000000, 'MIPS', subcategory='Memory Access', doc='''\
  Address to which fast transfer monitor is loaded to before it gets locked
  into the cache, this must be a KSEG0 address''', format=Format.hex),
 Config('Fast Reads', FastReadMode.adaptive, 'MIPS', subcategory='Memory Access', namespace=Namespace.ejtag, doc='''\
  Use fast mode transfers for block reads, only enable this if the target has
  working memory at kseg0 after reset (Malta+coreFPGA6, Sead-3, but not
  Malta+coreFPGA5 and most SoCs)''',danet=False),
 Config('Fast Reads', False, 'MIPS', subcategory='Memory Access', namespace=Namespace.ejtag, doc='''\
  Use fast mode transfers for block reads, only enable this if the target has
  working memory at kseg0 after reset (Malta+coreFPGA6, Sead-3, but not
  Malta+coreFPGA5 and most SoCs)''', sysprobe=False),
 Config('Fast Writes', True, 'MIPS', subcategory='Memory Access', namespace=Namespace.ejtag, doc='''\
  Use fast mode transfers for block writes'''),
 Config('Use Current ASID', True, 'MIPS', subcategory='Memory Access', doc='''\
  Uses the current ASID in entryhi as this is most likely the current running
  process, for the ASID of the access, ignoring the value from Codescape'''),
 Config('Use ISPRAM', False, 'MIPS', subcategory='Memory Access', doc='''\
  Enables debugger handling of ISPRAM, note ISPRAM setup is cached on setting
  Use ISPRAM = 1, if ISPRAM setup is changed this setting must be disabled and
  re-enabled'''),

 # MIPS/reset
 Config('Post Reset Delay', 0, 'MIPS', subcategory='Reset', doc='''\
  Time in ms to wait after a hard reset to allow bootrom to run before
  attempting any access from the probe''', sysprobe=False),
 Config('Reset ACK Timeout', 500, 'MIPS', subcategory='Reset', doc='''\
  The time in ms to wait for while acknowledging Reset (waiting for Rocc)'''),
 Config('Reset Duration', 500, 'MIPS', subcategory='Reset', doc='''\
  The time in ms that the nRESETOUT signal is assert on hard reset''', sysprobe=False),
  

 # MIPS/dbu
 Config('Force Reload Monitor', False, 'MIPS', subcategory='DBU', namespace=Namespace.dbu, doc='''\
   ''', danet=False),
 Config('Monitor Command Timeout', 500, 'MIPS', subcategory='DBU', namespace=Namespace.dbu, doc='''\
   ''', danet=False),  
Config('Monitor Data Compression', False, 'MIPS', subcategory='DBU', namespace=Namespace.dbu, doc='''\
   ''', danet=False),  

 # MIPS/advanced
 Config('CPC Probe Mode', True, 'MIPS', subcategory='Advanced', doc='''\
  After a hard reset CPC systems need a TAP reset to get the CPC into probe
  mode, so it'll power up all cores''', sysprobe=False),
 Config('Disable Ints on HW Single Step', False, 'MIPS', subcategory='Advanced', doc='''\
  Disables interrupts on HardwareSingle Step (So you don't end up stepping
  into interrupt handling code eg a timer interrupt).'''),
 Config('Disable trace on halt', False, 'MIPS', subcategory='Advanced', doc='''\
  When set the probe disable trace data collection on an unexpected halt
  (Breakpoint/SingleStep etc).'''),
 Config('EJTAG Boot All', True, 'MIPS', subcategory='Advanced', doc='''\
  When False, a reset with 'Halt after Reset' selected only applies the EJTAG
  boot indication/instruction to the first tap (ie c0v0).

  When True, all taps receive an EJTAG boot instruction.''', sysprobe=False),
 Config('Enter Debug Timeout', 100, 'MIPS', subcategory='Advanced', doc='''\
  The time in ms to wait while trying to get the core into debug mode'''),
 Config('FPGA Fast Read', True, 'MIPS', subcategory='Advanced', namespace=Namespace.ejtag, doc='''\
  Offload the fast transfer polling sequence to the FPGA'''),
 Config('FPGA Fast Write', True, 'MIPS', subcategory='Advanced', namespace=Namespace.ejtag, doc='''\
  Offload the fast transfer polling sequence to the FPGA'''),
 Config('Guest TLB', False, 'MIPS', doc='''\
  Make TLB commands operate on the guest TLB.''', sysprobe=False),
 Config('Lock Monitor in Cache', True, 'MIPS', subcategory='Advanced', namespace=Namespace.ejtag, doc='''\
  Lock the fast data monitor into the I cache if available'''),
 Config('Log Address Jumps', False, 'MIPS', subcategory='Advanced', namespace=Namespace.ejtag, doc='''\
  Write to log when debug instruction fetch address is not previous address +
  4, has slight impact on performance and can fill log quickly on pro-aptiv as
  it often re-requests same instruction'''),
 Config('Log Debug Instructions', False, 'MIPS', subcategory='Advanced', namespace=Namespace.ejtag, doc='''\
  Record each instruction executed in debug mode in DA Verbose Log (Slows
  performance when enabled).'''),
 Config('Max FDC Channels', 0, 'MIPS', subcategory='Advanced', doc='''\
  Controls the number of channels (from 0) which get mapped to DA virtual
  channels'''),
  
 Config('Print ECR on Timeout', True, 'MIPS', subcategory='Advanced', doc='''\
  Prints the ECR of all TAPs in the system including potentially none MIPS
  taps, hence this could be disturbing for non MIPS taps.'''),
 Config('Stop Count in DM', True, 'MIPS', subcategory='Advanced', doc='''\
  Stops the count register from being incremented when the CPU is in debug mode.'''),
 Config('Using BEV overlay', False, 'MIPS', subcategory='Advanced', doc='''\
  When this option transitions from 0->1 the probe will re-cache the BEV
  overlay settings, If user code reconfigures the BEV overlay at runtime
  then this option needs toggling so the probe can re-cache the new settings.'''),
 Config('Fast Mon Cache Mode', FastMonCacheMode.write_through, 'MIPS', subcategory='Advanced', namespace=Namespace.ejtag, doc='''\
  Set kseg0 cache mode to be used during locked in cache fast transfers (if
  kseg0 is currently not marked as cacheable). Only use write_back if the cache
  is properly initialised.'''),
 Config('Trace Fast', False, 'MIPS', subcategory='Advanced', doc='''\
  Experimental option not for users.'''),
 Config('Intrusive Trace', True, 'MIPS', subcategory='Advanced', doc='''\
  Allow the probe to halt the core, for a small period of time and then
  automatically resume, preventing the trace buffer from overflowing.''', danet=False),
 Config('Trace Timeout', 50, 'MIPS', subcategory='Advanced', doc='''\
  When running trace through sockets and the intrusive_trace option is
  enabled, the probe will halt the core for trace_timeout milliseconds
  to avoid overflowing the trace buffer.''', danet=False),
 Config('Trace Clock', 0, 'MIPS', subcategory='Advanced', doc='''\
  Set the expected trace clock to avoid autodetection.''', danet=False),
 Config('Calibrate Trace', 0xffffffff, 'MIPS', subcategory='Advanced', doc='''\
  In order to capture PDtrace data, the FPGA needs calibration. Either run
  the calibration script to find the proper Idelay, or set it manually.''', format=Format.hex, danet=False),
 Config('Trace PLLs', TracePLLMode.auto, 'MIPS', subcategory='Advanced', doc='''\
  The FPGA will either use the MMCM PLLs to lock with the trace clock or it
  will try to oversample.''', danet=False),
 Config('Use 20bit Addr', True, 'MIPS', subcategory='Advanced', doc='''\
  Only Read the first 20bits of the EJTAG address register, helps improve performance''', danet=False),
 Config('Use ALL Register', UseAllRegisterMode.adaptive, 'MIPS', subcategory='Advanced', doc='''\
  Use the ALL register to do dmseg servicing instead of reading CONTROL, DATA, 
  and ADDRESS separately.  This is usually a performance improvement except for 
  small number of taps or very slow TCK rates.''', danet=False),
 Config("Lazy Freeze",LazyFreezeMode.default,'MIPS',subcategory='Advanced',doc='''\
  Controls the level of lazy freeze performed on MT-ASE cores.'''),
 Config('Pracc Timeout', 500, 'MIPS', subcategory='Advanced', doc='''\
  The time in ms to wait for a pending debug access''', danet=False),
 Config('GCR core other', False, 'MIPS', subcategory='Advanced', doc='''\
  When set re-routes gcr register access to the 'other' core, the 'other' core 
  register must be set appropriately for the core you wish to access
  (ie GCR_CL_OTHER_REG, CPC_CL_OTHER_REG, GIC_VP_OTHER_REG)''', danet=False),
 Config('iCache Coherency Mode', iCacheCoherencyMode.flush_on_write, 'MIPS', subcategory='Advanced', doc='''\
  Control the behaviour of how icache coherency is maintained''', danet=False),
 # Meta:
 Config('Allow Intrusive Debug', False, 'Meta', doc='''\
  When set the DA will perform an intrusive poll of the target whilst running,
  this will have a slight impact on any   performance measurements which need
  to be cycle accurate, But gives better detection of a thread stopping or
  starting outside of the DAs control.'''),
 Config('Core Reg Interlock', False, 'Meta', doc='''\
  Take Lock2 when accessing TXXUXRXQ as part of sharing protocol (enable
  above) set both of these if sharing'''),
 Config('Core Reg Negotiate', False, 'Meta', doc='''\
  Use the soft locking / negotiation protocol when sharing the register port
  with another user (eg another thread or a host via Slave port).'''),
 Config('DCL High Precision Mode', False, 'Meta', doc='''\
  Takes LOCK2 while DCL script is running, can help reduce jitter in
  performance measurements'''),
 Config('Debug Route', MetaDebugRoute.auto, 'Meta', doc='''\
  The Meta HTP and MTP cores allow debug requests to be routed through the 
  core so that the debugger can access cache resource with the same view as the 
  core. 
  
  Auto address and runstate map:

  +---------------------------------------------+-------------------+-------------------+
  |                   Region                    |     Running       |   Halted          |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  |  start   |   end    |       Name            | Read    | Write   | Read    | Write   |
  +==========+==========+=======================+=========+=========+=========+=========+
  | 00000000 | 00200000 | Invalid 1             | -       | -       | -       | -       |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  | 00200000 | 04000000 | Custom + Expansion    | Around  | Around  | Around  | Around  |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  | 04000000 | 04800000 | Sys Ev + cache Flush  | -       | Through | -       | Through |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  | 04800000 | 05000000 | Core Registers        | Around  | Around  | Around  | Around  |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  | 05000000 | 06000000 | MMU table area        | Around  | Through | Through | Through |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  | 06000000 | 08000000 | Direct Map            | Around  | Through | Through | Through |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  | 08000000 | 80000000 | Local linear range    | Around  | Through | Through | Through |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  | 80000000 | 82000000 | Core Code memory      | Around  | Around  | Around  | Around  |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  | 82000000 | 84000000 | Core Data memory      | Through | Through | Through | Through |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  | 84000000 | 87FFFFF8 | Core locked cache     | MCM  [#mcm]_                          |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  | 87FFFFF8 | 88000000 | Special - non memory mapped debug registers eg MDBGCTRL1      |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  | 88000000 | FFFF0000 | Global linear range   |  Around | Through | Through | Through |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  | FFFF0000 | FFFFFFFF | Invalid 2             | -       | -       | -       | -       |
  +----------+----------+-----------------------+---------+---------+---------+---------+
  
  .. [#mcm] Accesses performed via MCM to the actual cache line and either through or 
            around to update physical memory where appropriate.'''),
 Config('Force Availability', True, 'Meta', doc='''\
  When set the DA will always set the force availability bit in the JTAG
  control register'''),
 Config('MCM Port Locking', True, 'Meta', doc='''\
  Use the Soft locking protocol to share the MCM port with another user (eg
  another thread or host via slave port)'''),
 Config('MDBG Diagnostics Mode', False, 'Meta', doc='''\
  Puts the Meta Debug Port in to diagnostics mode, to allow postmortem debug
  of a locked up system.'''),
 Config('Minim Translations', True, 'Meta', doc='''\
  Disables the DA from performing minim translations on minim code addresses
  on memory type 0.'''),
 Config('Per Thread Channels', True, 'Meta', doc='''\
  Each Meta thread gets it own set of DA channels'''),
 Config('Polling in Diagnostics Mode', True, 'Meta', doc='''\
  When in debug port diagnostic mode this disables polling of the ready bit
  during debug transactions, clear it if the core is very badly locked up, you
  may get some state out if you are lucky'''),
 Config('TBI Stack Unwinding', True, 'Meta', doc='''\
  When Halt interrupts are enabled and a target stops at a breakpoint (or due
  to single-step) the state shown to the user by the DA isn't the actual state
  of the target.  When the target stops at the breakpoint a halt interrupt
  fires and we jump to TBIs halt interrupt handler which see the halt as a
  breakpoint, so turns off halt interrupts and executes another switch
  instruction (breakpoint), this happens in a function called
  TBIUnexpectXXX().  The DA then unwinds the stack to show the user the
  original halt state.  When this setting is cleared you get to see the true
  state (ie stopped at a switch in TBIUexpectXXX).'''),
 Config('Allow RW in Wiggler Mode', False, 'Meta', subcategory='Deprecated', doc='''\
  Test mode not for users'''),
 Config('Force Debug Through Core', False, 'Meta', subcategory='Deprecated', doc='''\
  use Debug Route. When set all debug requests go through the core, instead of
  selecting through or round based on access type'''),
 Config('High Skew TAP mode', False, 'Meta', subcategory='Deprecated', sysprobe=False),
 Config('IMG JTAG v1.2', True, 'Meta', subcategory='Deprecated', doc='''\
  Allow disabling of IMGJTAG v1.2 features (attention etc). Needed for test
  and old broken target'''),
 Config('Idle Polling Enabled', False, 'Meta', subcategory='Deprecated', doc='''\
  Allows disabling idle polling per core''', sysprobe=False),
 Config('Soc Power Check', True, 'Meta', subcategory='Deprecated', doc='''\
  Use the global setting 'Polling' instead of this deprecated option.''', sysprobe=False),
]

def get_configs_for_probe(identifier, namespaces=AllNamespaces):
    '''Get the valid configs for the probe.

    `identifier` is a 'DA-net ...' or 'SysProbe ...'
    '''
    if isinstance(namespaces, str):
        namespaces = [Namespace(x) for x in namespaces.split()]
    type = identifier.split(None, 1)[0]
    if type.lower() == 'da-net':
        return [x for x in _known_configs if x.danet and x.namespace in namespaces]
    else:
        return [x for x in _known_configs if x.sysprobe and x.namespace in namespaces]
        
# for global options that do not use m_gbl_settings to get/set the option
global_getter_setters = {
    "JTAG Clock"        : ('m_tap.get_jtag_clock()', 'm_configuration.jtag_clock(m_tap.set_jtag_clock(%s))'),
    "Assert nHardReset" : ('m_tap.get_sideband(tap::sys_rst_out)', 'm_tap.set_sideband(tap::sys_rst_out,%s)'),
    "Assert nTRST"      : ('m_tap.get_sideband(tap::trst_out)', 'm_tap.set_sideband(tap::trst_out,%s)'),
    "Assert DINT"       : ('m_tap.get_sideband(tap::dint)', 'm_tap.set_sideband(tap::dint,%s)'),
    "Log Level"         : ('uint32_t(get_log_level())', 'set_log_level(dbg::level::type(%s))'),
    "JTAG Logging"      : ('m_tap.logging()', 'm_tap.logging(%s)'),
    "Timeout Scale"     : ('m_tap.timeout_scale()', 'm_tap.timeout_scale(%s)'),
}

class TestDAnet(object):
    identifier = 'DA-net 1'
    config = dict([(c.name, c.default) for c in get_configs_for_probe('da-net')])

class TestSysProbe(object):
    identifier = 'SysProbe 1'
    config = dict([(c.name, c.default) for c in get_configs_for_probe('Sysprobe')]) 

@test
def test_repr_is_evalable():
    eval(pformat(_known_configs))
    
@test
def test_repr_is_evalable_and_equal_to_original():
    pass#assertEquals(_known_configs, eval(pformat(_known_configs)))
    
if __name__ == '__main__':
    if test.main() == 0:
        pprint(_known_configs)
    
# [[[end]]]
