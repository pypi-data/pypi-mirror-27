import time
from copy import copy
from imgtec.codescape.program_file import ProgramFileError
from imgtec.console.support import *
from imgtec.console.results import *
from imgtec.console.program_file import elf_required, symbol, source, SymbolError
from imgtec.console.generic_device import go, runstate, cpuinfo
from imgtec.console.tdd import targetdata
from imgtec.lib.rst import grid_table, headerless_table
from imgtec.lib.namedbitfield import namedbitfield, compile_fields
from imgtec.console.scan import _check_config, get_tap_type, JTAG_TYPE_DBU
from imgtec.console.scan import JTAG_TYPE_MDH, tapreg, PCSampleValue
from imgtec.console.regs import regs
from imgtec.console.commands import config
from collections import Counter, OrderedDict

@command()
def pcsamp(core=0, vpe=0, device=None):
    """Read the PCSAMPLE register. 
    For DBU taps change core and vpe to access other threads.

    >>> pcsamp()
    0x17f800001
    PC       New
    bfc00000 1
    >>> '0x%08x' % pcsamp().PC
    0xbfc00000
    >>> pcsamp().New
    0x1

    """
    if device.probe.mode in ('autodetected', 'table'):
        if targetdata(device).socs[device.tiny.SoCNumber()].tap_type == 0x8:
            return dbu_pcsamp(device)
        else:
            return PCSampleValue(device.tiny.ReadRegister('ejtag_pcsample'))
    else:
        _check_config(device, 'pcsamp')
        tap_type = get_tap_type(device)
        if tap_type == JTAG_TYPE_DBU:
            return dbu_pcsamp_scanonly(device, core, vpe)
        elif tap_type == JTAG_TYPE_MDH:
            raise RuntimeError('scanonly pcsamp not supported on MDH targets')
        else:
            return tapreg('pcsamp', device=device)

DBUPCSampExtValue = namedbitfield('SamuraiPCSampExtValue', compile_fields('''\
        New                63
        Completed          62
        GuestCtl0          28
        POM                27 25
        Instr_cnt          24 22
        New_DebugContextID 21
        K                  20
        ASID               19 10
        guestID            9 0'''.splitlines()))
        
class DBUVaddrValue(object):
    def __init__(self, pc_vaddr):
        self.new = (pc_vaddr >> 63) & 0x1
        self.completed = (pc_vaddr >> 62) & 0x1
        
        #61-57 is shifted up 2 and combined with the lower 57 bits
        self.pc = ((pc_vaddr & 0x3E00000000000000) << 2) | (pc_vaddr & 0x1FFFFFFFFFFFFFF)
        
        #The shift may have left a 2 bit gap, sign extend over it
        if self.pc & 0x100000000000000:
            self.pc = self.pc | 0x0600000000000000
            
    def __repr__(self):
        return rst.simple_table(['New', 'Completed', 'PC'], [[str(bool(self.new)), str(bool(self.completed)), '0x%08x' % self.pc]])
        
class DBUPCSampleValue(object):
    def __init__(self, vaddr, extended):
        self._vaddr = vaddr
        self._extended = extended
        
    def __repr__(self):
        return repr(self._vaddr)
    
    @property
    def New(self):
        return self._vaddr.new
        
    @property
    def PC(self):
        return self._vaddr.pc
        
def dbu_pcsamp(device):
    pc_extensions = DBUPCSampExtValue(device.tiny.ReadRegister('dbu_drseg_pcs_extensions'))
    #Order is important, VADDR must be last
    pc_vaddr = device.tiny.ReadRegister('dbu_drseg_pcs_pc')
    return DBUPCSampleValue(DBUVaddrValue(pc_vaddr), pc_extensions)
    
def dbu_pcsamp_scanonly(device, core, vpe):
    from imgtec.console.dbudriver import get_rb_accessor
    acc = get_rb_accessor(device)
    pc_extensions = acc.read(core, core, vpe, 0x1f0, True)
    pc_vaddr = acc.read(core, core, vpe, 0x1f8, True)
    return DBUPCSampleValue(DBUVaddrValue(pc_vaddr), pc_extensions)

class SortFieldError(Exception):
    pass

class SortOrderError(Exception):
    pass

class ResultFilterError(Exception):
    pass

class PCSampNotSupportedError(Exception):
    pass

class NoValidPacketError(Exception):
    pass

UNKNOWN_FUNCTIONS       = 'Samples outside known functions'
UNREAD_FILE             = 'The file could not be read.'

def hex_string(value):
    return str(hex(value)).strip('L')

def percentage(part, whole):
    return 100 * part/float(whole)

def get_bucket_start_end_unknown(address):
    return address & ~0xfff, (address & ~0xfff) + 0x1000

def bucket_exists(f_dict, b_start, b_end):
    for f in f_dict.values():
        if f.unknown and f.within(b_start, b_end):
            return f

# processing cases split for ease of testing

def process_known_samples(pcsample, address_hits, result_dict, symbols, add_info_dict, device):
    pc_value = pcsample.address
    additional_info = FunctionAdditionalInfo(pcsample.asid,
                                             pcsample.tc_id)
    
    add_info_dict[hash(additional_info)] = additional_info

    if symbols.get(pc_value):
        symbol_at_address = symbols[pc_value]
    else:
        symbol_at_address = symbol(pc_value, device=device)[0]
        symbols[pc_value] = symbol_at_address
    current_func = symbol_at_address.name
    start = symbol_at_address.value
    end = start + symbol_at_address.size

    new_func = Function(current_func, address_hits, start, end, hash(additional_info))
    new_func_key = hash(new_func)
    if result_dict.get(new_func_key):
        result_dict[new_func_key].hits += address_hits
    else:
        result_dict[new_func_key] = new_func

def process_unknown_samples(pcsample, address_hits, result_dict, add_info_dict):
    pc_value = pcsample.address
    additional_info = FunctionAdditionalInfo(pcsample.asid,
                                             pcsample.tc_id) 

    add_info_dict[hash(additional_info)] = additional_info

    bucket_start, bucket_end = get_bucket_start_end_unknown(pc_value)
    bucket = bucket_exists(result_dict, bucket_start, bucket_end)
    if bucket is not None:
        bucket.update_minmax_unknown(pc_value)
        bucket.hits += address_hits
    else:
        new_unknown = Function(UNKNOWN_FUNCTIONS, address_hits, bucket_start, 
                               bucket_end, hash(additional_info))
        new_unknown.min_unknown = pc_value
        new_unknown.max_unknown = pc_value

        new_unknwon_key = hash(new_unknown)
        result_dict[new_unknwon_key] = new_unknown
        
def process_pcsamp_results(pcsample, address_hits, result_dict, symbols, add_info_dict, device):
    try:
        process_known_samples(pcsample, address_hits, result_dict, symbols, add_info_dict, device)
    except SymbolError:
        process_unknown_samples(pcsample, address_hits, result_dict, add_info_dict)

def process_source_lines(address, file_dict, hits, symbols, sources, device):
    try:
        if sources.get(address):
            source_at_address = sources[address]
        else:
            source_at_address = source(address, lines=0, device=device)
            sources[address] = source_at_address
        file = file_dict.get(source_at_address.file)
        if file is None:
            try:
                with open(source_at_address.file, 'r') as f:
                    source_lines = f.read().splitlines()    
                lines_list = ValidFileLineDict(dict({index + 1: ValidFileLine(line, index + 1)    
                                                     for index, line in enumerate(source_lines)}))
            except IOError:
                lines_list = InvalidFileLineDict(dict())
            finally:
                file = SourceFile(source_at_address.file, lines_list)
                file_dict[source_at_address.file] = file
        if not file.valid and source_at_address.current_line not in file.lines:
            file.lines[source_at_address.current_line] = InvalidFileLine(source_at_address.current_line)
        file.update_symbol_at_line(source_at_address.current_line, address, 
                                   symbols)
        file.increase_hitcount(hits, source_at_address.current_line)
    except ProgramFileError:
        pass

def final_step_processing(func_count, file_dict, pcsample_dict, elapsed_time, 
                          sort_field, sort_order, filter_exp, print_files_stats, device):  
    symbols_dict = dict()
    sources_dict = dict()
    add_info_dict = AdditionalInfoDict()

    for key in pcsample_dict:
        process_pcsamp_results(key, pcsample_dict[key], func_count, symbols_dict, add_info_dict, device)
        process_source_lines(key.address, file_dict, pcsample_dict[key], 
                             symbols_dict, sources_dict, device)
    
    for func in func_count.values():
        if func.unknown:
            func.update_final_addresses()

    sample_count = sum(pcsample_dict.values())

    result = PCSampStatsResult(func_count, add_info_dict, file_dict, sample_count,
    sample_count / elapsed_time, sort_field, sort_order, filter_exp, print_files_stats)       

    return result

class PCSampStatsResult(object):
    def __init__(self, all_func_dict, add_info_dict, file_dict, no_samples, sample_rate, 
    sort_field, sort_order, result_filter, print_files_stats):
        self.all_func_dict 			    = all_func_dict
        self.additional_info_dict       = add_info_dict
        self.file_dict                  = file_dict
        self.no_samples 				= no_samples
        self.sample_rate 				= sample_rate
        self._sort_field 				= sort_field
        self._sort_order 				= sort_order
        self._result_filter 			= result_filter

        self.update_func_table(self._result_filter)
        self.update_files_tables()

        self.print_basic_stats          = True
        self.print_func_table           = True
        self.print_files_stats          = print_files_stats
        self.samp_count_for_update      = self.no_samples
    
    @property
    def sort_field(self):
        return self._sort_field

    @sort_field.setter
    def sort_field(self, new_sort_field):
        if self.check_sort_field(new_sort_field):
            self._sort_field = new_sort_field
            self.update_func_table(self._result_filter)

    @property
    def sort_order(self):
        return self._sort_order

    @sort_order.setter
    def sort_order(self, new_sort_order):
        if self.check_sort_order(new_sort_order):
            self._sort_order = new_sort_order
            self.update_func_table(self._result_filter)

    @property
    def result_filter(self):
        return self._result_filter

    @result_filter.setter
    def result_filter(self, new_result_filter):
        self.update_func_table(new_result_filter)
        self._result_filter = new_result_filter

    def sort_functions(self):
        if self.check_sort_field(self._sort_field) and self.check_sort_order(self._sort_order):
            if self._sort_field == 'name':
                key = lambda list_item:list_item.name.lower()
            else:
                key = lambda list_item:getattr(list_item, self._sort_field)
            return sorted(self.all_func_dict.values(), key=key, reverse=self._sort_order == 'desc')

    def filter_functions(self, filter_exp, sorted_func_list):
        try:
            filtered_list = list()
            for f in sorted_func_list:
                all_fields_dict = copy(self.additional_info_dict[f.additional_info_id].__dict__)
                all_fields_dict.update(f.__dict__)
                if eval(filter_exp, all_fields_dict):
                    filtered_list.append(f)
            return filtered_list
        except NameError: 
            valid_fields = [field for field in all_fields_dict if field != '__builtins__']
            raise ResultFilterError('Valid fields are: %r' % valid_fields)

    def update_filtered_list(self, filtered_list):
        self.samp_count_for_update = 0
        if not filtered_list:
            self.samp_count_for_update = self.no_samples
        else:
            for func in filtered_list:
                self.samp_count_for_update += func.hits
        for func in filtered_list:
            func.percentage = percentage(func.hits, self.samp_count_for_update)
        for key in self.file_dict:
            file = self.file_dict[key]
            for line in file.lines:
                file.lines[line].visible = file.file_line_in_filtered_function(file.lines[line], filtered_list)
            
    def update_func_table(self, new_result_filter):
        if (self.check_sort_field(self._sort_field) 
            and self.check_sort_order(self._sort_order)):
            table_funcs = self.sort_functions()
            table_funcs = self.filter_functions(new_result_filter, table_funcs)
            self.update_filtered_list(table_funcs)

        updated_func_dict = FunctionDict()
        for f in table_funcs:
            updated_func_dict[hash(f)] = f 
        self.func_table = updated_func_dict.as_table(self.additional_info_dict)

    def update_files_tables(self):
        self.files_tables = ''
        for key in self.file_dict:
            file = self.file_dict[key]
            for line in file.lines:
                file.lines[line].percentage = percentage(file.lines[line].hits, self.samp_count_for_update)
            file.update_hits()
            file.percentage = percentage(file.hits, self.samp_count_for_update)
        self.files_tables = repr(self.file_dict)

    def check_sort_order(self, ord):
        if not ord in ['asc', 'desc']:
            raise SortOrderError("Wrong sort order given. Please use one of: ['asc', 'desc']")
        else:
            return True

    def check_sort_field(self, field):
        if not field in ['name', 'hits', 'startaddress']:
            raise SortFieldError("Wrong sort field given. Please use one of: ['name', 'hits', 'startaddress']")
        else:
            return True

    def __repr__(self):
        self.update_files_tables()
        self.update_func_table(self._result_filter)
        string_rep = ""
        if self.print_basic_stats:
            string_rep += "Samples collected: {}\nSample Collection Rate: {} samples/sec".format(self.no_samples, format(self.sample_rate, '.2f'))
        if self.print_func_table:
            string_rep += "\n\nFunctions Table:\n{}".format(self.func_table)
        if self.print_files_stats:
            string_rep += "\n\nSource Lines Tables:\n{}".format(self.files_tables)
        return string_rep

class Function(object):
    def __init__(self, name, hits, startaddress, endaddress, info_id):
        self.name 			    = name
        self.hits 			    = hits
        self.startaddress 	    = startaddress
        self.endaddress 	    = endaddress
        self.additional_info_id = info_id
        self.unknown 		    = self.name == UNKNOWN_FUNCTIONS

    def update_minmax_unknown(self, new_value):
        self.min_unknown 	= min(self.min_unknown, new_value)
        self.max_unknown 	= max(self.max_unknown, new_value)

    def within(self, start_addr, end_addr):
        return self.startaddress >= start_addr and self.endaddress <= end_addr

    def update_final_addresses(self):
        if self.min_unknown < self.max_unknown:
            self.startaddress 	= self.min_unknown
            self.endaddress 	= self.max_unknown

    def as_list(self, add_info_dict=None):
        return [self.name, str(self.hits) + ' ({}%)'.format("%.2f" % self.percentage), 
                hex_string(self.startaddress), hex_string(self.endaddress), 
                self.additional_info_for_output(add_info_dict) if add_info_dict else self.additional_info_id]

    def additional_info_for_output(self, add_info_dict):
        add_info = add_info_dict[self.additional_info_id]
        add_info_str = ''
        if add_info.asid is not None:
            add_info_str += 'asid={}'.format(add_info.asid)
        if add_info.tc_id is not None:
            add_info_str += ',tc_id={}'.format(add_info.tc_id)
        return add_info_str
    
    def __eq__(self, other):
        return (self.name == other.name and self.startaddress == other.startaddress
                and self.additional_info_id == other.additional_info_id)

    def __hash__(self):
        return hash((self.name, self.startaddress, self.additional_info_id)) 

    def __repr__(self):
        return 'Function(name={}, hits={}, percentage={}, startaddress={}, endaddress={})'.format(self.name, self.hits, 
                                                                                                  self.percentage, 
                                                                                                  hex_string(self.startaddress), 
                                                                                                  hex_string(self.endaddress))

class FunctionAdditionalInfo(object):
    def __init__(self, asid, tc_id):
        self.asid           = asid
        self.tc_id          = tc_id

    def __hash__(self):
        return hash((self.asid, self.tc_id))

    def __eq__(self, other):
        return self.asid == other.asid and self.tc_id == other.tc_id
    
    def __repr__(self):
        return 'asid={}, tc_id={}'.format(self.asid, self.tc_id)

class AdditionalInfoDict(dict):
    def __repr__(self):
        rows_list = list()
        for key in self:
            rows_list.append([repr(key), repr(self[key])])
        return rst.simple_table(['Info ID', 'Additional Info'], rows_list)

class ValidFileLine(object):
    def __init__(self, content, num):
        self.content 	        = content
        self.num  		        = num
        self.hits 		        = 0
        self.symbol_at_line     = None

    def as_list(self):
        if self.hits != 0 and self.visible:
            return ['{} ({}%)'.format(self.hits, format(self.percentage, '.2f')), '> {}:'.format(self.num), self.content]
        elif self.hits != 0 and not self.visible:
            return ['--------', '> {}:'.format(self.num), self.content]
        else:
            return [' ', '> {}:'.format(self.num), self.content]

    def __repr__(self):
        return 'ValidFileLine(num={}, content={}, hits={}, percentage={})'.format(self.num, self.content, self.hits, self.percentage)

class InvalidFileLine(object):
    def __init__(self, num):
        self.num  		        = num
        self.hits 		        = 0
        self.symbol_at_line     = None

    def __repr__(self):
        return 'InvalidFileLine(num={}, hits={}, percentage={})'.format(self.num, self.hits, self.percentage)

class FunctionDict(OrderedDict):
    def as_table(self, add_info_dict):
        rows_list = [map(str, entry.as_list(add_info_dict)) for entry in self.values()]
        return grid_table(['Name', 'Hits', 'Start address', 'End address', 'Info'], rows_list)
    
    def __repr__(self):
        rows_list = [map(str, entry.as_list()) for entry in self.values()]
        return grid_table(['Name', 'Hits', 'Start address', 'End address', 'Info ID'], rows_list)

class ValidFileLineDict(dict):
    def __repr__(self):
        rows_list = [map(str, self[entry].as_list()) for entry in self]
        return headerless_table(rows_list)

class InvalidFileLineDict(dict):
    def __repr__(self):
        return UNREAD_FILE

class FileDict(OrderedDict):
    def __repr__(self):
        str_rep = ''
        for key in self:
            file = self[key]
            str_rep += repr(file)
        return str_rep

class SourceFile(object):
    def __init__(self, name, lines):
        self.name       = name
        self.lines      = lines
        self.valid      = isinstance(self.lines, ValidFileLineDict)
        self.hits       = 0

    def file_line_in_filtered_function(self, line, filtered_func_list):
        if line.symbol_at_line is not None:
            for func in filtered_func_list:
                if (line.symbol_at_line.name == func.name
                    and line.symbol_at_line.value == func.startaddress):
                    return True

    def update_symbol_at_line(self, line_num, address, symbols):
        self.lines[line_num].symbol_at_line = symbols[address]

    def increase_hitcount(self, hits, line_num):
        self.hits += hits
        self.lines[line_num].hits += hits

    def update_hits(self):
        self.hits = 0
        for line in self.lines:
            if self.lines[line].visible:
                self.hits += self.lines[line].hits

    def __repr__(self):
        return '\n{}\n\n{}\n\nHits inside this file: {} ({}%)\n'.format(self.name, 
                                                                   repr(self.lines), 
                                                                        self.hits, 
                                                                        format("%.2f" % self.percentage))

PROFILER_PC_SAMPLE_PACKET_TYPE = 67

# Masks for necessary data
PROFILER_PC_SAMPLE_DATA        = 0x1000
PROFILER_NEW_SAMPLE_DATA       = 0x4000
PROFILER_32_BIT_DATA           = 0x0001
# if not 32 bit
PROFILER_64_BIT_DATA           = 0x0002
PROFILER_ASID_DATA_PRESENT     = 0x0004
PROFILER_TC_ID_DATA_PRESENT    = 0x0008

def configure_pc_sample(enable_collection=True, sample_frequency=100, 
                        oversamples=1000, device=None):
    cpu_info = dict(cpuinfo(device))
    if cpu_info.get('has_dcr'):
        dcr = regs('ejtag_dcr', device=device)
        if not dcr.PCS:
            raise PCSampNotSupportedError('PC Sampling is not supported on this device.')

        dcr = dcr._replace(PCSe=enable_collection)
        regs('ejtag_dcr', dcr, device=device)
    else:
        # dbu based pc sample
        regs('dbu_drseg_pcs_control', 1, device=device)        

    config('sampling duration', int(oversamples/sample_frequency), device=device)
    config('sampling oversamples', oversamples, device=device)
    config("sampling threads", 1 if enable_collection else 0, device=device)

def get_channel_data_endian_str(device=None):
    return '<' if device.tiny.GetChannelDataEndian() == Endian.little else '>'

def find_position_of_first_packet(data):
    if data:
        pos = 0
        length = len(data)        
        while pos < length:
            # possible packet
            if ord(data[pos]) == PROFILER_PC_SAMPLE_PACKET_TYPE:    
                size = ord(data[pos + 1])
                # either matches length of sample or next tag header
                if pos + size == length or ord(data[pos + size]) == PROFILER_PC_SAMPLE_PACKET_TYPE:  
                    return pos, size
            else:
                pos += 1
        raise NoValidPacketError("Could not find a valid start packet in the pc sample data")    

class PCSample(object):
    def __init__(self, address, asid, tc_id):
        self.address            = address
        self.asid               = asid
        self.tc_id              = tc_id

    def __hash__(self):
        return hash((self.address, self.asid, self.tc_id))

    def __eq__(self, other):
        return (self.address == other.address 
                and self.asid == other.asid
                and self.tc_id == other.tc_id)

    def __repr__(self):
        return 'PCSample: address={}, asid={}, tc_id={}\n'.format(hex_string(self.address),
                                                                  self.asid, self.tc_id)

def packet_from_data(data, position, endian_str):
    # Packet header
    (packet_id, packet_size, flags) = struct.unpack_from(endian_str + "BBH", data, position)
    options = [("address", PROFILER_32_BIT_DATA, endian_str + "I"), 
               ("address", PROFILER_64_BIT_DATA, endian_str + "Q"),
               ("asid", PROFILER_ASID_DATA_PRESENT, endian_str + "H"), 
               ("tc_id", PROFILER_TC_ID_DATA_PRESENT, endian_str + "B")]

    fields_dict = dict() 

    next_field_position = struct.calcsize(endian_str + "BBH") + position
    
    # Only process pc sample packets with new data.
    if (packet_id == PROFILER_PC_SAMPLE_PACKET_TYPE 
        and flags & PROFILER_NEW_SAMPLE_DATA):
        for (name, mask, fmt) in options:
            if flags & mask:
                value = struct.unpack_from(fmt, data, next_field_position)[0]
                fields_dict[name] = value
                next_field_position += struct.calcsize(fmt)
            else:
                if not fields_dict.get(name):
                    fields_dict[name] = None
        return PCSample(fields_dict['address'], fields_dict['asid'], fields_dict['tc_id'])

def read_pc_samples(data, endian_str):
    packets = list()
    if data:
        position, packet_size = find_position_of_first_packet(data)
        data_length = len(data)
        for current_pos in xrange(position, data_length, packet_size):
            if (current_pos + packet_size) <= data_length:
                packets.append(packet_from_data(data, current_pos, endian_str))
    return packets

def flush_channel(device=None):
    # Stop collection before flushing the channel
    configure_pc_sample(enable_collection=False, device=device)
    while device.tiny.ChannelReadString(4):
        pass
    # Re-enable collection
    configure_pc_sample(enable_collection=True, device=device)

name = named('name')                 # |
hits = named('hits')                 # |
startaddress = named('startaddress') # |-> Note: must be the same name!
asc = named('asc')                   # |
desc = named('desc')                 # |

@command(sort_field=[namedstring(name), namedstring(hits), namedstring(startaddress)],
         sort_order=[namedstring(asc), namedstring(desc)])
def pcsampstats(sample_pickup_time, sort_field='name', sort_order='asc',
filter_exp='all', print_files_stats=False, device=None):
    '''Collect PC Sampling statistics over a given time in seconds.
    Results are shown in a table organised by function and optionally annotated source files.

    To sample for 3 seconds:
    >>> pcsampstats(3)

    Set 'filter_exp' to filter the results. For example by function name or number of hits:
    >>> pcsampstats(2, filter_exp='name == "foo"')
    >>> pcsampstats(2, filter_exp='hits > 100')

    You can change the sort order as follows:
    >>> pcsampstats(2, sort_field='startaddress', sort_order='desc')

    Annotated source files can be enabled with 'print_files_stats':
    >>> pcsampstats(2, print_files_stats=True)

    ================== =======================================================================
    Parameter          Meaning
    ================== =======================================================================
    sample_pickup_time Sampling time in seconds.
    sort_field         String giving the field used for sorting. One of 'name', 'startaddress' 
                       or 'hits'.
    sort_order         String giving the order used for sorting. One of 'asc' or 'desc'.
    filter_exp         Python expression as a string, used for filtering the functions table.
                       Note that if you enclose this with single quotes, strings in the 
                       expression must use double quotes or vice versa.
    print_files_stats  Set true to enable the printing of source file stats.
    ================== =======================================================================

    The result can be saved and reconfigured later:
    >>> result = pcsampstats(5)

    To change the sort order, change the sort_field/sort_order attributes.
    For example, this will update the functions table to be sorted by hits and descending.
    >>> result.sort_field = 'hits'
    >>> result.sort_order = 'desc'

    You can also re-filter your results. For example, to include all functions that start after 
    address 0x80000000:
    >>> result.result_filter = 'startaddress > 0x80000000' 
    To filter by tc_id/asid use:
    >>> result.result_filter = 'tc_id == 1'
    (Similar for asid.)

    You can also configure printing output by setting one of: 
        - result.print_func_table  (table of hits per function)
        - result.print_basic_stats (no of samples and sample collection rate)
        - result.print_files_stats (annotated source files)
    
    For example, to hide files stats:
    >>> result.print_files_stats = False
    Or show the functions table:
    >>> result.print_func_table = True
    '''
    elf_required(device)
    flush_channel(device)

    if not runstate().is_running:
        go()

    func_count = FunctionDict()
    pcsamples = Counter()
    file_dict = FileDict()
    endian = get_channel_data_endian_str(device)
    error = None
    try:
        start_time = time.time()
        while time.time() - start_time < sample_pickup_time:
            samples = read_pc_samples(device.tiny.ChannelReadString(4, 256 * 512), endian)
            pcsamples.update(samples)

    except KeyboardInterrupt as e:
        error = e
    
    end_time = time.time()
    configure_pc_sample(enable_collection=False, device=device)

    samples = read_pc_samples(device.tiny.ChannelReadString(4, 256 * 512), endian)
    pcsamples.update(samples)

    while samples:
        samples = read_pc_samples(device.tiny.ChannelReadString(4, 256 * 512), endian)
        pcsamples.update(samples)

    processing_result = final_step_processing(func_count, file_dict, pcsamples,
                                              end_time - start_time, sort_field, sort_order, 
                                              filter_exp, print_files_stats, device)  
    
    if error is None:
        return processing_result
    else:
        print processing_result
        raise error