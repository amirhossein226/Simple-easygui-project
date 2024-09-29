import easygui as gui
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path


def get_dest_file(source_file):
    while True:
        dest_file = gui.filesavebox(
            msg="Choose a route and name for saving file!",
            default="*.pdf"
        )

        if dest_file == None:
            exit()
        elif Path(dest_file).suffix != '.pdf' or dest_file == source_file:
            gui.msgbox(
                msg=f"You are see this prompt because one of the below reasons:\n1- your destination route is exactly the same as the source route\n2- The file suffix is not .pdf"
            )
            continue
        return dest_file


def get_positive_int(start=None, reader=None):
    """
    This function will used to get the start and end point.

    By passing the start parameter to this function, actually 
    we are telling that we already have teh start pint and need 
    to get endpoint. 
    """
    message = 'Enter a positive integer for ' + \
        ('starting' if not start else 'ending') + ' pint'

    while True:
        # display the enter box to get the input from user
        page_number = gui.enterbox(
            msg=message
        )

        # if pressed 'Cancel' ,stop executing the program
        if page_number == None:
            exit()
        # if user enter none-digit input or digit entered by user not in the range of pdf pages' len show it the message and ask it for another input
        elif not page_number.isdigit() or int(page_number) not in range(0, len(reader.pages)):
            gui.msgbox(
                msg=f"""
                your entry must have the below characteristics:
                1- positive integer
                2- range between 0 to {len(reader.pages) - 1}"""
            )
            continue
        # When getting endpoint , we must check to ensure the number of endpoint is bigger than start point
        if start and int(page_number) < int(start):
            gui.msgbox(
                f"""
                The endpoint must be bigger than start point:{page_number} !> {start}
                """
            )
            continue

        break
    return int(page_number)


while True:
    source_file = gui.fileopenbox(
        msg="Choose your PDF file",
        default="*.pdf"
    )
    # if the "Cancel" button clicked, then not continue remain lines of code and exit
    if source_file == None:
        exit()
    # if the selected file is not the pdf file then display a message and try to ask it for the file again
    elif Path(source_file).suffix == ".pdf":
        break
    gui.msgbox(
        msg="you must choose a PDF file"
    )

reader = PdfReader(source_file)

# define the start and end page of pdf
start = get_positive_int(reader=reader)
end = get_positive_int(start=start, reader=reader)


destination_file = get_dest_file(source_file)

writer = PdfWriter()
for page in reader.pages[start:end]:
    writer.add_page(page)

with Path(destination_file).open("wb") as file:
    writer.write(file)
