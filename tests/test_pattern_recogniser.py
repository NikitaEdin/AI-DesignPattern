import contextlib
from io import StringIO
import sys
import os

# Repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../PatternRecogniser')))

import unittest
import argparse
from unittest.mock import MagicMock
from PatternRecogniser.pattern_recogniser import DPR
from PatternRecogniser.catalogue import WorkflowType

################################### Utils ###################################
def _mock_llm():
    m = MagicMock()
    m.get_prefix.return_value = "TEST"
    return m

def _mock_workflow(results=None):
    w = MagicMock()
    w.execute.return_value = results if results is not None else []
    return w

def _mock_llm_with_response(response: str):
    m = MagicMock()
    m.get_prefix.return_value = "TEST"
    m.generate_response.return_value = response
    return m

def _mock_file_manager(files=None):
    fm = MagicMock()
    fm.locate_snippets.return_value = files if files is not None else []
    fm.locate_custom_snippet.return_value = files if files is not None else []
    return fm

def _mock_result(filename="Singleton_0_E_C.py", identified="Singleton", expected="Singleton", confidence=1.0,
                 difficulty="E", analysis_time=5.0, evaluation_pass="PASS", evaluation_feedback="Correct identification.",
                 explanation="The class overrides __new__ to ensure a single instance.", error=None,
                 workflow_type=WorkflowType.SINGLE_PROMPT):
    r = MagicMock()
    r.snippet_path = f"../CodeSnippets/{identified}/{filename}"
    r.identified_pattern = identified
    r.expected_pattern = expected
    r.confidence = confidence
    r.difficulty= difficulty
    r.analysis_time = analysis_time
    r.evaluation_pass = evaluation_pass
    r.evaluation_feedback = evaluation_feedback
    r.explanation = explanation
    r.error = error
    r.workflow_type = workflow_type
    r.metadata = {}
    return r

def _mock_snippet(filename="Singleton_0_E_C.py",
                  content="class Singleton: pass",
                  design_pattern="Singleton",
                  difficulty="E",
                  llm_tag="C"):
    """fake CodeSnippet"""
    s = MagicMock()
    s.filename = filename
    s.filepath = f"../CodeSnippets/{design_pattern}/{filename}"
    s.content = content
    s.design_pattern = design_pattern
    s.difficulty = difficulty
    s.llm = llm_tag
    return s

def _make_args(**kwargs):
    default = dict(
        llm = 'claude',
        workflow = WorkflowType.SINGLE_PROMPT,
        input_path = None,
        filter_pattern = None,
        filter_difficulty = None,
        filter_llm = None,
        count = -1,
        dont_save = False
    )
    default.update(kwargs)
    return argparse.Namespace(**default)


################################### WORKFLOW TESTS ###################################
class TestWorkflowExecution(unittest.TestCase):
    """
    Tests full pipeline using a mock LLM and a mock workflow.
    The mock workflow mimics SingleWorkflow.execute()
    """

    def _make_dpr_with_results(self, results):
        """Mock DPR with workflow that returns given results"""
        llm = _mock_llm()
        llm_factory = MagicMock(return_value=llm)
        workflow = MagicMock()
        workflow.execute.return_value = results
        workflow_factory = MagicMock(return_value=workflow)
        report_gen = MagicMock()
        rg_factory = MagicMock(return_value=report_gen)
        dpr = DPR(file_manager=_mock_file_manager(files=[_mock_snippet()]), llm_factory=llm_factory,
                  workflow_factory=workflow_factory, report_generator_factory=rg_factory)
        return dpr, workflow, report_gen
 
    def test_results_saved_regardless_of_correctness(self):
        """Both correct and incorrect identifications"""
        correct = _mock_result(identified="Singleton", expected="Singleton", confidence=0.98)
        wrong = _mock_result(identified="Observer", expected="Singleton", confidence=0.55)
        dpr, _, report_gen = self._make_dpr_with_results([correct, wrong])
 
        dpr.run(_make_args())
 
        # call_args[0] = positional args tuple, [0] = results list
        saved = report_gen.save_results.call_args[0][0]
        # 2 results
        self.assertEqual(len(saved), 2) 
        # check correct answer matches
        self.assertEqual(saved[0].identified_pattern, "Singleton")
        # check wrong answers match
        self.assertEqual(saved[1].identified_pattern, "Observer")
        self.assertEqual(saved[1].expected_pattern, "Singleton")
 
    def test_confidence_preserved_across_range(self):
        """confidence values"""
        dpr_high, _, rg_high = self._make_dpr_with_results([_mock_result(confidence=1.0)])
        dpr_low, _, rg_low = self._make_dpr_with_results([_mock_result(confidence=0.45)])
 
        dpr_high.run(_make_args())
        dpr_low.run(_make_args())
 
        self.assertEqual(rg_high.save_results.call_args[0][0][0].confidence, 1.0)
        self.assertEqual(rg_low.save_results.call_args[0][0][0].confidence, 0.45)
 
    def test_successful_result_fields_preserved(self):
        """PASS evaluation"""
        dpr, _, report_gen = self._make_dpr_with_results([
            _mock_result(evaluation_pass="PASS", error=None)
        ])
        dpr.run(_make_args())
        # call_args[0] = positional args tuple, [0] = results list, [0] = first result
        saved = report_gen.save_results.call_args[0][0][0]
        self.assertEqual(saved.evaluation_pass, "PASS")
        self.assertIsNone(saved.error)
 
    def test_failed_result_fields_preserved(self):
        """FAIL evaluation"""
        dpr, _, report_gen = self._make_dpr_with_results([
            _mock_result(evaluation_pass="FAIL", error="LLM timeout")
        ])
        dpr.run(_make_args())
        saved = report_gen.save_results.call_args[0][0][0]
        self.assertEqual(saved.evaluation_pass, "FAIL")
        self.assertEqual(saved.error, "LLM timeout")

    def test_single_prompt_workflow_type_passed_to_factory(self):
        """workflow_factory should receive SINGLE_PROMPT and llm_interface"""
        llm = _mock_llm()
        workflow_factory = MagicMock(return_value=_mock_workflow(results=[_mock_result()]))
        dpr = DPR(file_manager=_mock_file_manager(files=[_mock_snippet()]),
                  llm_factory=MagicMock(return_value=llm), workflow_factory=workflow_factory,
                  report_generator_factory=MagicMock(return_value=MagicMock()))
 
        dpr.run(_make_args(workflow=WorkflowType.SINGLE_PROMPT))
 
        workflow_factory.assert_called_once_with(WorkflowType.SINGLE_PROMPT, llm)
 
    def test_invalid_workflow_types(self):
        """MULTI_LAYERED should sys.exit with raise ValueError"""
        dpr = DPR(file_manager=_mock_file_manager(files=[_mock_snippet()]),
                  llm_factory=MagicMock(return_value=_mock_llm()), workflow_factory=MagicMock(side_effect=NotImplementedError),
                  report_generator_factory=MagicMock(return_value=MagicMock()))
        with self.assertRaises(SystemExit):
            dpr.run(_make_args(workflow=WorkflowType.MULTI_LAYERED))
 
        with self.assertRaises(ValueError):
            DPR._default_workflow_factory("unknown_type", _mock_llm())
 
    def test_no_files_skips_workflow_and_save(self):
        """File_manager returns no files, workflow and report should never be called"""
        workflow_factory = MagicMock()
        report_gen = MagicMock()
        dpr = DPR(file_manager=_mock_file_manager(files=[]),
                  llm_factory=MagicMock(return_value=_mock_llm()),
                  workflow_factory=workflow_factory,
                  report_generator_factory=MagicMock(return_value=report_gen))
 
        dpr.run(_make_args())
 
        workflow_factory.assert_not_called()
        report_gen.save_results.assert_not_called()
 

################################### SAVING TESTS ###################################
class TestSavingBehaviour(unittest.TestCase):
 
    def _make_dpr(self, results=None):
        report_gen = MagicMock()
        rg_factory = MagicMock(return_value=report_gen)
        workflow = MagicMock()
        workflow.execute.return_value = results if results is not None else [_mock_result()]
        dpr = DPR(file_manager=_mock_file_manager(files=[_mock_snippet()]),
                  llm_factory=MagicMock(return_value=_mock_llm()), workflow_factory=MagicMock(return_value=workflow),
                  report_generator_factory=rg_factory)
        return dpr, report_gen
 
    def test_dont_save_prints_result_and_skips_report(self):
        """dont_save=True should print pattern/confidence/label and never touch ReportGenerator"""
        results = [
            _mock_result(identified="Singleton", expected="Singleton", confidence=0.85),
            _mock_result(identified="Observer", expected="Singleton", confidence=0.55),
        ]
        dpr, report_gen = self._make_dpr(results=results)
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            dpr.run(_make_args(dont_save=True))
        out = buf.getvalue()
 
        self.assertIn("Singleton", out)
        self.assertIn("85%", out)
        self.assertIn("[Success]", out)
        self.assertIn("[Failure]", out)
        report_gen.save_results.assert_not_called()
        report_gen.save_custom_results.assert_not_called()
 
    def test_save_routing_dataset_vs_custom_input(self):
        """Dataset mode calls save_results with llm; custom input calls save_custom_results"""
        llm = _mock_llm()
        # Dataset mode
        report_gen_ds = MagicMock()
        workflow = MagicMock()
        workflow.execute.return_value = [_mock_result()]
        dpr_ds = DPR(file_manager=_mock_file_manager(files=[_mock_snippet()]),
                     llm_factory=MagicMock(return_value=llm), workflow_factory=MagicMock(return_value=workflow),
                     report_generator_factory=MagicMock(return_value=report_gen_ds))
        dpr_ds.run(_make_args(dont_save=False, input_path=None))
        report_gen_ds.save_results.assert_called_once()
        self.assertEqual(report_gen_ds.save_results.call_args[0][1], llm)
        report_gen_ds.save_custom_results.assert_not_called()
 
        # Custom input mode
        report_gen_ci = MagicMock()
        workflow2 = MagicMock()
        workflow2.execute.return_value = [_mock_result()]
        dpr_ci = DPR(file_manager=_mock_file_manager(files=[_mock_snippet()]),
                     llm_factory=MagicMock(return_value=_mock_llm()), workflow_factory=MagicMock(return_value=workflow2),
                     report_generator_factory=MagicMock(return_value=report_gen_ci))
        dpr_ci.run(_make_args(dont_save=False, input_path="Input/my_code.py"))
        report_gen_ci.save_custom_results.assert_called_once()
        report_gen_ci.save_results.assert_not_called()
 
    def test_empty_results_skips_all_saving(self):
        """Empty results list should not trigger any save or print"""
        dpr, report_gen = self._make_dpr(results=[])
        dpr.run(_make_args(dont_save=False))
        report_gen.save_results.assert_not_called()
        report_gen.save_custom_results.assert_not_called()
 
################################### FILTERING TESTS ###################################
 
class TestFiltering(unittest.TestCase):
 
    def _make_dpr(self, fm):
        return DPR(file_manager=fm,
                   llm_factory=MagicMock(return_value=_mock_llm()), workflow_factory=MagicMock(return_value=_mock_workflow()),
                   report_generator_factory=MagicMock(return_value=MagicMock()))
 
    def test_individual_filters_forwarded(self):
        """Each filter arg should be passed through"""
        cases = [
            dict(filter_pattern="Singleton"), dict(filter_difficulty="H"),
            dict(filter_llm="openai"), dict(count=5),
        ]
        for overrides in cases:
            fm = _mock_file_manager(files=[])
            self._make_dpr(fm).run(_make_args(**overrides))
            expected = dict(design_pattern=None, difficulty=None, llm=None, count=-1)
            # Map kwarg name, locate_snippets param name
            key_map = {"filter_pattern": "design_pattern",
                       "filter_difficulty": "difficulty",
                       "filter_llm": "llm",
                       "count": "count"}
            for k, v in overrides.items():
                expected[key_map[k]] = v
            fm.locate_snippets.assert_called_once_with(**expected)
 
    def test_all_filters_combined(self):
        """All filters together should all be forwarded in a single call"""
        fm = _mock_file_manager(files=[])
        self._make_dpr(fm).run(_make_args(
            filter_pattern="Factory", filter_difficulty="M",
            filter_llm="openai", count=3))
        fm.locate_snippets.assert_called_once_with(
            design_pattern="Factory", difficulty="M", llm="openai", count=3)
 
    def test_no_filters_passes_all_none(self):
        """No filters"""
        fm = _mock_file_manager(files=[])
        self._make_dpr(fm).run(_make_args())
        fm.locate_snippets.assert_called_once_with(
            design_pattern=None, difficulty=None, llm=None, count=-1)
 
################################### CLI ARGS TESTS ###################################
 
class TestCLIExamples(unittest.TestCase):
    """
    Mirrors the example commands from the CLI
    """

    def _make_dpr(self, fm=None):
        """Mocked DPR, returns (dpr, workflow, report_gen)"""
        llm = _mock_llm()
        llm_factory = MagicMock(return_value=llm)
        workflow = MagicMock()
        workflow.execute.return_value = [_mock_result()]
        workflow_factory = MagicMock(return_value=workflow)
        report_gen = MagicMock()
        dpr = DPR(file_manager=fm or _mock_file_manager(files=[_mock_snippet()]),
                  llm_factory=llm_factory,
                  workflow_factory=workflow_factory,
                  report_generator_factory=MagicMock(return_value=report_gen))
        return dpr, llm_factory, workflow_factory, workflow, report_gen

    def test_llm_claude_all_snippets(self):
        """--llm claude :  all snippets, single-prompt, no filters"""
        # python pattern_recogniser.py --llm claude
        fm = _mock_file_manager(files=[_mock_snippet()])
        dpr, llm_factory, _, workflow, _ = self._make_dpr(fm)

        dpr.run(_make_args(llm="claude"))

        llm_factory.assert_called_once_with("claude")
        fm.locate_snippets.assert_called_once_with(
            design_pattern=None, difficulty=None, llm=None, count=-1)
        workflow.execute.assert_called_once()

    def test_openai_medium_factory_patterns(self):
        """--llm openai --filter-pattern Factory --filter-difficulty M"""
        fm = _mock_file_manager(files=[_mock_snippet()])
        dpr, llm_factory, _, _, _ = self._make_dpr(fm)

        dpr.run(_make_args(llm="openai", filter_pattern="Factory", filter_difficulty="M"))

        llm_factory.assert_called_once_with("openai")
        fm.locate_snippets.assert_called_once_with(
            design_pattern="Factory", difficulty="M", llm=None, count=-1)

    def test_claude_analysing_openai_generated_observer_hard_count5(self):
        """--llm claude --filter-llm openai --filter-pattern Observer --filter-difficulty H --count 5"""
        fm = _mock_file_manager(files=[_mock_snippet()])
        dpr, llm_factory, _, _, _ = self._make_dpr(fm)

        dpr.run(_make_args(llm="claude", filter_llm="openai",
                           filter_pattern="Observer", filter_difficulty="H", count=5))

        llm_factory.assert_called_once_with("claude")
        fm.locate_snippets.assert_called_once_with(
            design_pattern="Observer", difficulty="H", llm="openai", count=5)

    
    def test_claude_custom_input_file(self):
        """--llm claude --input my_code.py :  locate_custom_snippet, save_custom_results"""
        fm = _mock_file_manager(files=[_mock_snippet()])
        dpr, llm_factory, _, _, report_gen = self._make_dpr(fm)

        dpr.run(_make_args(llm="claude", input_path="Input/my_code.py"))

        llm_factory.assert_called_once_with("claude")
        fm.locate_snippets.assert_not_called()
        fm.locate_custom_snippet.assert_called_once_with("Input/my_code.py")
        report_gen.save_custom_results.assert_called_once()
        report_gen.save_results.assert_not_called()


if __name__ == "__main__":
    unittest.main()
 