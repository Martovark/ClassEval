
import os
import json
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
ROOT_DIR = str(Path(ROOT_DIR) / "..")
DATA_DIR = str(Path(ROOT_DIR) / "data")  # This is the data of this project
OUTPUT_DIR = str(Path(ROOT_DIR) / "output")  # This is the output of this project
LOGS_DIR = str(Path(ROOT_DIR) / "log")


def load_json(path):
    with open(path, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    return data

def load_jsonl(path):
    data = []
    with open(path, "r", encoding="utf-8") as fp:
        for line in fp:
            data.append(json.loads(line))
    return data

def save_jsonl(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        for item in obj:
            f.write(json.dumps(item, ensure_ascii=False)+'\n')


class PathUtil:

    @staticmethod
    def orig_data_dir():
        path = Path(DATA_DIR)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    @staticmethod
    def model_output_data(filename: str, ext: str):
        path = Path(OUTPUT_DIR)/'model_output'
        path.mkdir(parents=True, exist_ok=True)
        path = path / f'{filename}.{ext}'
        return str(path)
    
    @staticmethod
    def log_output_data(filename: str, ext: str):
        path = Path(LOGS_DIR)
        path.mkdir(parents=True, exist_ok=True)
        path = path / f'{filename}.{ext}'
        return str(path)

    @staticmethod
    def test_result_data(filename: str, ext: str):
        path = Path(OUTPUT_DIR)/'result'
        path.mkdir(parents=True, exist_ok=True)
        path = path / f'{filename}.{ext}'
        return str(path)

    @staticmethod
    def eval_data(dataset_name: str):
        path = Path(DATA_DIR)/f'{dataset_name}.json'
        return str(path)

    @staticmethod
    def benchmark_code_data(filename: str, ext: str):
        path = Path(DATA_DIR)/'benchmark_solution_code'
        path.mkdir(parents=True, exist_ok=True)
        path = path / f'{filename}.{ext}'
        return str(path)

    @staticmethod
    def benchmark_code_file():
        path = Path(DATA_DIR) / 'benchmark_solution_code'
        return str(path)

    @staticmethod
    def benchmark_test_file():
        path = Path(DATA_DIR) / 'benchmark_test_code'
        return str(path)

    @staticmethod
    def benchmark_test_data(filename: str, ext: str):
        path = Path(DATA_DIR)/'benchmark_test_code'
        path.mkdir(parents=True, exist_ok=True)
        path = path / f'{filename}.{ext}'
        return str(path)
    
    @staticmethod
    def update_flags(class_eval_name: str):
        class_eval_jsonl_path = Path(OUTPUT_DIR) / "model_output" / f"{class_eval_name}.jsonl"
        results_path = Path(OUTPUT_DIR) / "result" / "detailed_result.json"
        
        results = load_json(results_path)
        class_eval = load_jsonl(class_eval_jsonl_path)
        
        dataset_name = list(results.keys())[0]
        results = results[dataset_name]
        
        idx = 0 
        for task_id, dct in results.items():
            for k, v in dct.items():
                if k == "TestClass":
                    class_success = v["class_success"]
            class_eval[idx]["matched"] = [class_success == 1]
            idx += 1
        
        save_jsonl(class_eval, class_eval_jsonl_path)
    
    @staticmethod
    def update_acc():
        all_metrics_path = Path(ROOT_DIR) / "dump" / "all_metrics.jsonl"
        results_path = Path(OUTPUT_DIR) / "result" / "pass_at_k_result.json"
        
        all_metrics = load_jsonl(all_metrics_path)
        results = load_json(results_path)
        results = results["pass_1_greedy"]
        
        dataset_name = list(results.keys())[0]
        results = results[dataset_name]
        
        for dataset in all_metrics:
            if dataset["dataset"] == dataset_name:
                if "accuracy@1" in dataset["metric"]:
                    _ = dataset["metric"].pop("accuracy@1")# ["accuracy@1"]
                dataset["metric"]["class_partial_success"] = results["class_partial_success"]
                dataset["metric"]["class_success"] = results["class_success"]
        
        save_jsonl(all_metrics, all_metrics_path)
        
        
        
        
            
            