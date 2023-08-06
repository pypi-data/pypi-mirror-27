from imgtec.console.support import command
from imgtec.lib.namedenum import namedenum
from imgtec.lib.namedbitfield import namedbitfield
from imgtec.console import *
from imgtec.console.pure25519.ed25519_oop import SigningKey
import binascii
import struct

##############################################################################
# Constants
##############################################################################

SIGN_KEYSIZE = 32
ENCR_KEYSIZE = 16
SIGNSIZE = 64
CERTSIZE = 140

##############################################################################
# Error handling
##############################################################################

class RunError(Exception):
   pass

def run(main):
   try:
      main()
   except RunError as e:
      print "ERROR: %s" % e
      exit(1)

##############################################################################
# Crypto packages
##############################################################################


##############################################################################
# File access
##############################################################################

def read(filename, verbose, nbytes=None):
   if filename==None:
      return ""
   if verbose:
       print "Reading %s" % filename
   try:
      txt = open(filename, "rb").read()
   except:
      raise RunError("Cannot open file '%s' for read" % filename)
   if nbytes and len(txt)!=nbytes:
      raise RunError("File '%s' has invalid length" % filename)
   return txt

def write(filename, content, overwrite=True, tohex=False, tobyte=False):
   if not filename:
      return
   print "Writing %s" % filename
   # Overwrite
   if not overwrite and os.path.exists(filename):
      raise RunError("File '%s' already exists" % filename)
   # Open
   try:
      f = open(filename, "wb")
   except:
      raise RunError("Cannot open file '%s' for write" % filename)
   # Write
   if tohex:
      assert len(content)%4==0
      for pos in range(0, len(content), 4):
         f.write("%08X\n" % struct.unpack("<I", content[pos:pos+4]))
   elif tobyte:
      for pos in range(0, len(content)):
         f.write("%s\n" % binascii.hexlify(content[pos]))
   else:
      f.write(content)

##############################################################################
# Signature
##############################################################################

def sign(key, message):
   signing_key = SigningKey(key)
   signature = signing_key.sign(message)
   return signature

##############################################################################
# Console commands
##############################################################################

IR_DEVICEADDR = 5
IR_APBACCESS = 6

ID_REGS = {
"CIDR3"   : 0xFFC,
"CIDR2"   : 0xFF8,
"CIDR1"   : 0xFF4,
"CIDR0"   : 0xFF0,
"PIDR3"   : 0xFEC,
"PIDR2"   : 0xFE8,
"PIDR1"   : 0xFE4,
"PIDR0"   : 0xFE0,
"PIDR4"   : 0xFD0,
"DEVTYPE" : 0xFCC,
"DEVID"   : 0xFC8
}

DEVIDS = {
"DEVID_MDH"             : 1,
"DEVID_DBU"             : 2,
"DEVID_APB2JTAG"        : 3,
"DEVID_CORE"            : 4,
"DEVID_MMBLOCK"         : 5,
"DEVID_M7000_BRIDGE"    : 6,
"DEVID_CM"              : 7,
"DEVID_ESECURE"         : 8,
}

MfrCertType = namedenum('MfrCertType',
    SystemMfr       = 0,
    ChipMfr         = 1,
)

SlaveAddr = namedbitfield('SlaveAddr',
    [('dest_id', 17, 12), ('core_id', 11, 6), ('vpe_id', 3, 0)])

BootInfo = namedbitfield('Bootinfo', [
    ('HostImage',20,20),
    ('eSecureImage',16,16),
    ('HostUpgradeFlag',12,12),
    ('eSecureUpgradeFlag',8,8),
    ('BootStep',7,0)])


WDATA = 0x8
RDATA = 0x4
CONTROL = 0x0
WR_REQ = 1<<3 #8
RD_REQ = 1<<2 #4
WR_ACK = 1<<1 #2
RD_ACK = 1<<0 #1

TIMEOUT = 1000
DEBUG = 0

#@command()
def mdh_read_(byte_address):
    """ the inbuilt mdh read is broken on some console versions """
    tapi("5 %d" % IR_DEVICEADDR)

    tapd("32 %d" % (byte_address & 0xf80) )

    tapi("5 %d" % IR_APBACCESS)

    tapd("39 %d" % ((byte_address & 0x7c) | 0x3) )

    result = tapd("39 %d" % ((byte_address & 0x7c) | 0x2) )

    if (result[0] & 0x3) == 0x3:
        return result[0] >> 7

    raise RuntimeError("APB read failed try a lower TCK clock") #TODO retry abit if valid = 0

#@command()
def mdh_write_(byte_address,word):
    """ the inbuilt mdh read is broken on some console versions """
    tapi("5 %d" % IR_DEVICEADDR)

    tapd("32 %d" % (byte_address & 0xf80) )

    tapi("5 %d" % IR_APBACCESS)

    result = tapd("39 %d" % (word << 7 | (byte_address & 0x7c) | 0x1) )

    if (result[0] & 0x3) == 0x3:
        return

    raise RuntimeError("APB read failed try a lower TCK clock") #TODO retry abit if valid = 0

def esecure_read():
    """ internal only """
    mdh_write_(CONTROL,RD_REQ)
    timeout = 0
    while (mdh_read_(CONTROL) & RD_REQ) == 0: #wait for RD_REQ=1
        timeout+=1
        if timeout == TIMEOUT:
            raise RuntimeError("esecure_read: timeout waiting for RD_REQUEST to go high")
    data = mdh_read_(RDATA)
    mdh_write_(CONTROL,RD_ACK)
    timeout = 0
    while (mdh_read_(CONTROL) & RD_REQ) != 0: #wait for RD_REQ=0
        timeout+=1
        if timeout == TIMEOUT:
            raise RuntimeError("esecure_read: timeout waiting for RD_REQUEST to go low")
    mdh_write_(CONTROL,0)
    return data

#@command()
def esecure_write(data):
    """ internal only """
    mdh_write_(WDATA,data)
    mdh_write_(CONTROL,WR_REQ)
    timeout = 0
    while (mdh_read_(CONTROL) & WR_ACK) == 0:
        timeout+=1
        if timeout == TIMEOUT:
            raise RuntimeError("esecure_write: timeout waiting for WR_ACK to go high")
    mdh_write_(CONTROL,0)
    timeout = 0
    while (mdh_read_(CONTROL) & WR_ACK) != 0:
        timeout+=1
        if timeout == TIMEOUT:
            raise RuntimeError("esecure_read: timeout waiting for WR_ACK to go low")

def dump_id_regs():
    for k,v in ID_REGS.items():
        print k + " " + hex(mdh_read_(v))

def dump_return_data():
    """internal"""
    status = esecure_read()
    if status >> 16 == 0:
        while (mdh_read_(CONTROL) & RD_REQ) != 0:
            print hex(esecure_read())
    else:
        print decode_cmd_status(status)

status_strs = [
"Status at last tamper    : ",
"Timestamp of last tamper : ",
"Raw tamper status        : ",
"Current Time             : ",
"Boot Status              : ",
"eSecure Firmware Version : ",
"Host Firmware Version    : "]

def dump_status_data():
    i = 0
    while (mdh_read_(CONTROL) & RD_REQ) != 0:
        if i == 0 :
            esecure_read() #dont print size field

        if i < len(status_strs):
            if i == 4:
                bs = esecure_read()
                print status_strs[i]  + hex(bs) + " : "
                print repr(BootInfo(bs))
            else:
                print status_strs[i] + hex(esecure_read())
        else:
            print "Extra data: " + hex(esecure_read())
        i+=1

def decode_cmd_status(status):
    sts = (status >> 16) & 0xf
    if sts == 0: return "Okay"
    if sts == 1: return "Invalid Command"
    if sts == 2: return "Authorization Error"
    if sts == 3: return "Invalid Signature"
    if sts == 4: return "Bus Error"
    if sts == 5: return "Reserved"
    if sts == 6: return "Crypto Error"
    if sts == 7: return "Invalid Parameter"
    return "reserved"


def dump_status():
    esecure_write(0xC)
    esecure_write(0xFE020000)
    esecure_write(0x0)
    print "\nPublic Boot Key - Chip Manufacturer:"
    dump_return_data()

    esecure_write(0xC)
    esecure_write(0xFE020001)
    esecure_write(0x0)
    print "\nPublic Boot Key - System Manufacturer:"
    dump_return_data()

    esecure_write(0x8)
    esecure_write(0xFE010000)
    print "\nStatus:"
    dump_status_data()

    esecure_write(0x8)
    esecure_write(0xFE000000)
    print "\nSerial Number:"
    dump_return_data()

@command()
def esecurepresent(device=None):
    """ Check for the presence of the esecure hardware """
    jtagchain()
    #tapinfo()

    cidr1 = mdh_read_(ID_REGS["CIDR1"])

    if ((cidr1 >> 4) & 0xf) == 0xe:
        devid = mdh_read_(ID_REGS["DEVID"])
        if devid == 8:
            return True

    #autodetect()
    return False

def esecure_write_bytes(bytestr):
    if len(bytestr) % 4 != 0:
        raise RuntimeError("bytestr must always be a multiple of 4 bytes")

    words = []
    for pos in range(0, len(bytestr), 4):
        words.append(struct.unpack('<I',bytestr[pos:pos+4])[0])

    for word in words:
        if DEBUG: print "writing: "+ hex(word)
        esecure_write(word)

@command()
def esecurestatus(device=None):
    """ Dispaly the status of the esecure hardware """
    esecurepresent()
    dump_status()

@command()
def esecureenable(developer_key,developer_certificate,manufacturer_certificate_type,dbg_grant=0xffff,verbose=False,device=None):
    ''' Enable debug access to the requested devices
        developer_key - name (+ path) of the file containing the developers private (secret) key
        developer_certificate - name (+ path) of the file containing the developer certificate (signed by the manufacturer for the given developer key and allowed permissions).
        manufacturer_certificate_type - The type of certificate used to sign the developers certificate
            0 - Chip Manufacturer
            1 - System Manufacturer
        dbg_grant - 16bit bitmask, 1 bit for each cluster/core/subsystem to be unlocked dbg_grant[0] is the cpu within the eSecure block,
                    defaults to 0xffff as ultimately the actual access is controlled by the certificate.
    '''
    esecurepresent()

    #Send Get Challenge Command
    esecure_write(0x8)
    esecure_write(0xFD000000)

    #Read Challenge
    status = esecure_read()
    if status != 0x14:
        print "Unexpected status from get challenge: " + hex(status)
        dump_return_data()
        raise RuntimeError()

    if Command._interactive:
        print "challenge_data:"
    challenge = [0,0,0,0]
    for i in range(len(challenge)):
        challenge[i] = esecure_read()
        if Command._interactive:
            print hex(challenge[i])

    if (mdh_read_(CONTROL) & RD_REQ) != 0:
        print "Warning Extra Read data still pending:"
        dump_return_data()
        #todo raise exception ??

    command = 0xFD010000 | (manufacturer_certificate_type & 0x1)

    challenge.insert(0,dbg_grant)
    challenge.insert(0,command)

    challenge_bs = ""
    for word in challenge:
        challenge_bs += struct.pack('<I',word)

    if DEBUG: print "data to sign (command + param + challenge): " +  binascii.hexlify(challenge_bs)

    #sign challenge
    developer_cert = read(developer_certificate, Command._interactive)
    if verbose: print "developer cert:"
    if verbose: print binascii.hexlify(developer_cert)
    signing_key = read(developer_key, Command._interactive, SIGN_KEYSIZE)
    if verbose: print "developer key: " + binascii.hexlify(signing_key)

    signed_challenge = sign(signing_key,challenge_bs)
    if DEBUG: print "signed challenge:"
    if DEBUG: print binascii.hexlify(signed_challenge)

    #Send Debug Access Request Command
    if Command._interactive:
        print "Unlocking..."

    # total length = 4 /length/ + 4 /command/ + 4 /dbg_grant/ + developer_cert + signed_challenge
    msglen = 4 + 4 + 4 + len(developer_cert) + len(signed_challenge)

    if DEBUG: print "writing: " + hex(msglen)
    esecure_write(msglen)
    if DEBUG: print "writing: " + hex(command)
    esecure_write(command)
    if DEBUG: print "writing: " + hex(dbg_grant)
    esecure_write(dbg_grant)
    esecure_write_bytes(developer_cert) #140 bytes
    esecure_write_bytes(signed_challenge) #64 bytes

    status = esecure_read()

    if Command._interactive:
        print "Status: " + decode_cmd_status(status)

    return (status >> 16) & 0xf


