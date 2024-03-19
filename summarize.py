def build_final_context(chunks):
    context = ""
    for index, chunk in enumerate(chunks):
        context +=  f"Context {index + 1}: " + chunk + "\n"
    return context

class Prompts:

    @staticmethod
    def summarize_prompt(context):
        return f"""
        Sau đây là một nội dung được trích xuất của một văn bản, nhiệm vụ của bạn là hãy tóm tắt nó
        ---CONTEXT---
        {context}
        ---END CONTEXT---
        Hãy đưa ra tóm tắt của văn bản trên. Tôi chỉ cần phần tóm tắt, và không cần thêm bất kì thứ gì khác.
        Tóm Tắt:
        """

    @staticmethod
    def final_ans_prompt(context):
        return f"""
        Dưới đây là các đoạn tóm tắt của từng đoạn nhỏ của một văn bản lớn.
        ---CONTEXT---
        {context}
        ---END CONTEXT---
        Dựa trên các đoạn trên, hãy đưa ra tóm tắt tổng của tất cả các đoạn trên. Tôi chỉ cần tóm tắt tổng, không cần thêm bất kì thứ gì khác.
        Tóm tắt tổng:
        """
    

def summarize_chunk(chunk, results_queue, llm):
    message = [{"role": "user", "content": Prompts.summarize_prompt(chunk)}]
    response = llm.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=message,
        temperature=0.1,
        max_tokens=4096
    )
    summarized_chunk = response.choices[0].message.content
    results_queue.put(summarized_chunk) 