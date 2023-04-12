import sys

def get_similarity_percentage(smaller_text, bigger_text, similarity_score, percentage):
    percentage
    is_the_highest = 0
    score=0
    bigger_text_string = " ".join(bigger_text)
    smaller_text_string = " ".join(smaller_text)
    for info in smaller_text:
        if info in bigger_text_string:
            score += 1

    print("score: " + str(score))
    if score > similarity_score:
        similarity_score = score;
        new_percentage = score/len(smaller_text) * 100
        if new_percentage > percentage:
            percentage = new_percentage   
            is_the_highest = 1
         
    print(new_percentage)    

    return {
        'percentage':percentage,
        'is_the_highest':is_the_highest
        }


