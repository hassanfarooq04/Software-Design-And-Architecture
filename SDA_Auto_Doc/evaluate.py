from rouge_score import rouge_scorer
import nltk
import json

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def calculate_bleu(reference, hypothesis):
    """
    Calculates BLEU score.
    """
    reference_tokens = nltk.word_tokenize(reference)
    hypothesis_tokens = nltk.word_tokenize(hypothesis)
    
    # BLEU-1, BLEU-2, BLEU-4
    score_1 = nltk.translate.bleu_score.sentence_bleu([reference_tokens], hypothesis_tokens, weights=(1, 0, 0, 0))
    score_4 = nltk.translate.bleu_score.sentence_bleu([reference_tokens], hypothesis_tokens, weights=(0.25, 0.25, 0.25, 0.25))
    
    return {"bleu_1": score_1, "bleu_4": score_4}

def calculate_rouge(reference, hypothesis):
    """
    Calculates ROUGE score.
    """
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    return {
        "rouge_1": scores['rouge1'].fmeasure,
        "rouge_2": scores['rouge2'].fmeasure,
        "rouge_L": scores['rougeL'].fmeasure
    }

if __name__ == "__main__":
    # Example evaluation
    ref = "Calculates the sum of two numbers."
    hyp = "This function returns the sum of a and b."
    
    bleu = calculate_bleu(ref, hyp)
    rouge = calculate_rouge(ref, hyp)
    
    print(f"Reference: {ref}")
    print(f"Hypothesis: {hyp}")
    print(f"BLEU Score: {bleu}")
    print(f"ROUGE Score: {rouge}")