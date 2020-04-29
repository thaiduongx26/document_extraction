def remove_password(pdf_file: str):
    import pikepdf

    pdf = pikepdf.open(pdf_file)
    pdf.save(pdf_file)
