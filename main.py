import tkinter
import tkinter.ttk
import tkinter.filedialog
import re


class MyApp(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title("STM32WB UUID Extractor")
        self.frame = tkinter.ttk.Frame(self, padding=10)
        self.frame.grid()

        self.label1 = tkinter.ttk.Label(self.frame, text="Select a file to extract UUIDs. For example \"custom_stm.c\"")
        self.btn_select_file = tkinter.ttk.Button(self.frame, text="Select file", command=self.select_file)
        self.text_area = tkinter.Text(self, width=20, height=10)

        self.label1.grid(row=0, column=0)
        self.btn_select_file.grid(row=1, column=0, sticky=tkinter.W)
        self.text_area.grid(row=2, column=0, columnspan = 2, sticky = tkinter.W+tkinter.E)

    def select_file(self):
        filename = tkinter.filedialog.askopenfilename()
        text_result = ''

        if not filename:
            print("No file")
        else:
            file = open(filename, 'r')
            lines = file.readlines()

            uuids_section_mode = 0
            uuid_found = 0
            for line in lines:
                if line.find("Hardware Characteristics Service") > -1:
                    #print("UUIDs section has been found")
                    uuids_section_mode = 1

                if uuids_section_mode and line.startswith("#define"):
                    #print("UUID record has been found")
                    uuid_found = 1

                    result = re.search("#define\s+COPY_(\w+)\(", line)
                    UUID_name = result.group(1)

                    text_result += UUID_name + '\r\n'

                    try:
                        result = re.findall("0x([0-9a-fA-F]{2})", line)
                        UV = result
                        uuid_text = ''
                        pattern = [4, 2, 2, 2, 6]
                        j = 0

                        for i,c in enumerate(pattern):
                            for k in range(c):
                                uuid_text += UV[j+k]

                            j += c

                            if i != len(pattern)-1:
                                uuid_text += '-'

                        text_result += uuid_text + '\r\n'
                    except Exception:
                        text_result += "An error occurred while decoding UUID" + '\r\n'



                if uuid_found and len(line.strip()) == 0:
                    #print("End of UUIDs section has been found")
                    uuids_section_mode = 0
                    uuid_found = 0

        self.text_area.insert(tkinter.INSERT, text_result)


root = MyApp()
root.mainloop()
