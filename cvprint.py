
import gdb
import sys
import struct



class PlotterCommand(gdb.Command):
    
    def __init__(self):
        super(PlotterCommand, self).__init__("m",
                                             gdb.COMMAND_DATA,
                                             gdb.COMPLETE_SYMBOL)
    def invoke(self, arg, from_tty):
        mat_type = "d"
        args = gdb.string_to_argv(arg)

        # generally, we type "plot someimage" in the GDB commandline
        # where "someimage" is an instance of cv::Mat
        v = gdb.parse_and_eval(args[0])
        
        # the value v is a gdb.Value object of C++
        # code's cv::Mat, we need to translate to
        # a python object under cv2.cv
        #image_size =  (v['cols'],v['rows'])
        print("cols: ", v['cols'])
        print("rows: ", v['rows'])
        #print(v['data'])
        
        # conver the v['data'] type to "char*" type
        char_type = gdb.lookup_type("char")
        char_pointer_type =char_type.pointer()
        buffer = v['data'].cast(char_pointer_type)

        # read bytes from inferior's memory, because
        # we run the opencv-python module in GDB's own process
        # otherwise, we use memory corss processes        
        #buf = v['step']['buf']
        #bytes = buf[0] * v['rows'] # buf[0] is the step? Not quite sure.
        if mat_type =="d":
            bytes = v['rows'] * v['cols'] * 8
        elif mat_type =="f":
            bytes = v['rows'] * v['cols'] * 4

        inferior = gdb.selected_inferior()
        mem = inferior.read_memory(buffer, bytes)

        
        rows = range(0, int(v['rows']))

        print("values: ")

        for j in [x*int(v['cols']) for x in rows]:
            if mat_type == "d":
        	    print([struct.unpack('<d',mem.tobytes()[8*i:8*i+8]) for i in range(j ,j+ int(v['cols']))])
            elif mat_type == "f":
                print([struct.unpack('<f',mem.tobytes()[4*i:4*i+4]) for i in range(j ,j+ int(v['cols']))])
        #print(np.frombuffer(mem, dtype=np.uint8))

        #print(mem)
	

        # set the img's raw data
        #cv.SetData(img, mem)

        # create a window, and show the image
        #cv.StartWindowThread()
        #cv.NamedWindow('viewer')
        #cv.ShowImage('viewer', img)

        # the below statement is necessory, otherwise, the Window
        # will hang
        #cv.WaitKey(0)
        #cv.DestroyWindow('viewer')

        # save matrix as an xml file and open it with matrix viewer
        # cv.Save("/tmp/dump.xml", img, "matrix")
        # call(["matrix-viewer", "/tmp/dump.xml"])
        # cv.SaveImage("/tmp/viewer.png", img)
        # call(["matrix-viewer", "/tmp/viewer.png"])
        
PlotterCommand()
