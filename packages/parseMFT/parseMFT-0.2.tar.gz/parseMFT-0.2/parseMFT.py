#!/usr/bin/python
import argparse
import os
import sys
import json
import csv
from datetime import datetime
from parsemft import mft # we only directly use this module and to avoid parsemft.mft.member() use 'from'
from signal import signal, SIGPIPE, SIG_DFL

verbose = 0
debug = False

# 1024 is valid for current version of Windows but should really get this value from somewhere
MFT_RECORD_SIZE = 1024

class Progress:
    """
        Implements a simple percentage-based progress spinner to STDERR
    """

    spinner = ['/', '-', '\\', '|']

    def __init__(self, total=100, step=25, msg='progress', prefix='[---] ', first_is_zero=True):
        """
            total  => what number represents completion
            step   => count between updates to spinner
            msg    => progress message (what is progressing)
            prefix => a prefix to put before the message
        """
        self.count = 0
        self.divisor = 1000
        self.multiple = 1
        self.first_is_zero = first_is_zero
        self.total = total
        self.step = step
        self.msg = prefix + msg + ':   0%  '

        sys.stderr.write(self.msg)

        self.messages = []

        # low values cause a divide by zero error
        if self.total < 1:
            self.total = self.divisor
            self.multiple = self.divisor
        elif self.total < self.divisor:
            self.multiple = self.divisor / self.total
            self.total = self.divisor
            self.step = 1

    def output(self, count):
        """
            Update progress to 'count'
        """
        if self.first_is_zero:
            count += 1

        # depending on step, percentage and spinner updates may not be concurrent
        if count * self.multiple % (self.total / self.divisor) == 0:
            sys.stderr.write('\b\b\b\b\b\b')
            sys.stderr.write('{0: >3d}% '.format(100 * count * self.multiple / self.total))
            sys.stderr.write(self.spinner[count / self.step % 4])
        elif count % self.step == 0:
            sys.stderr.write('\b' + self.spinner[count / self.step % 4])
        sys.stderr.flush()
        self.count = count

    def complete(self):
        """
            Assert that progress has completed
        """
        sys.stderr.write('\b\b\b\b\b\b100%  \b\b\n')
        if self.count < self.total:
            print >> sys.stderr, "[EEE] progress completed at %s of %s" % (self.count, self.total)
        sys.stderr.flush()
        for msg in self.messages:
            if type(msg) is tuple:
                for a in msg[:-1]:
                    sys.stderr.write(str(a))
                    sys.stderr.write(' ')
                sys.stderr.write(str(msg[-1]))
                sys.stderr.write('\n')
                sys.stderr.flush()
            else:
                print >> sys.stderr, msg
        self.currProgress = None

    def deferMessage(self, message):
        self.messages.append(message)

def errMsg(level, label, msg, opts, fatal=False, debug_only=False):
    if verbose < level or (debug_only and not debug):
        return
    elif fatal:
        if type(msg) is tuple:
            for message in msg:
                print >> sys.stderr, '[' + label * 3 + ']', message
        else:
            print >> sys.stderr, '[' + label * 3 + ']', msg
        sys.exit(1)
    elif opts.progress and opts.currProgress != None:
        if type(msg) is tuple:
            for message in msg:
                opts.currProgress.deferMessage(('[' + label * 3 + ']', message))
        else:
            opts.currProgress.deferMessage(('[' + label * 3 + ']', msg))
    else:
        if type(msg) is tuple:
            for message in msg:
                print >> sys.stderr, '[' + label * 3 + ']', message
        else:
            print >> sys.stderr, '[' + label * 3 + ']', msg

def fmt_excel(date_str):
    """
        Work around for original mft module behavior
    """
    return '="{}'.format(date_str)

def fmt_norm(date_str):
    """
        Work around for original mft module behavior
    """
    return date_str

def generateJSON(mftRecords, opts):
    """
        Calls json.dumps() with parameters determined from opts
            opts.indent => level of indentation
                            0 for condensed JSON output
    """
    indent = None
    sort_keys = False
    key_separator = ':'
    if opts.indent > 0:
        indent = opts.indent
        sort_keys = True
        key_separator = ': '

    for record in mftRecords:
        try:
            json.dumps(record, separators=(',', key_separator), indent=indent, sort_keys=sort_keys)
        except UnicodeDecodeError:
            errMsg(0, 'D', record, opts, fatal=True)

    return json.dumps(mftRecords, separators=(',', key_separator), indent=indent, sort_keys=sort_keys)

def formatTime(unixtime, opts):
    """
        Returns timestamp as a formatted string.
        Fractional seconds are retained when opts.keep_fractional_seconds is asserted
    """
    try:
        sFormat = "%Y-%m-%d %H:%M:%S"
        if opts.timesketch:
            sFormat = "%Y-%m-%dT%H:%M:%S+00:00"
        if opts.keep_fractional_seconds:
            sFormat += ".%f"
        # this should be the raw time read from the MFT record exchanged from NTFS epoch to unix epoch, it is in UTC
        if opts.localtz:
            date_str = datetime.fromtimestamp(unixtime).strftime(sFormat)
        else:
            date_str = datetime.utcfromtimestamp(unixtime).strftime(sFormat)
    except ValueError:
        # this happens when encountering a date before 1900
        errMsg(0, 'W', 'Invalid date: ' + str(unixtime), opts)
        date_str = str(datetime.utcfromtimestamp(unixtime))
    return date_str

def parseMFTRecord(raw_record, opts):
    """
        Parses an MFT raw record directly read from the MFT and returns it as a dictionary
        Internally this calls mft.parse_record() and then makes it JSON compatible
        In particular, tuple keys are expanded into subkeys
    """
    record = mft.parse_record(raw_record, opts)
    # the record returned uses tuples as keys which is not valid JSON
    stacks = {}
    for key in record.keys():
        try:
            (label, count) = key
            try:
                record[label, count]
                errMsg(0, 'D', "label: %s; count: %s" % (label, count), opts, debug_only=True)
                if label not in stacks:
                    stacks[label] = {}
                stacks[label][count] = record[label, count]
                record.pop(key)
            except KeyError:
                # some false positives... this will unpack 'f1' as ('f', 1)
                pass
        except ValueError:
            # if a key cannot be unpacked it isn't one we need
            pass
    for key in stacks:
        record[key] = stacks[key]

    errMsg(0, 'D', record, opts, debug_only=True)

    return record

def getMFTRecords(opts):
    """
        Read all MFT records from opts.filename and returns the dictionary
        Unless opts.inmemory only stores a "mini record" sufficient to generate full paths
            {
                'recordnum': record['recordnum']
                'filename':  record['filename']
                'fncnt':     record['fncnt']
                'par_ref':   record['fn'][0]['par_ref']
                'name':      record['fn'][?]['name']
            }
    """
    with open(opts.filename, 'rb') as mftfile:
        num_records = 0
        mftRecords = []
        if opts.progress:
            progress = Progress(total=opts.mftsize, msg='Parsing MFT Entries')
            opts.currProgress = progress

        # need to review the method for file reading
        raw_record = mftfile.read(MFT_RECORD_SIZE)
        while raw_record != "":
            record = parseMFTRecord(raw_record, opts)
            if record['recordnum'] == 0:
                record['recordnum'] = num_records
            if opts.inmemory:
                # convenience access
                if record['fncnt'] == 1:
                    record['par_ref'] = record['fn'][0]['par_ref']
                    record['name'] = record['fn'][0]['name']
                elif record['fncnt'] > 1:
                    record['par_ref'] = record['fn'][0]['par_ref']
                    for i in range(record['fncnt'] - 1):
                        errMsg(3, 'I', record['fn'][i], opts)
                        if record['fn'][i]['nspace'] == 1 or record['fn'][i]['nspace'] == 3:
                            record['name'] = record['fn'][i]['name']
                    if 'name' not in record:
                        record['name'] = record['fn'][record['fncnt'] - 1]['name']
                if 'name' not in record:
                    record['name'] = 'NoFNRecord'
                mftRecords.append(record)
            else:
                minirec = {}
                errMsg(0, 'D', record, opts, debug_only=True)

                minirec['recordnum'] = record['recordnum']
                minirec['filename'] = record['filename']
                minirec['fncnt'] = record['fncnt']
                if record['fncnt'] == 1:
                    minirec['par_ref'] = record['fn'][0]['par_ref']
                    minirec['name'] = record['fn'][0]['name']
                elif record['fncnt'] > 1:
                    minirec['par_ref'] = record['fn'][0]['par_ref']
                    for i in range(record['fncnt'] - 1):
                        errMsg(3, 'I', record['fn'][i], opts)
                        if record['fn'][i]['nspace'] == 1 or record['fn'][i]['nspace'] == 3:
                            minirec['name'] = record['fn'][i]['name']
                    if 'name' not in minirec:
                        minirec['name'] = record['fn'][record['fncnt'] - 1]['name']
                if 'name' not in minirec:
                    minirec['name'] = 'NoFNRecord'
                mftRecords.append(minirec)

            errMsg(0, 'D', "getMFTRecords() processing record %d out of %d" % (num_records, opts.mftsize), opts, debug_only=True)
            if opts.progress:
                progress.output(num_records)

            num_records += 1

            raw_record = mftfile.read(MFT_RECORD_SIZE)

    if opts.progress:
        progress.complete()

    return mftRecords

def expandPaths(mftRecords, opts):
    """ 
        Sets the full path for each entry in the MFT as 'filename' using getFolderPath()
    """
    if opts.progress:
        progress = Progress(total=opts.mftsize, msg='Building File Paths')
        opts.currProgress = progress
    # mftRecords = expandPaths(mftRecords, opts)
    # if filename starts with '/' or 'ORPHAN' we're done
    # else get filename of parent, add it to ours, and we're done
    # if we've not already calculated the full path...
    for record in mftRecords:
        if record['filename'] == '':
            if record['fncnt'] > 0:
                record['filename'] = getFolderPath(mftRecords, record, opts)
                errMsg(0, 'D', "[DDD] Filename (with path): %s" % record['filename'], opts, debug_only=True)
            else:
                record['filename'] = 'NoFNRecord'
                if 'name' not in record:
                    record['name'] = 'NoFNRecord'
        if opts.progress:
            progress.output(record['recordnum'])
    if opts.progress:
        progress.complete()

    return mftRecords

def getFolderPath(mftRecords, record, opts):
    """
        Recursively get and return the full path for the record
    """
    errMsg(0, 'D', "Building folder for record number (%d)" % record['recordnum'], opts, debug_only=True)

    # If we've already figured out the path name, just return it
    if record['filename'] != '':
        return record['filename']

    try:
        if record['par_ref'] == 5:  # Seq number 5 is "/", root of the directory
            return opts.path_sep + record['name']
    except KeyError:  # If there was an error getting the parent's sequence number, then there is no FN record
        return 'NoFNRecord'

    # Self referential parent sequence number.
    if record['par_ref'] == record['recordnum']:
        errMsg(0, 'D', ("Error, self-referential, while trying to determine path for record:", record), opts, debug_only=True)
        return 'ORPHAN' + opts.path_sep + record['name']

    try:
        parentRecord = mftRecords[ record['par_ref'] ]
        if parentRecord['filename'] == '':
            # need to get parent's path...
            parentRecord['filename'] = getFolderPath(mftRecords, parentRecord, opts)
        return parentRecord['filename'] + opts.path_sep + record['name']
    except KeyError:
        # parent reference is not in the MFT
        errMsg(-1, 'E', "KeyError() parent reference not in MFT for record " + str(record['recordnum']), opts)
        errMsg(1, 'E', ("KeyError() parent reference not in MFT for record", record), opts)
        return 'ORPHAN' + opts.path_sep + record['name']
    except IndexError:
        # parent reference should be in MFT, but is not
        errMsg(-1, 'E', "IndexError() parent reference not in MFT for record " + str(record['recordnum']), opts)
        errMsg(1, 'E', ("IndexError() parent reference not in MFT for record", record), opts)
        return 'ORPHAN' + opts.path_sep + record['name']

def parseMFT(opts):
    """
        Read all MFT records from opts.filename, generate full paths, and return the dictionary
        Unless opts.inmemory only stores a "mini record"
    """
    mftRecords = getMFTRecords(opts)

    # this is a waste of effort when creating a bodyfile without opts.fullpath
    if opts.bodyfile and not opts.fullpath:
        return mftRecords
    else:
        return expandPaths(mftRecords, opts)

def getHeaders(opts):
    """
        Returns list of CSV fields for the output style
            opts.bodyfile   -> generate MACB bodyfile header
            opts.timesketch -> generate timesketch compatible header row
            opts.timeline   -> generate plaso/l2t compatible header row
                otherwise use the default CSV header
    """
    if opts.bodyfile:
        return ['MD5', 'name', 'inode', 'mode_as_string', 'UID', 'GID', 'size', 'atime', 'mtime', 'ctime', 'crtime']
    elif opts.timesketch:
        return ['message', 'timestamp', 'datetime', 'timestamp_desc', 'full_path', 'date_type', 'extra']
    elif opts.timeline:
        return ['date','time','timezone','MACB','source','sourcetype','type','user','host','short','desc','version','filename','inode','notes','format','extra']
    else:
        return mft.mft_to_csv(None, True, opts)

def getRow(record, opts):
    """
        Returns list of CSV values for the record according to option
            opts.bodyfile   -> generate MACB bodyfile
            opts.timesketch -> generate timesketch compatible row
            opts.timeline   -> generate plaso/l2t compatible row
                otherwise use the default CSV
    """
    if opts.bodyfile:
        return getBodyFileRow(record, opts)
    elif opts.timesketch:
        return getTimeSketchRow(record, opts)
    elif opts.timeline:
        return getTimelineRow(record, opts)
    else:
        return getCSVRow(record, opts)

def getCSVRow(record, opts):
    """
        Returns a list of values according to default CSV fields
    """
    if 'baad' in record:
        csvRow = [ str(record['recordnum']), "BAAD MFT Record" ]
        return csvRow

    csvRow = [record['recordnum'], mft.decode_mft_magic(record), mft.decode_mft_isactive(record),
                  mft.decode_mft_recordtype(record)]

    if 'corrupt' in record:
        tmpList = [ str(record['recordnum']), "Corrupt", "Corrupt", "Corrupt MFT Record" ]
        csvRow.extend(tmpList)
        return csvRow

    tmpList = [str(record['recordnum'])]
    csvRow.extend(tmpList)

    if record['fncnt'] > 0:
        csvRow.extend([str(record['fn'][0]['par_ref']), str(record['fn'][0]['par_seq'])])
    else:
        csvRow.extend(['NoParent', 'NoParent'])

    if record['fncnt'] > 0 and 'si' in record:
        filename_buffer = [
            record['filename'],
            formatTime(record['si']['crtime'], opts),
            formatTime(record['si']['mtime'], opts),
            formatTime(record['si']['atime'], opts),
            formatTime(record['si']['ctime'], opts),
            formatTime(record['fn'][0]['crtime'], opts),
            formatTime(record['fn'][0]['mtime'], opts),
            formatTime(record['fn'][0]['atime'], opts),
            formatTime(record['fn'][0]['ctime'], opts) ]
    elif 'si' in record:
        filename_buffer = [
            'NoFNRecord',
            formatTime(record['si']['crtime'], opts),
            formatTime(record['si']['mtime'], opts),
            formatTime(record['si']['atime'], opts),
            formatTime(record['si']['ctime'], opts),
            'NoFNRecord', 'NoFNRecord', 'NoFNRecord', 'NoFNRecord',
        ]

    else:
        filename_buffer = [
            'NoFNRecord',
            'NoSIRecord', 'NoSIRecord', 'NoSIRecord', 'NoSIRecord',
            'NoFNRecord', 'NoFNRecord', 'NoFNRecord', 'NoFNRecord',
        ]

    csvRow.extend(filename_buffer)

    if 'objid' in record:
        objid_buffer = [
            record['objid']['objid'],
            record['objid']['orig_volid'],
            record['objid']['orig_objid'],
            record['objid']['orig_domid'],
        ]
    else:
        objid_buffer = ['', '', '', '']

    csvRow.extend(objid_buffer)

    # If this goes above four FN attributes, the number of columns will exceed the headers
    # instead of limiting the columns could make the columns variable to meet the rows
    for i in range(1, min(4, record['fncnt'])):
        filename_buffer = [
            record['fn'][i]['name'],
            formatTime(record['fn'][i]['crtime'], opts),
            formatTime(record['fn'][i]['mtime'], opts),
            formatTime(record['fn'][i]['atime'], opts),
            formatTime(record['fn'][i]['ctime'], opts),
        ]
        csvRow.extend(filename_buffer)

    # Pad out the remaining FN columns
    if record['fncnt'] < 2:
        tmpList = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    elif record['fncnt'] == 2:
        tmpList = ['', '', '', '', '', '', '', '', '', '']
    elif record['fncnt'] == 3:
        tmpList = ['', '', '', '', '']
    else:
        tmpList = []

    csvRow.extend(tmpList)

    for record_str in ['si', 'al']:
        csvRow.append('True') if record_str in record else csvRow.append('False')

    csvRow.append('True') if record['fncnt'] > 0 else csvRow.append('False')

    for record_str in [
        'objid',
        'volname',
        'volinfo',
        'data',
        'indexroot',
        'indexallocation',
        'bitmap',
        'reparse',
        'eainfo',
        'ea',
        'propertyset',
        'loggedutility',
    ]:
        csvRow.append('True') if record_str in record else csvRow.append('False')

    if 'notes' in record:  # Log of abnormal activity related to this record
        csvRow.append(record['notes'])
    else:
        csvRow.append('None')
        record['notes'] = ''

    if 'stf-fn-shift' in record:
        csvRow.append('Y')
    else:
        csvRow.append('N')

    if 'usec-zero' in record:
        csvRow.append('Y')
    else:
        csvRow.append('N')

    if record['ads'] > 0:
        csvRow.append('Y')
    else:
        csvRow.append('N')

    return csvRow

def bodyFixTime(unixtime, opts):
    if unixtime > 0:
        return int(unixtime)
    else:
        return opts.invalid_data

def getBodyFileRow(record, opts):
    """
        Returns a list of values according to bodyfile fields
    """
    if record['fncnt'] > 0:

        if opts.fullpath:  # Use full path
            name = record['filename']
        else:
            name = record['fn'][0]['name']

        if opts.stdinfo:  # Use STD_INFO
            row = ['0', name, '0', '0', '0', '0',
                            int(record['fn'][0]['real_fsize']),
                            bodyFixTime(record['si']['atime'], opts),
                            bodyFixTime(record['si']['mtime'], opts),
                            bodyFixTime(record['si']['ctime'], opts),
                            bodyFixTime(record['si']['crtime'], opts)]
        else:  # Use FN
            row = ['0', name, '0', '0', '0', '0',
                            int(record['fn'][0]['real_fsize']),
                            bodyFixTime(record['fn'][0]['atime'], opts),
                            bodyFixTime(record['fn'][0]['mtime'], opts),
                            bodyFixTime(record['fn'][0]['ctime'], opts),
                            bodyFixTime(record['fn'][0]['crtime'], opts)]

    else:
        if 'si' in record:
            row = ['0', 'No FN Record', '0', '0', '0', '0', '0',
                             bodyFixTime(record['si']['atime'], opts),
                             bodyFixTime(record['si']['mtime'], opts),
                             bodyFixTime(record['si']['ctime'], opts),
                             bodyFixTime(record['si']['crtime'], opts)]
        else:
            row = ['0', 'Corrupt Record', '0', '0', '0', '0', '0', 0, 0, 0, 0]

    return row

def l2tFixTime(unixtime, opts):
    """
        Returns a tuple of (date, time) from unixtime in either local or UTC depending on opts.localtz
    """
    dateFormat = '%Y-%m-%d'
    timeFormat = '%H:%M:%S'
    if opts.legacy_l2t_date:
        dateFormat = '%m/%d/%Y'
    if opts.keep_fractional_seconds:
        timeFormat += '.%f'

    try:
        if opts.localtz:
            date = datetime.fromtimestamp(unixtime).strftime(dateFormat)
            time = datetime.fromtimestamp(unixtime).strftime(timeFormat)
        else:
            date = datetime.utcfromtimestamp(unixtime).strftime(dateFormat)
            time = datetime.utcfromtimestamp(unixtime).strftime(timeFormat)
    except ValueError:
        # raised when year is < 1900, e.g., 1636 -- which shouldn't even be happening in NTFS...
        errMsg(-1, 'W', "date '%s' is invalid" % str(datetime.utcfromtimestamp(unixtime)), opts)
        (date, time) = str(datetime.utcfromtimestamp(unixtime)).split(' ')
    return (date, time)

def getTimelineRow(record, opts):
    """
        Returns a list of values according to plaso/l2t fields
        [date,time,timezone,MACB,source,sourcetype,type,user,host,short,desc,version,filename,inode,notes,format,extra]
            http://code.google.com/p/log2timeline/wiki/l2t_csv and
            http://forensicswiki.org/wiki/L2T_CSV
    """
    # initialize the fields
    l2tFields = getHeaders(opts)
    l2tRecord = {}
    for field in l2tFields:
        l2tRecord[field] = ''

    l2tRecord['timezone'] = 'FILE'
    l2tRecord['source'] = 'FILE'
    l2tRecord['sourcetype'] = 'NTFS $MFT'
    if 'fn' in record and 'name' in record['fn'][0]:
        l2tRecord['short'] = record['fn'][0]['name']
    else:
        l2tRecord['short'] = 'NoFNRecord'
    l2tRecord['version'] = 2
    l2tRecord['filename'] = record['filename']
    l2tRecord['inode'] = record['recordnum']
    #l2tRecord['notes'] = record['file']
    l2tRecord['format'] = 'parseMFT'
    #l2tRecord['extra'] = record['file']

    rows = {}
    types = {
        'atime': 'Last Accessed',
        'mtime': 'Last Written',
        'ctime': 'Last Changed',
        'crtime': 'File Created'
    }
    macb = {
        'atime': '.a..',
        'mtime': 'm...',
        'ctime': '..c.',
        'crtime': '...b'
    }

    for which_time in types:
        l2tRecord['type'] = types[which_time]
        l2tRecord['MACB'] = macb[which_time]
        l2tRecord['notes'] = ''

        if record['fncnt'] > 0:
            l2tRecord['desc'] = '$FN 0 %s time' % l2tRecord['type']
            (date, time) = l2tFixTime(record['fn'][0][which_time], opts)
        elif 'si' in record:
            l2tRecord['desc'] = '$SI %s time' % l2tRecord['type']
            (date, time) = l2tFixTime(record['si'][which_time], opts)
        else:
            l2tRecord['desc'] = 'unknown %s time' % l2tRecord['type']
            (date, time) = (opts.invalid_data, opts.invalid_data)
            #l2TRecord['notes'] = 'invalid date: %s (%s)' % (, formatTime())

        l2tRecord['date'] = date
        l2tRecord['time'] = time

        rows[which_time] = []
        for field in l2tFields:
            rows[which_time].append(l2tRecord[field])
        
    if record['recordnum'] == 0 and record['filename'] == 'NoFNRecord':
        errMsg(0, 'D', (rows, '\n\n', record), opts, fatal=True)
    
    return rows

def getTimeSketchRow(record, opts):
    # From: https://github.com/google/timesketch/blob/master/docs/CreateTimelineFromJSONorCSV.md
    # [
    #   {
    #   "message": "the message",
    #   "timestamp": <unixdate>,
    #   "datetime": "YYYY-MM-DDTHH:MI:SS+00:00",
    #   "timestamp_desc": "action",
    #   "extra_field_<number>": "data"
    #   },
    # ]
    # unfortunately, this is incorrect and it actually expects all values to be strings in JSON
    rows = {}
    types = {
        'atime': ['Last Read', 'windows:mft::accessed'],
        'mtime': ['Last Written', 'windows:mft::modified'],
        'ctime': ['Last Changed', 'windows:mft::changed'],
        'crtime': ['Created', 'windows:mft::created']
    }
    tsHeaders = getHeaders(opts)
    # initialize record row data
    data = {}
    for field in tsHeaders:
        data[field] = ''
    data['message'] = record['filename']
    data['full_path'] = record['filename']

    if record['filename'] == 'NoFNRecord':
        data['message'] = 'NoFNRecord'
        data['timestamp'] = 0
        data['datetime'] = opts.invalid_data
        data['date_type'] = 'windows:mft:NoFNRecord'
        data['timestamp_desc'] = 'MFT timestamp'
        row = []
        for field in tsHeaders:
            row.append(data[field])
        return row

    for which_time in types:
        this = data.copy()
        this['timestamp_desc'] = types[which_time][0]
        this['date_type'] = types[which_time][1]
        if record['fncnt'] > 0:
            this['timestamp'] = record['fn'][0][which_time]
            this['datetime'] = formatTime(record['fn'][0][which_time], opts)
            this['date_type'] = this['date_type'].replace('::', ':fn[0]:')
        elif 'si' in record:
            this['timestamp'] = record['si'][which_time]
            this['datetime'] = formatTime(record['si'][which_time], opts)
            this['date_type'] = this['date_type'].replace('::', ':si:')
        else:
            this['timestamp'] = 0
            this['datetime'] = opts.invalid_data
            this['date_type'] = this['date_type'].replace('::', ':not_found:')
        row = []
        for field in tsHeaders:
            row.append(this[field])
        rows[which_time] = row

    return rows
    
def outputMFT(mftRecords, opts):
    """
        Prints parsed MFT records to STDOUT, or file when opts.output is specified
        Unless opts.inmemory was specified, re-reads the MFT one record at time as it writes the data
        Handles file opening and closing
    """
    if opts.progress:
        progress = Progress(total=opts.mftsize, msg='Outputting MFT Data')
        opts.currProgress = progress
    # Output is complicated because we may be doing it all at once (JSON)
    # or as we read the file (without --inmemory). Further, we may be
    # writing to stdout rather than to a file. So we obtain a handle to
    # our output mechanism and use that from here on out.
    opts.outputHandle = sys.stdout
    if opts.output:
        opts.outputHandle = open(opts.output, 'wb')
    # if doing csv, output headers...
    if opts.csv:
        opts.csvFileHandle = csv.writer(opts.outputHandle, delimiter=opts.delimiter, lineterminator='\n')
        opts.csvFileHandle.writerow( getHeaders(opts) )
        if opts.inmemory:
            for record in mftRecords:
                output(record, opts)
                # handle ADS (alternate data streams)
                if record['ads'] > 0:
                    for i in range(record['ads']):
                        errMsg(0, 'D', "ADS:", str(record['data_name'][i]), opts, debug_only=True)
                        record_ads = record.copy()
                        record_ads['filename'] = record['filename'] + ':' + record['data_name'][i]
                        output(record_ads, opts)
                if opts.progress:
                    progress.output(record['recordnum'])
        else:
            # since we didn't store the full record...
            with open(opts.filename, 'rb') as mftfile:
                mftfile.seek(0)
                raw_record = mftfile.read(MFT_RECORD_SIZE)

                while raw_record != "":
                    record = parseMFTRecord(raw_record, opts)
                    errMsg(0, 'D', ("outputMFT() record", record), opts, debug_only=True)

                    # get the expanded file path
                    record['filename'] = mftRecords[ record['recordnum'] ]['filename']
                    output(record, opts)

                    # handle ADS (alternate data streams)
                    if record['ads'] > 0:
                        for i in range(record['ads']):
                            errMsg(0, 'D', "ADS: %s" % (record['data_name'][i]), opts, debug_only=True)
                            record_ads = record.copy()
                            record_ads['filename'] = record['filename'] + ':' + record['data_name'][i]
                            output(record_ads, opts)

                    if opts.progress:
                        progress.output( record['recordnum'] )

                    raw_record = mftfile.read(MFT_RECORD_SIZE)
    elif opts.json:
        # JSON must be done all at once so the only way to get complete output is to use --inmemory
        # due to the data structure, ADS data is present but not "handled"
        opts.outputHandle.write( generateJSON(mftRecords, opts) )
        if opts.progress:
            progress.output(opts.mftsize)
    else:
        raise AttributeError('missing output option')

    # closing stdout is of small importance as all error messages go to stderr
    opts.outputHandle.close()

    if opts.progress:
        progress.complete()

def output(record, opts):
    """
        Prints the record, according to the output format, to the opened file
    """
    row = getRow(record, opts)
    # each row is a list of fields so formats that return multiple rows per record do so as a dictionary
    if type(row) is dict:
        for key in row:
            opts.csvFileHandle.writerow(row[key])
    elif type(row) is list:
        opts.csvFileHandle.writerow(row)
    elif row is None:
        errMsg(-1, 'W', ('no row found for record\n', json.dumps(record, separators=(',', ': '), indent=4, sort_keys=True)), opts)
    else:
        raise AttributeError('Unexpected row type %s for record %d' % (type(row), record['recordnum']))
        sys.exit(1)
    
def parseOpts(args):
    """ 
        Requires <filename> to read MFT from and an output format to use (-c|-j|-b|-g|-t)
    """
    global verbose, debug, path_sep
    parser = argparse.ArgumentParser(description='Parse Windows MFT and output timeline', epilog='To avoid unicode errors in the console: "export PYTHONIOENCODING=UTF-8"')
    parser.add_argument('filename', metavar='MFT_FILE', help='read MFT from FILE')

    # File structure
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--csv', action='store_true', help='CSV format output')
    group.add_argument('-j', '--json', action='store_true', help="JSON format output [use --inmemory to get all data]")

    # Format options that are tweaks to the default CSV output
    group.add_argument('-b', '--bodyfile', action='store_true', help="Bodyfile format output")
    group.add_argument('-g', '--timesketch', action='store_true', help="Timesketch compatible output")
    group.add_argument('-t', '--timeline', action='store_true', help='Plaso/log2timeline compatible output')

    parser.add_argument('-o', '--output', metavar='FILE', help='write results to FILE [default is STDOUT]')

    # CSV options
    parser.add_argument('-e', '--excel', action='store_true', help="Make output Excel friendly, normally used with -c")

    # JSON options
    parser.add_argument('-i', '--indent', type=int, default=4, help="Number of spaces to indent in json output; only meaningful when used with -j")

    # Time options
    parser.add_argument('-s', '--stdinfo', action='store_true', help='Prefer STD_INFO timestamps to FILENAME timestamps')
    parser.add_argument('-l', '--localtz', action='store_true', help='Report times using local timezone')
    parser.add_argument('-k', '--keep_fractional_seconds', action='store_true', help="Keep fractional seconds in date/time stamps")
    parser.add_argument('--legacy_l2t_date', action='store_true', help='Use legacy l2t "MM/DD/YYYY" date format')
    
    # Other options
    parser.add_argument('-f', '--fullpath', action='store_true', help='Bodyfile uses full path rather than just filename; ignored without -b')
    parser.add_argument('-x', '--invalid_data', default='', metavar='STRING', help='Text to use for an invalid or missing data, e.g., when time is zero (1601-01-01 00:00:00) [default is an empty string]')
    parser.add_argument('-w', '--windows_path', action='store_true', help='File paths should use the windows path separator instead of linux')
    parser.add_argument('--max_memory', type=int, default=4, help='Set the maximum memory for --inmemory [default is 4 GB]')

    parser.add_argument('-a', '--anomaly', action='store_true', help='Turn on anomaly detection')

    # General options
    parser.add_argument('-m', '--inmemory', action='store_true', help='Load in a single pass. Faster but uses more memory.')
    parser.add_argument('--estimate_memory_only', action='store_true', help='Terminate after estimating the amount of memory required.')
    parser.add_argument('-p', '--progress', action='store_true', help='Show systematic progress reports')

    # Generic options
    parser.add_argument('-d', '--debug', action='store_true', help='Turn on debugging output [implies -vvv, use -q to suppress verbose output]')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Show non-fatal errors')
    parser.add_argument('-q', '--quiet', action='count', default=0, help='Suppress error messages')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s 0.2 2017-12-19')
    
    opts = parser.parse_args(args)
    verbose = opts.verbose - opts.quiet
    if opts.debug:
        debug = opts.debug
        verbose += 3
    if opts.windows_path:
        opts.path_sep = '\\'
    else:
        opts.path_sep = '/'

    opts.date_formatter = fmt_norm
    if opts.excel:
        opts.date_formatter = fmt_excel

    # Implied options to keep options more straightforward for the user
    # Internally, the actual dichotomy is CSV|JSON with the rest being
    # tweaks that however are normally used with CSV. If needed, a
    # --force_json option can be added to set these as JSON instead.
    if opts.bodyfile or opts.timesketch or opts.timeline:
        opts.csv = True
    if opts.csv:
        opts.delimiter = ','
        if opts.bodyfile:
            opts.delimiter = '|'
    if opts.estimate_memory_only:
        opts.inmemory = True
    if opts.timesketch and opts.localtz:
        opts.localtz = False
        if verbose > -1:
            print >> sys.stderr, "[WWW] --localtz ignored with --timesketch"

    # do not overwrite files
    if opts.output and os.path.exists(opts.output):
        if verbose > -1:
            print >> sys.stderr, "[EEE] '%s' already exists" % opts.output
        return 3
    # ensure the file to read exists
    if not os.path.isfile(opts.filename):
        if verbose > -1:
            print >> sys.stderr, "[EEE] '%s' is not a file" % opts.filename
        return 2

    # informational notices and warnings
    if opts.json and not opts.inmemory:
        if verbose > -1:
            print >> sys.stderr, "[WWW] JSON output will be incomplete without --inmemory"
    if opts.csv and opts.indent != 4:
        # not default value
        if verbose > 0:
            print >> sys.stderr, "[III] --indent only useful with --json"
    if opts.json and opts.excel:
        if verbose > 0:
            print >> sys.stderr, "[III] --excel useless with --json"
    if opts.fullpath and not opts.bodyfile:
        if verbose > -1:
            print >> sys.stderr, "[WWW] --fullpath redundant without --bodyfile"
    if opts.keep_fractional_seconds and opts.bodyfile:
        if verbose > -1:
            print >> sys.stderr, "[WWW] --keep_fractional_seconds ignored with --bodyfile"
    if opts.legacy_l2t_date and not opts.timeline:
        if verbose > -1:
            print >> sys.stderr, "[WWW] --legacy_l2t_date ignored without --timeline"

    # The number of records in the MFT is the size of the MFT / 1024
    opts.mftsize = long(os.path.getsize(opts.filename)) / 1024

    if (opts.inmemory and verbose > -1) or verbose > 0:
        print >> sys.stderr, '[III] There are %d records in the MFT' % opts.mftsize

    ## from David Kovar...
    # The size of the full MFT is approximately the number of records * the avg record size
    # Avg record size was determined empirically using some test data, 4500 per record
    ## my observation
    # on launch uses ~10 MB
    # MFT 1,  273664 entries, ~120 MB parsed,  ~160 MB peak, -m: ~3.1 GB, 12163 bytes/record
    # MFT 2,  203008 entries, ~100 MB parsed,  ~125 MB peak, -m: ~2.2 GB, 11636 bytes/record
    # MFT 3, 2089984 entries, ~850 MB parsed, ~1180 MB peak, -m: ~20. GB, 10275 bytes/record
    # This is more than twice as much memory as the prior estimate, so even with such a
    # small sample the formula clearly needs to be adjusted. Without -m it looks like a
    # peak of 650 bytes per record and with -m it is about 12,000 bytes per record (the
    # sparser the MFT and the flatter the directory structure the fewer bytes per record,
    # but since we won't know we should be conservative).
    # To be more precise use something like guppy.
    opts.sizeinmb = (opts.mftsize * 0.012, opts.mftsize * 0.00065)

    if (opts.inmemory and verbose > -1) or verbose > 0:
        print >> sys.stderr, '[III] An estimated %d MB of memory is needed to keep in RAM (%d MB otherwise)' % opts.sizeinmb
    if opts.inmemory and opts.sizeinmb[0] > opts.max_memory * 1024:
        print >> sys.stderr, '[EEE] --inmemory may require more than the %d GB RAM limit. If there is enough system RAM run again with --max_memory=%d' % (opts.max_memory, (opts.sizeinmb[0]/1024+1))
        sys.exit(1)
    if opts.estimate_memory_only:
        sys.exit(0)

    return opts

def main(args):
    """ Sets up options for how to process the MFT and calls parseMFT() then outputMFT() """
    opts = parseOpts(args)
    mftRecords = parseMFT(opts)
    outputMFT(mftRecords, opts)

if __name__ == '__main__':
    # Restore default handler for SIG_PIPE (http://coding.derkeiler.com/Archive/Python/comp.lang.python/2004-06/3823.html)
    # this avoids a useless IOError() when piping to another application and that application closes early by simply restoring
    # the default handler
    signal(SIGPIPE, SIG_DFL)
    sys.exit(main(sys.argv[1:]))
