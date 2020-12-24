from docx import Document  # api
from docx import document as document_real # need document.Document as type-assertion
from docx.enum.style import WD_BUILTIN_STYLE
from docx.table import Table  # for type assertion
from docx.text.paragraph import Paragraph  # for type assertion
original_docx_file = r'D:\desktop_files_and_folders\word\separate_word_and_concatenate\中心节点各小节(read_only).docx'
target_docx_file = r'D:\desktop_files_and_folders\word\separate_word_and_concatenate\out.docx'

table_flag = ''
section_end_flag = '__结束__'
"""
the goal of this python module:
 - read original_docx_file, and get those UNIQUE section_objs
 - save these section_objs into docx files
 - use UI to freely change the order of these section_objs  # todo now
 - after changing the order of sections, the section number should also be ordered automatically
"""


class section_obj:
    """obj for the smallest word section, will be saved into TreeWidgetItem afterwards"""
    def __init__(self, para_dict: dict):
        """
        initiate the section_obj
        :param para_dict: a dict that stores the parameters which object-initiation needs
        """
        self.section_lv = 0  # 章节的级别, 包括1级, 2级...
        self.elements_list = []

        for key in para_dict.keys():
            setattr(self, key, para_dict[key])
        pass
    pass


class DocxHelper:
    """class that takes responsible to handle docx"""
    def __init__(self, para_dict: dict):
        self.file_name = ''  # now the para_dict just needs 'file_name'
        self.should_create_new = True  # used to justify whether we should create a new docx fileS
        self.TO_HANDLE_TABLE_OBJS_ = []  # stores all Table objects in the docx

        for key in para_dict.keys():
            setattr(self, key, para_dict[key])
        pass

        if self.should_create_new is True:
            self.document = Document()  # generate a new document_object
        elif self.should_create_new is False:
            self.document = Document(self.file_name)  # generate
        assert isinstance(self.document, document_real.Document)

        pass

    def extract_dict_from_docx(self):
        """extract a dictionary of section_obj from the original_docx_file"""
        # now we have a Document obj, which is read from the original_docx_file
        document = self.document
        assert isinstance(document, document_real.Document)
        elements_in_one_section = []  # it stores paragraphs, tables...
        for para in document.paragraphs:
            if para.text != section_end_flag:
                elements_in_one_section.append(para)
            elif para.text == section_end_flag:
                # todo need to modify afterwards
                break
                pass
            if para.text.startswith('表'):
                # handle tables
                table_obj = self.__get_one_table()
                elements_in_one_section.append(table_obj)
                pass
            para_text = para.text
            para_style = para.style
            pass
        # now we get all the elements in one section, return it
        return elements_in_one_section
        pass

    def write_into_target_docx(self, all_elements):
        """write all handled sections into target_docx_file"""
        document = self.document
        assert isinstance(document, document_real.Document)
        for element in all_elements:
            if isinstance(element, Paragraph):
                para = document.add_paragraph(element.text, element.style)
                para.style = element.style
                # if para.text.startswith('表') or para.text.startswith('图'):
                #     para.style = '图-表题注'
                pass
            elif isinstance(element, Table):
                rows = element.rows
                columns = element.columns
                table = document.add_table(len(rows), len(columns))
                for each_row in range(len(rows)):
                    for each_column in range(len(columns)):
                        table.cell(each_row, each_column).add_paragraph(element.cell(each_row, each_column).text)
                        pass
                    pass
                table.style
                # document.tables.append(element)
                pass
            pass
        document.save(self.file_name)
        pass

    def __get_one_table(self):
        """get one table each time"""
        all_tables = self.TO_HANDLE_TABLE_OBJS_
        the_result_table = None
        document = self.document
        assert isinstance(document, document_real.Document)
        if not self.TO_HANDLE_TABLE_OBJS_:
            # read all Table objs into self.TO_HANDLE_TABLE_OBJS_
            for table in document.tables:
                self.TO_HANDLE_TABLE_OBJS_.append(table)
            pass
        # pop one
        the_result_table = self.TO_HANDLE_TABLE_OBJS_.pop()
        pass
        return the_result_table
        pass

    pass


if __name__ == '__main__':
    the_para_dict_origin = {
        'file_name': original_docx_file,
        'should_create_new': False
    }
    docx_helper = DocxHelper(the_para_dict_origin)
    ele_in_one_section = docx_helper.extract_dict_from_docx()  # all_elements

    the_para_dict_target = {
        'file_name': target_docx_file,
        'should_create_new': False
    }
    docx_helper_target = DocxHelper(the_para_dict_target)
    docx_helper_target.write_into_target_docx(ele_in_one_section)

    print('Work done!!')

    pass

