from tkinter import *
from tkinter.ttk import Notebook, Treeview
import unittest


class TestcaseSelector:

    def start(self):

        # Create the TK window
        self.root = Tk()
        window = self.root
        self.note = Notebook(self.root)

        window.wm_title("Select Testcases")
        window.minsize(width=250,height=250)

        # Create a scrollbar
        scrollbar = Scrollbar(window)
        scrollbar.pack(side=RIGHT,fill=Y)

        # Create a window frame for the treeview we're going to add
        testcase_frame = Frame(window)

        # Set view on the frame and allow multiple selections
        self.treeView = Treeview(testcase_frame,selectmode=EXTENDED)

        # testcase_frame.pack(fill=X)
        self.treeView.pack(fill=BOTH,expand=1)

        # Attach scrollbar to Tree
        self.treeView.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.treeView.yview)

        testSectionData = {}
        testData = {}

        # Add in all the available testcases as items in the tree grouped by their section
        testcases_dictionary = get_testcase_name_dictonary()

        for key in testcases_dictionary.keys():
            subsection = testcases_dictionary[key]
            testSectionData[key] = testcases_dictionary[key]

            subsection_parent = self.treeView.insert('',END,text=key)

            for test in subsection:
                self.treeView.insert(subsection_parent,END,text=test._testMethodName)
                testData[test._testMethodName] = test

        # self.webData = webData
        self.webData = testData
        self.testSectionData = testSectionData
        self.frame = Frame(window)
        self.frame.pack(fill=X)

        # Create Buttons for Cancel and Run
        Button(testcase_frame, text="Cancel", fg="red", command=self.frame.quit, height=5, width=50).pack(side=RIGHT,fill=Y)
        Button(testcase_frame, text="Run Selected",fg="green", command=self._save_selection,height=5,width=50).pack(side=LEFT,fill=Y)

        self.note.add(testcase_frame)
        self.note.pack(fill=BOTH,expand=1)


    def _save_selection(self):
        selected_tests = self.treeView.selection()

        output=[]
        for selection in selected_tests:
            item_text = self.treeView.item(selection,'text')
            if 'test_' in item_text:
                if item_text not in output:
                    output.append(item_text)
                else:
                    pass
            elif 'Tests' in item_text:
                for test in self.testSectionData[item_text]:
                    output.append(test._testMethodName)
                # output = output + self.testSectionData[item_text]

        self.frame.quit()
        self.testcases = self.get_tests_from_selected_names(output)

    def get_tests_from_selected_names(self,names):
        ret_tests = {}
        for name in names:
            ret_tests[name] = self.webData[name]

        return ret_tests

    def get_testcases(self):
        self.start()
        self.root.mainloop()
        self.root.destroy()

        return self.testcases



def test_name(parent):
    tns = []
    if hasattr(parent, '_testMethodName'):
        return parent
    elif hasattr(parent, '_tests'):
        for t in parent._tests:
            tn = test_name(t)
            if tn:
                tns.append(tn)
    return tns

def get_all_automated_tests():

    loader = unittest.TestLoader()
    tests = loader.discover('Tests', pattern='*Tests.py')

    tcs = [y for x in [y for x in test_name(tests) for y in x] for y in x]

    return tcs

def get_testcase_name_dictonary():

    all_tests = get_all_automated_tests()

    section_dict = {}

    for test in all_tests:
        testcase_name = test
        test_section = type(test).__name__

        if test_section in section_dict:
            section_dict[test_section].append(testcase_name)
        else:
            section_dict[test_section] = [testcase_name]

    return section_dict