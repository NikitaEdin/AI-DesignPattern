import os
import pandas as pd
import openpyxl
import catalogue
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

    def save_result(self, result: AnalysisResult, llm_interface: LLMInterface) -> str:
        """Save single AnalysisReport record"""
        return self.save_results([result], llm_interface)

    def save_results(self, results: List[AnalysisResult], llm_interface: LLMInterface) -> str:
        """Save a list of AnalysisReport to Excel file"""
        if not results:
            print('No results to  save')
            return ""
        
        # Prepare info
        llm_name = catalogue.LLM_SHORT_MAP.get(llm_interface.get_prefix())

        # Abort is failed to get llm name by prefix
        if llm_name is None:
            return ""
        

        filename = f'report_{llm_name}.xlsx'
        filepath = os.path.join(self.base_report_dir, filename)

        # Convert results to DataFrame
        dataframe = self._results_to_dataframe(results, llm_name)

        # Save to Excel
        saved_path = self._save_to_excel(dataframe, filepath)

        return str(saved_path)
    
    def _results_to_dataframe(self, results: List[AnalysisResult], analysing_llm:str = 'None') -> pd.DataFrame:
        """Convert analysis results to pandas DataFrame"""

        data = []
        for result in results:
            # Determine success flag if pattern match
            success = False
            if result.expected_pattern and result.identified_pattern:
                success = result.expected_pattern.lower() == result.identified_pattern.lower()

            snippet_filename = os.path.basename(result.snippet_path)
            analysed_file_data = catalogue.parse_filename(snippet_filename)
            analysed_llm = catalogue.LLM_SHORT_MAP.get(analysed_file_data.get('llm'))
            
            row = {
                'Date': result.analysis_started_at.strftime('%H:%M:%S %d-%m-%Y'),
                'Analysing_LLM': analysing_llm.lower(),
                'Generated_LLM': analysed_llm.lower(),
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

    # Custom input report handling
    def save_custom_results(self, results: list[AnalysisResult]):
        """Save analysis results for custom input to /Output/<filename>_result.txt"""
        
        if not results:
            print("No results to save")
            return []
        
        # Create output folder (if needed)
        os.makedirs('Output', exist_ok=True)
        
        saved_paths = []
        
        for idx, result in enumerate(results, 1):
            # Extract filename (no extension)
            input_filename = os.path.splitext(os.path.basename(result.snippet_path))[0]
            
            output_filename = f'{input_filename}_result.txt'
            output_path = os.path.join('Output', output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"File: {result.snippet_path}\n")
                f.write(f"Workflow: {result.workflow_type}\n")
                f.write(f"Analysis Time: {result.analysis_time:.2f}s\n")
                f.write(f"Analysis Started: {result.analysis_started_at.strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
                
                f.write(f"Identified Pattern: {result.identified_pattern}\n")
                f.write(f"Confidence: {result.confidence:.2%}\n\n")
                
                f.write("Explanation:\n")
                f.write(f"{result.explanation}\n\n")
                
                f.write(f"Evaluation Pass: {'YES' if result.evaluation_pass else 'NO'}\n\n")
                
                f.write("Evaluation Feedback:\n")
                f.write(f"{result.evaluation_feedback}\n\n")
            
            saved_paths.append(output_path)
            print(f"Result {idx}/{len(results)} saved to: {output_path}")
        
        return saved_paths


