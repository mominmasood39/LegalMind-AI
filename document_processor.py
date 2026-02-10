import os
import re
import json
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from backend.config import settings
import time

class DocumentProcessor:
    def __init__(self):
        print("Initializing Document Processor...")
        
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ Embedding model loaded")
        
        print("Connecting to Pinecone...")
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        
        index_name = settings.PINECONE_INDEX_NAME
        
        if index_name not in pc.list_indexes().names():
            print(f"Creating new Pinecone index: {index_name}")
            pc.create_index(
                name=index_name,
                dimension=384,  # MiniLM dimension
                metric='cosine',
                spec=ServerlessSpec(
                    cloud="aws",
                    region=settings.PINECONE_REGION
                )
            )
            time.sleep(10)
        
        self.index = pc.Index(index_name)
        print(f"✓ Connected to Pinecone index: {index_name}")
    
    def clean_text(self, text):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'Page\s+\d+', '', text)
        text = re.sub(r'\d+\s+of\s+\d+', '', text)
        text = re.sub(r'[^\w\s\.\,\;\:\-\(\)\[\]]', '', text)
        return text.strip()
    
    def extract_from_pdf(self, pdf_path):
        print(f"Processing: {os.path.basename(pdf_path)}")
        reader = PdfReader(pdf_path)
        text = ""
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            except Exception as e:
                print(f"  Warning: Error on page {page_num}: {e}")
        return self.clean_text(text)
    
    def chunk_text(self, text, chunk_size=400, overlap=50):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk.split()) > 20:
                chunks.append(chunk)
        return chunks
    
    def detect_document_type(self, filename):
        filename_lower = filename.lower()
        if 'arbitration' in filename_lower:
            return 'Arbitration Act 1940'
        elif 'code_of_civil' in filename_lower or 'civil_proce' in filename_lower:
            return 'Code of Civil Procedure 1908'
        elif 'contract_act' in filename_lower:
            return 'Contract Act 1872'
        elif 'crpc' in filename_lower:
            return 'Criminal Procedure Code 1898'
        elif 'customs' in filename_lower:
            return 'Customs Act 1969'
        elif 'dissolution' in filename_lower:
            return 'Dissolution of Muslim Marriages Act 1939'
        elif 'factories' in filename_lower:
            return 'Factories Act 1934'
        elif 'guardians' in filename_lower or 'wards' in filename_lower:
            return 'Guardians and Wards Act 1890'
        elif 'income_tax' in filename_lower:
            return 'Income Tax Ordinance 2001'
        elif 'industrial_relations' in filename_lower:
            return 'Industrial Relations Act 2012'
        elif 'limitation' in filename_lower:
            return 'Limitation Act 1908'
        elif 'muslim_family' in filename_lower:
            return 'Muslim Family Laws Ordinance 1961'
        elif 'national_accountabil' in filename_lower:
            return 'National Accountability Ordinance 1999'
        elif 'negotiable' in filename_lower:
            return 'Negotiable Instruments Act 1881'
        elif 'citizenship' in filename_lower:
            return 'Pakistan Citizenship Act 1951'
        elif 'constitution' in filename_lower:
            return 'Constitution of Pakistan 1973'
        elif 'penal_code' in filename_lower or 'ppc' in filename_lower or 'pakistan_penal' in filename_lower:
            return 'Pakistan Penal Code 1860'
        elif 'partnership' in filename_lower:
            return 'Partnership Act 1932'
        elif 'payment_of_wages' in filename_lower:
            return 'Payment of Wages Act 1936'
        elif 'electronic_crimes' in filename_lower or 'peca' in filename_lower or 'prevention_of_electr' in filename_lower:
            return 'Prevention of Electronic Crimes Act 2016'
        elif 'qanun' in filename_lower or 'shahadat' in filename_lower:
            return 'Qanun-e-Shahadat Order 1984'
        elif 'registration' in filename_lower:
            return 'Registration Act 1908'
        elif 'sale_of_goods' in filename_lower:
            return 'Sale of Goods Act 1930'
        elif 'sales_tax' in filename_lower:
            return 'Sales Tax Act 1990'
        elif 'specific_relief' in filename_lower:
            return 'Specific Relief Act 1877'
        elif 'transfer_of_property' in filename_lower:
            return 'Transfer of Property Act 1882'
        elif 'anti-terrorism' in filename_lower or 'ata' in filename_lower:
            return 'Anti-Terrorism Act 1997'
        elif 'companies_act' in filename_lower or 'company' in filename_lower:
            return 'Companies Act 2017'
        elif 'protection_of_women' in filename_lower:
            return 'Protection of Women Act 2006'
        elif 'child_marriage' in filename_lower:
            return 'Child Marriage Restraint Act 1929'
        elif 'workmen' in filename_lower or 'compensation' in filename_lower:
            return 'Workmen Compensation Act 1923'
        elif 'copyright' in filename_lower:
            return 'Copyright Ordinance 1962'
        elif 'banking' in filename_lower:
            return 'Banking Companies Ordinance 1962'
        elif 'land_acquisition' in filename_lower:
            return 'Land Acquisition Act 1894'
        else:
            clean_name = filename.replace('.pdf', '').replace('_', ' ')
            clean_name = ' '.join(word.capitalize() for word in clean_name.split())
            return clean_name
    
    def extract_section_number(self, text):
        patterns = [
            r'Section\s+(\d+[A-Z]?)',
            r'Article\s+(\d+[A-Z]?)',
            r'Part\s+([IVX]+)',
            r'Chapter\s+(\d+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return "General"
    
    def process_all_documents(self, docs_folder='documents'):
        if not os.path.exists(docs_folder):
            print(f"Error: '{docs_folder}' folder not found!")
            return False
        
        pdf_files = [f for f in os.listdir(docs_folder) if f.endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in '{docs_folder}' folder!")
            return False
        
        print(f"\n{'='*60}")
        print(f"Found {len(pdf_files)} PDF files to process")
        print(f"{'='*60}\n")
        
        total_chunks = 0
        vectors_to_upsert = []
        
        for idx, pdf_file in enumerate(pdf_files):
            pdf_path = os.path.join(docs_folder, pdf_file)
            doc_type = self.detect_document_type(pdf_file)
            
            print(f"[{idx+1}/{len(pdf_files)}] {pdf_file}")
            print(f"  Document type: {doc_type}")
            
            full_text = self.extract_from_pdf(pdf_path)
            if not full_text:
                print(f"  ⚠ No text extracted, skipping...")
                continue
            
            chunks = self.chunk_text(full_text)
            print(f"  Created {len(chunks)} chunks")
            
            print(f"  Creating embeddings...")
            for chunk_idx, chunk in enumerate(chunks):
                embedding = self.embedding_model.encode(chunk).tolist()
                section = self.extract_section_number(chunk)
                vector_id = f"{pdf_file}_{chunk_idx}"
                
                metadata = {
                    'text': chunk[:1000],
                    'document': doc_type,
                    'filename': pdf_file,
                    'section': section,
                    'chunk_id': chunk_idx
                }
                
                vectors_to_upsert.append({
                    'id': vector_id,
                    'values': embedding,
                    'metadata': metadata
                })
                
                total_chunks += 1
                
                if len(vectors_to_upsert) >= 100:
                    self.index.upsert(vectors=vectors_to_upsert)
                    print(f"    Uploaded {total_chunks} chunks so far...")
                    vectors_to_upsert = []
        
        if vectors_to_upsert:
            self.index.upsert(vectors=vectors_to_upsert)
        
        print(f"\n{'='*60}")
        print(f"✓ Processing Complete!")
        print(f"  Total documents: {len(pdf_files)}")
        print(f"  Total chunks indexed: {total_chunks}")
        print(f"{'='*60}\n")
        
        summary = {
            'total_documents': len(pdf_files),
            'total_chunks': total_chunks,
            'documents_processed': [
                {'filename': f, 'type': self.detect_document_type(f)} 
                for f in pdf_files
            ]
        }
        
        with open('processing_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("Summary saved to 'processing_summary.json'\n")
        return True

def main():
    print("\n" + "="*60)
    print("LEGAL DOCUMENT PROCESSOR")
    print("="*60 + "\n")
    
    processor = DocumentProcessor()
    success = processor.process_all_documents()
    
    if success:
        print("✓ All documents successfully processed and indexed!")
    else:
        print("✗ Processing failed. Check error messages above.")

if __name__ == "__main__":
    main()