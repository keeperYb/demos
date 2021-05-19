import traceback

import win32com.client
from win32com.client import constants

class Win32DocHandler:
    """能够声场一个pywin32的doc对象"""
    def __init__(self, file_path):
        self.file_path = file_path
        self.application_obj = None
        self.doc_obj = None
        self.__init_obj()
        pass

    def __init_obj(self):
        """
        得到 Application, Document的对象
        :return:
        """
        word = None
        try:
            # word = win32com.client.Dispatch("kwps.Application")
            word = win32com.client.gencache.EnsureDispatch("kwps.Application")
        except Exception as e:
            traceback.print_exc()
            try:
                word = win32com.client.gencache.EnsureDispatch("wps.Application")
            except Exception as e:
                traceback.print_exc()
                try:
                    word = win32com.client.gencache.EnsureDispatch("word.Application")
                except Exception as e:
                    traceback.print_exc()
        if word is not None:
            word.Visible = 1  # 0为不可见, 1为可见
            self.application_obj = word
            self.doc_obj = word.Documents.Open(self.file_path)
        pass

    def add_outside_obj_before_holder(self, outside_file_path, place_holder):
        """docx 插入对象, 到指定place_hoder的上方"""
        # 找到特定的place_hoder, 上移光标, 插入对象
        selection = self.application_obj.Selection
        find = selection.Find
        find.Text = place_holder
        find.Wrap = 1
        find.Execute()

        selection.MoveUp()

        selection.InlineShapes.AddOLEObject(FileName=outside_file_path, DisplayAsIcon=False)
        pass

    def update_pageNumber(self):
        """更新目录 """
        wd_section = self.doc_obj.Sections(2)  # 注意section内部成员编号是从1开始的, 而实际需要从小节2开始加页码
        wd_section.Footers(constants.wdHeaderFooterPrimary).PageNumbers.Add(PageNumberAlignment=constants.wdAlignPageNumberCenter)  # 添加页码
        pass

    def close_all(self):
        """关闭, 退出"""
        self.doc_obj.Close(SaveChanges=True)
        self.application_obj.Quit()
        pass

    pass

def update_toc(docx_file):
    try:
        word = None
        try:
            # word = win32com.client.Dispatch("kwps.Application")
            word = win32com.client.gencache.EnsureDispatch("kwps.Application")
        except Exception as e:
            traceback.print_exc()
            try:
                word = win32com.client.gencache.EnsureDispatch("wps.Application")
            except Exception as e:
                traceback.print_exc()
                try:
                    word = win32com.client.gencache.EnsureDispatch("word.Application")
                except Exception as e:
                    traceback.print_exc()
        if word is not None:
            word.Visible = 0
            # script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe)))
            # print(script_dir)
            doc = word.Documents.Open(docx_file)

            # print(doc.Shapes.Count)




            # # wd_section = doc.Sections(1)#注意section内部成员编号是从1开始的
            # # print(wd_section)
            # # wd_section.Footers(constants.wdHeaderFooterPrimary).PageNumbers.Add(PageNumberAlignment=constants.wdAlignPageNumberCenter)#添加页码
            #
            # # doc.Sections(1).Footers(1).Range.Text = "XXX"
            # # for section in  doc.Sections:
            # #     print(section)
            # # print(len(doc.Sections))
            # doc.Sections(1).Footers(1).PageNumbers.Add(1,True)
            # # doc.Sections(1).Headers(1).PageNumbers.Add(1,True)
            # doc.Sections(1).Footers(1).PageNumbers.NumberStyle = 0
            # doc.Sections(1).Footers(1).Range.ParagraphFormat.Alignment = 1  #    win32com.client.constants.wdAlignParagraphCenter
            #
            # # # win32com.client.constants.wdHeaderFooterPrimary
            # # activefooter = doc.Sections(1).Footers(1).Range
            # # activefooter.ParagraphFormat.Alignment = 1
            # # activefooter.Collapse(0)
            # # activefooter.Fields.Add(activefooter, win32com.client.constants.wdFieldPage)
            # # activefooter = doc.Sections(1).Footers(1).Range
            # # activefooter.Collapse(0)
            # # activefooter.InsertAfter(Text = ' of ')
            # # activefooter.Collapse(0)
            # # activefooter.Fields.Add(activefooter,win32com.client.constants.wdFieldNumPages)

            doc.TablesOfContents(1).Update()
            doc.Close(SaveChanges=True)
            word.Quit()
    except Exception as e:
        traceback.print_exc()
    finally:
        pass
