def enrich_prompt_with_feedback(prompt, feedback_list):
    if not feedback_list:
        return prompt
    feedback_str = "\n".join([
        f"Previous action: {f['action']}, Feedback: {f['feedback']}, Comment: {f.get('comment','')}" for f in feedback_list
    ])
    return f"{prompt}\n\nFeedback history for similar events:\n{feedback_str}\n" 