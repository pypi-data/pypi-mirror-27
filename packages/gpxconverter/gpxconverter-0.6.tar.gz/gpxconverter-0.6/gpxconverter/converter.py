import getopt
import xml.etree.ElementTree as et
import csv
import re
import os
import sys


def convert(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, 'hi:o:', ['ifile=', 'ofile='])
    except getopt.GetoptError:
        print 'gpxconvert -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'gpxconvert -i <inputfile> -o <outputfile>'
            print 'for more help information. please visit github site.'
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg

    base_path = os.getcwd()
    xml_file = os.path.join(base_path, inputfile)
    if os.path.isfile(xml_file):
        _write_output(inputfile, outputfile, xml_file)
    else:
        print(inputfile +
              """ does not exist.Please check file name and try again!""")
        sys.exit()


def _write_output(inputfile, outputfile, xml_file):

    tree = et.parse(xml_file)
    root = tree.getroot()
    tags = []
    for child in root:
        child_tag = _get_tag(child)
        if child_tag != 'metadata':
            if child_tag not in tags:
                tags.append(child_tag)

    # row_count = 0  # count records
    ext_index = re.search(r'\.', inputfile[::-1])

    if outputfile:
        output_csv_file = outputfile
    else:
        output_csv_file = inputfile[: -(ext_index.start() + 1)]

    outputfiles = {}
    csv_headers = {}
    record_count = {}
    for tag in tags:
        outputfiles[tag] = output_csv_file + '_' + tag + '.csv'
        csv_headers[tag] = False
        record_count[tag] = 0

    for child in root:
        child_tag = _get_tag(child)
        if child_tag == 'wpt':
            waypoint = child
            elements = waypoint.getchildren()
            if not csv_headers['wpt']:
                with open(outputfiles[child_tag], 'w') as csv_file:
                    fieldnames = ['lat', 'lon']
                    header = _get_header(elements)
                    fieldnames.extend(header)
                    writer = csv.DictWriter(csv_file, fieldnames)
                    writer.writeheader()
                    csv_headers['wpt'] = True
            with open(outputfiles[child_tag], 'a') as csv_file:
                row_value = _parse_waypoints(waypoint, elements, fieldnames)
                writer = csv.DictWriter(csv_file, fieldnames)
                writer.writerow(row_value)

            record_count[child_tag] += 1

    for tag in tags:
        print(outputfiles[tag] + ' is created with ' +
              str(record_count[tag]) + ' record(s).')


def _get_header(elements):
    header = []
    for element in elements:
        header.append(_get_tag(element))

    return header


def _get_tag(element):
    return re.sub(r'^{.*?}', '', element.tag)


def _parse_waypoints(waypoint, elements, fieldnames):
    values = []
    values.append(waypoint.attrib['lat'])
    values.append(waypoint.attrib['lon'])

    for element in elements:
        elemnet_tag = _get_tag(element)
        if elemnet_tag == 'link':
            if element.text:
                link_value = '[' + element.text + ']'
            else:
                link_value = '[None]'
            link_value += '(' + element.attrib['href'] + ')'
            values.append(link_value)
        elif elemnet_tag == 'extensions':
            values.append('not support')
        else:
            values.append(element.text)

    return dict(zip(fieldnames, values))
