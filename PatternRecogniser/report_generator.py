import add_shared
import os
import pandas as pd
import openpyxl
import catalogue
from datetime import datetime
from typing import List
from openpyxl.utils.dataframe import dataframe_to_rows
from shared.llm_interface import LLMInterface
from workflow_interface import AnalysisResult


class ReportGenerator:
    """Handles generation and management of Excel analysis report"""

    def __init__(self, base_report_dir: str = "./Reports"):
        self.base_report_dir = base_report_dir
        os.makedirs(self.base_report_dir, exist_ok=True)

        # Column for Excel sheet
        self.columns = [
            'Date',
            'Analysing_LLM',
            'Generated_LLM',
            'Snippet_name',
            'Identified pattern',
            'Confidence',
            'Success',
            'Analysis_time',
            'Workflow_type',
            'Pattern_difficulty'
        ]

    def save_results(self, results: List[AnalysisResult], llm_interface: LLMInterface) -> str:
        if not results:
            print('No results to  save')
            return ""
        
        # Prepare info
        llm_name = catalogue.LLM_SHORT_MAP.get(llm_interface.get_prefix())
        filename = f'report_{llm_name}.xlsx'
        filepath = os.path.join(self.base_report_dir, filename)

        # Conver results to DataFrame
        dataframe = self._results_to_dataframe(results, llm_name)

        # Save to Excel
        saved_path = self._save_to_excel(dataframe, filepath)

        return str(saved_path)
    
    def _results_to_dataframe(self, results: List[AnalysisResult], analysing_llm:str = 'None') -> pd.DataFrame:
        """Convert analysis results to pandas DataFrame"""

        data = []
        current_time = datetime.now()
        for result in results:
            # Determine success flag if pattern match
            success = False
            if result.expected_pattern and result.identified_pattern:
                success = result.expected_pattern.lower() == result.identified_pattern.lower()

            snippet_filename = os.path.basename(result.snippet_path)
            analysed_file_data = catalogue.parse_filename(snippet_filename)
            row = {
                'Date': current_time.strftime('%H:%M:%S %d-%m-%Y'),
                'Analysing_LLM': analysing_llm,
                'Generated_LLM': analysed_file_data.get('llm'),
                'Snippet_name': snippet_filename,
                'Identified pattern': result.identified_pattern,
                'Confidence': result.confidence,
                'Success': success,
                'Analysis_time': round(result.analysis_time, 3),
                'Workflow_type': result.workflow_type.name,
                'Pattern_difficulty': analysed_file_data.get('difficulty')
            }
            data.append(row)

        return pd.DataFrame(data, columns=self.columns)

    def _save_to_excel(self, dataframe: pd.DataFrame, filepath: str) -> str:
        """Save given Dataframe to Excel"""
        if os.path.exists(filepath):
            return self._append_existing_excel(dataframe, filepath)
        else:
            return self._create_excel(dataframe, filepath)

    def _create_excel(self, dataframe: pd.DataFrame, filepath: str) -> str:
        """Create new Excel file"""
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            dataframe.to_excel(writer, sheet_name='Analysis Results', index=False)

            # TODO: Excel formatting

        print(f'Created new Excel report: {filepath}')
        return filepath
    
    def _append_existing_excel(self, dataframe: pd.DataFrame, filepath: str) -> str:
        """Append Dataframe to existing Excel report"""
        try:
            workbook = openpyxl.load_workbook(str(filepath))
            worksheet = workbook['Analysis Results']

            for row in dataframe_to_rows(dataframe, index=False, header=False):
                worksheet.append(row)

            # Save
            workbook.save(str(filepath))
            workbook.close()

            print(f'Appended {len(dataframe)} rows to existing Excel report: {filepath}')
            return filepath
        except Exception as e:
            print(f'Error appending to Excel file: {e}')
            # TODO: create backup in case of failure

            return self._create_excel(dataframe, filepath)
