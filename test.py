import cv2
import numpy as np
import PIL
from PIL import Image
print('Pillow Version:', PIL.__version__)


def generate_debug_image_with_relation(list_pages):
    print("list_pages: ", list_pages[0])
    page0 = cv2.imread(list_pages[0])
    print("page0: ", page0)


    page0 = np.asarray()
    page1 = np.asarray(cv2.imread(list_pages[1]))
    print("page1: ", page1)
    page = np.concatenate([page0, page1])
    cv2.imwrite("debug.jpg", page)


folder = "E:\\document_dataset\\kepco_debug_image\\中国0010"
list_page = ["1.PNG", "2"]#, "01 入札説明書.pdf-page-2.png"]
list_page = [folder + '/' + x for x in list_page]
generate_debug_image_with_relation(list_page)
