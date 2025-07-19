import openai
import os
import logging

class Llama3Client:
    def __init__(self, config):
        self.api_base = config['llm']['endpoint']
        self.model = config['llm']['model']
        self.prompt_template = config['llm']['log_analysis_prompt']
        openai.api_key = "lm-studio"  # Dummy key for LM Studio
        openai.api_base = self.api_base
        # Setup LLM log file
        os.makedirs('logs', exist_ok=True)
        self.llm_logger = logging.getLogger("llm_analysis")
        handler = logging.FileHandler("logs/llm_analysis.log", encoding="utf-8")
        handler.setFormatter(logging.Formatter('%(asctime)s | %(message)s'))
        if not self.llm_logger.handlers:
            self.llm_logger.addHandler(handler)
        self.llm_logger.setLevel(logging.INFO)

    def log_llm_result(self, job_id, log_text, llm_response):
        self.llm_logger.info(f"{job_id} | {log_text} | {llm_response}")

    def analyze_log(self, log_text, job_id=None):
        prompt = f"{self.prompt_template}\n{log_text}"
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            llm_response = response['choices'][0]['message']['content']
            if job_id:
                self.log_llm_result(job_id, log_text, llm_response)
            return llm_response
        except Exception as e:
            err_msg = f"[LLM Error] {e}"
            if job_id:
                self.log_llm_result(job_id, log_text, err_msg)
            return err_msg 