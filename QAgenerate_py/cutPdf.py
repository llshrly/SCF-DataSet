import os
from PyPDF2 import PdfFileWriter, PdfFileReader

def split_pdf(filename, filepath, save_dirpath, step=10):
    """
    拆分PDF为多个小的PDF文件，
    filename:文件名
    filepath:文件路径
    save_dirpath:保存小的PDF的文件路径
    step: 每step间隔的页面生成一个文件
    """
    if not os.path.exists(save_dirpath):
        os.mkdir(save_dirpath)
    pdf_reader = PdfFileReader(filepath)
    # 读取每一页的数据
    pages = pdf_reader.getNumPages()
    for page in range(0, pages, step):
        pdf_writer = PdfFileWriter()
        # 拆分pdf，每 step 页的拆分为一个文件
        for index in range(page, page+step):
            if index < pages:
                pdf_writer.addPage(pdf_reader.getPage(index))
        # 保存拆分后的小文件
        save_path = os.path.join(save_dirpath, filename+str(int(page/step)+1)+'.pdf')
        print(save_path)
        with open(save_path, "wb") as out:
            pdf_writer.write(out)

    print("文件已成功拆分，保存路径为："+save_dirpath)
    
filename = '.pdf'
filepath = os.path.join(os.getcwd(), filename)
save_dirpath = os.path.join(os.getcwd(), '')
split_pdf(filename, filepath, save_dirpath, step=10)
