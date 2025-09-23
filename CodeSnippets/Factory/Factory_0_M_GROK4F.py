from abc import ABC, abstractmethod

class Report(ABC):
    @abstractmethod
    def generate(self):
        pass

class PDFReport(Report):
    def generate(self):
        return "PDF report content generated"

class HTMLReport(Report):
    def generate(self):
        return "HTML report content generated"

class ReportCreator(ABC):
    @abstractmethod
    def create_report(self) -> Report:
        pass

    def process_report(self):
        report = self.create_report()
        return report.generate()

class PDFReportCreator(ReportCreator):
    def create_report(self) -> Report:
        return PDFReport()

class HTMLReportCreator(ReportCreator):
    def create_report(self) -> Report:
        return HTMLReport()

if __name__ == "__main__":
    try:
        pdf_creator = PDFReportCreator()
        print(pdf_creator.process_report())

        html_creator = HTMLReportCreator()
        print(html_creator.process_report())
    except Exception as e:
        print(f"Error processing report: {e}")