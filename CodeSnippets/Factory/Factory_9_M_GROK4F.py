import abc

class Document(abc.ABC):
    @abc.abstractmethod
    def generate(self):
        pass

class ReportDocument(Document):
    def generate(self):
        return "Generated report content"

class InvoiceDocument(Document):
    def generate(self):
        return "Generated invoice content"

class DocumentCreator:
    def create_document(self, doc_type):
        if doc_type == "report":
            return ReportDocument()
        elif doc_type == "invoice":
            return InvoiceDocument()
        else:
            raise ValueError(f"Unknown document type: {doc_type}")

if __name__ == "__main__":
    creator = DocumentCreator()
    try:
        report = creator.create_document("report")
        print(report.generate())
        
        invoice = creator.create_document("invoice")
        print(invoice.generate())
        
        invalid = creator.create_document("contract")
    except ValueError as e:
        print(f"Error: {e}")