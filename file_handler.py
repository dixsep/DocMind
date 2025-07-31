import hashlib
from pathlib import Path
import os
from datetime import datetime, timedelta
import pickle
from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter

MAX_TOTAL_SIZE: int = 200 * 1024 * 1024

class DocumentProcessor:

    def __init__(self):
        self.headers = [("#", "Header 1"), ("##", "Header 2")]
        self.cache_dir = Path("document_cache")
        self.cache_dir.mkdir(parents = True, exist_ok = True)

    #check total_file size
    def validate_files(self, files):

        total_size = sum(os.path.getsize(file_path) for file_path in files)

        if total_size >= MAX_TOTAL_SIZE:
            raise ValueError(f"Total size exceeds {MAX_TOTAL_SIZE//1024//1024}MB limit")

    # get hash 
    def generate_hash(self, content : bytes):
        return hashlib.sha256(content).hexdigest()

    def is_cache_valid(self, cache_path : Path):
        if not cache_path.exists():
            return False

        cache_age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
        return cache_age < timedelta(days=7)

    def load_from_cache(self, cache_path):

        with open(cache_path, "rb") as f:
            data = pickle.load(f)

        return data["chunks"]

    def save_to_cache(self, chunks, cache_path):

        with open(cache_path, "wb") as f:
            pickle.dump({
                "timestamp" : datetime.now().timestamp(),
                "chunks" : chunks
            }, f)

    #get chunks from file
    def process_file(self, file_path):

        #file_path does not have ends with

        converter = DocumentConverter()
        markdown = converter.convert(file_path).document.export_to_markdown()
        splitter = MarkdownHeaderTextSplitter(self.headers)
        chunks = splitter.split_text(markdown)

        print(f"chunks : {chunks}")

        return chunks

     # process all files
    def process(self, files):

        #files : list of file_paths
        self.validate_files(files)
        all_chunks = []
        seen_hashes = set()

        for file in files:
            try:
                with open(file, "rb") as f:
                    file_hash = self.generate_hash(f.read())
                    print("hash : ", file_hash)

                cache_path = self.cache_dir / f"{file_hash}.pkl"

                # if self.is_cache_valid(cache_path):
                #     print(f"loading cache from {file}")
                #     chunks = self.load_from_cache(cache_path)
                # else:
                #     chunks = self.process_file(file)
                #     print("chunks : ",chunks)
                #     self.save_to_cache(chunks, cache_path)

                chunks = self.process_file(file)

                #remove duplicate chunks

                # for chunk in chunks:
                #     chunk_hash = self.generate_hash(chunk.page_content.encode())
                #     if chunk_hash not in seen_hashes:
                #         all_chunks.append(chunk)
                #         seen_hashes.add(chunk_hash)

                for chunk in chunks:
                    all_chunks.append(chunk)

            except Exception as e:
                print(f"Failed to process file : {file} : {str(e)}")


        return all_chunks
