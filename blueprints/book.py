# coding: utf-8
__author__ = 'Hansheng Zhang'

import xml.etree.ElementTree as ET

class Author(object):
    TYPE_AUTHOR = "Author"
    TYPE_TRANSLATOR = "Translator"

    def __init__(self):
        super(Author, self).__init__()
        self.t = Author.TYPE_AUTHOR
        self.name = ""

    def load_from_xml(self, author_xml):
        self.t = author_xml.tag
        self.name = author_xml.text

    def to_xml(self):
        author_xml = ET.Element(self.t)
        author_xml.text = self.name
        return author_xml


class Record(object):
    def __init__(self):
        super(Record, self).__init__()
        self.year = 0
        self.month = 0
        self.day = 0
        self.title = ""
        self.authors = []

        self.publisher = ""
        self.publish_year = 0

        self.comment = ""

    def load_from_xml(self, record_xml):
        date = record_xml.find('Date')
        self.year = int(date.find('Year').text)
        self.month = int(date.find('Month').text)
        self.day = int(date.find('Day').text)
        self.title = record_xml.find('Title').text

        self.authors = []
        author_xmls = record_xml.find('Authors')
        if not author_xmls == None:
            for author_xml in list(author_xmls):
                author = Author()
                author.load_from_xml(author_xml)
                self.authors.append(author)
        publisher_xml = record_xml.find('Publisher')
        if not publisher_xml == None:
            self.publisher = publisher_xml.text
        else:
            self.publisher = ""
        publish_year_xml = record_xml.find("PublishYear")
        if not publish_year_xml == None:
            self.publish_year = int(publish_year_xml.text)
        else:
            self.publish_year = 0

        self.comment = record_xml.find('Comment').text
        if self.comment == None:
            self.comment = ""

    def to_xml(self):
        record_xml = ET.Element('Record')

        date = ET.SubElement(record_xml, 'Date')
        year_xml = ET.SubElement(date, 'Year')
        year_xml.text = str(self.year)
        month_xml = ET.SubElement(date, 'Month')
        month_xml.text = str(self.month)
        day_xml = ET.SubElement(date, 'Day')
        day_xml.text = str(self.day)

        title_xml = ET.SubElement(record_xml, 'Title')
        title_xml.text = self.title
        if len(self.authors) > 0:
            authors_xml = ET.SubElement(record_xml, 'Authors')
            for author in self.authors:
                authors_xml.append(author.to_xml())

        if self.publisher:
            publisher_xml = ET.SubElement(record_xml, 'Publisher')
            publisher_xml.text = self.publisher
        if self.publish_year:
            publish_year_xml = ET.SubElement(record_xml, 'PublishYear')
            publish_year_xml.text = str(self.publish_year)
        comment_xml = ET.SubElement(record_xml, 'Comment')
        comment_xml.text = self.comment
        return record_xml


data_dir = "data"
file_path = data_dir + "/2015.xml"
tree = ET.parse(file_path)
root = tree.getroot()


def add_book(year, month, day, title, comment):
    record = ET.SubElement(root, 'Record')

    date = ET.SubElement(record, 'Date')
    year_xml = ET.SubElement(date, 'Year')
    year_xml.text = str(year)
    month_xml = ET.SubElement(date, 'Month')
    month_xml.text = str(month)
    day_xml = ET.SubElement(date, 'Day')
    day_xml.text = str(day)

    title_xml = ET.SubElement(record, 'Title')
    title_xml.text = title

    comment_xml = ET.SubElement(record, 'Comment')
    comment_xml.text = comment
    tree.write(file_path)


def print_record_info():
    total_count = 0
    for record_xml in root.iter('Record'):
        record = Record()
        record.load_from_xml(record_xml)
        print "%s/%s/%s\t%s\t" % (record.year, record.month, record.day, record.title),
        for author in record.authors:
            print author.name + "\t",
        print record.publisher + ",",
        print record.publish_year,
        print "\t" + record.comment
        total_count = total_count + 1
    print "total: %s books" % total_count


# print_record_info()
def all_records():
    records = []
    for record_xml in root.iter('Record'):
        record = Record()
        record.load_from_xml(record_xml)
        records.append(record)
    return records


from flask import Blueprint, render_template
book = Blueprint('book', __name__)

@book.route('/')
def get_root():
    return render_template("book_index.html")

from flask import Response
import json

@book.route('/list')
def get_list():
    rlt = []
    for record in all_records():
        rlt.append({'date':'%04d-%02d-%02d' % (record.year, record.month, record.day), 'name': record.title})
    rlt.reverse()
    return Response(json.dumps(rlt), mimetype='application/json')

