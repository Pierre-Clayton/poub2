from .config import BaseConfig
import csv
import PyPDF2
from pathlib import Path
import sqlalchemy as db
from sqlalchemy import text
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker



class UtilFunctions(object):

    def psqlcon(self):
        dhost = BaseConfig.DHOST
        dport = BaseConfig.DPORT
        dbase = BaseConfig.DBASE
        duser = BaseConfig.DUSER
        dpass = BaseConfig.DPASS
        con = db.create_engine(f'postgresql://{duser}:{dpass}@{dhost}:{dport}/{dbase}',
                                pool_recycle=3600, pool_size=10)
        return con

    def db_session(self):
        engine = self.psqlcon()
        db_sess = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=engine))
        return db_sess
    
    def save_to_db(self,cls,data):
        sess = self.db_session()
        new_object = cls(**data)
        sess.add(new_object)
        sess.commit()
        return new_object

    def update_db(self,session):
        session.commit()

    def chunk_text(self,text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
        """
        Splits the text into overlapping chunks for better retrieval/LLM usage.
        
        :param text: The full string to chunk
        :param chunk_size: The maximum number of characters per chunk
        :param chunk_overlap: The number of characters to overlap between chunks
        :return: List of text chunks
        """
        # Replace newlines with spaces (optional)
        text = text.replace('\n', ' ')
        
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + chunk_size, text_length)
            chunk = text[start:end]
            chunks.append(chunk.strip())
            start += chunk_size - chunk_overlap  # move start by chunk_size minus overlap
        
        return chunks

    def parse_pdf(self,file_path: str, chunk_size=500, chunk_overlap=50) -> list[str]:
        """
        Reads a PDF file, returns a list of text chunks.
        """
        pdf_path = Path(file_path)
        if not pdf_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        text_content = []
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
        
        full_text = "\n".join(text_content)
        # Now chunk the text
        chunks = self.chunk_text(full_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return chunks

    def parse_csv(self,file_path: str, chunk_size=500, chunk_overlap=50) -> list[str]:
        """
        Reads a CSV file and returns list of text chunks (concatenated rows).
        """
        csv_path = Path(file_path)
        if not csv_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        rows_text = []
        with open(csv_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                # Join row fields with a space or comma
                row_str = " ".join(row)
                rows_text.append(row_str)
        
        # Combine all rows into one big string
        full_text = "\n".join(rows_text)
        # Chunk it
        chunks = self.chunk_text(full_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return chunks

