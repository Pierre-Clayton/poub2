import math, random
from collections import Counter
mbti_question_map = {
    "Q1": ("E", "You find it takes effort to introduce yourself to other people."),
    "Q2": ("I", "You do not usually initiate conversations."),
    "Q3": ("I", "You often get so lost in thoughts that you ignore or forget your surroundings."),
    "Q4": ("E", "You are usually highly motivated and energetic."),
    "Q5": ("E", "You enjoy group activities more than solitary ones."),
    "Q6": ("I", "You feel drained after extensive social interaction."),
    "Q7": ("I", "You prefer deep conversations over small talk."),
    "Q8": ("E", "You find it easy to introduce yourself to strangers."),
    "Q9": ("E", "You feel energized by social interactions."),
    "Q10": ("I", "You prefer to reflect before speaking."),
    "Q11": ("S", "You rarely do something just out of sheer curiosity."),
    "Q12": ("N", "You are curious about many different things."),
    "Q13": ("S", "You often prefer facts over abstract ideas."),
    "Q14": ("N", "You enjoy discussing theoretical concepts more than practical applications."),
    "Q15": ("S", "You trust experience more than speculation."),
    "Q16": ("S", "You prefer concrete details over abstract concepts."),
    "Q17": ("N", "You enjoy daydreaming and imagining possibilities."),
    "Q18": ("N", "You rely more on instincts than on data."),
    "Q19": ("S", "You notice small details others overlook."),
    "Q20": ("N", "You find new ideas more exciting than following a routine."),
    "Q21": ("F", "Winning a debate matters less to you than making sure no one gets upset."),
    "Q22": ("T", "You feel superior to other people."),
    "Q23": ("T", "You tend to prioritize logic over emotions in decision-making."),
    "Q24": ("F", "You find it easy to empathize with others’ emotions."),
    "Q25": ("T", "You make decisions based on principles rather than feelings."),
    "Q26": ("T", "You value fairness over personal considerations."),
    "Q27": ("T", "You believe efficiency is more important than kindness."),
    "Q28": ("T", "You enjoy analyzing problems more than comforting others."),
    "Q29": ("F", "You find it difficult to make decisions based purely on logic."),
    "Q30": ("F", "You avoid conflict whenever possible."),
    "Q31": ("J", "Being organized is more important to you than being adaptable."),
    "Q32": ("J", "You try to respond to your emails as soon as possible and cannot stand a messy inbox."),
    "Q33": ("J", "You like to have a detailed plan before starting something new."),
    "Q34": ("P", "You prefer to keep your options open rather than stick to a strict plan."),
    "Q35": ("J", "You are more comfortable with schedules than spontaneity."),
    "Q36": ("J", "You prefer structure over flexibility in your daily routine."),
    "Q37": ("J", "You find deadlines helpful rather than stressful."),
    "Q38": ("J", "You make detailed to-do lists to stay productive."),
    "Q39": ("J", "You dislike last-minute changes to plans."),
    "Q40": ("P", "You enjoy spontaneous adventures more than careful planning.")
    }
    
def mbti_full():
    return [{"index": i,"question": q, "trait": trait, "reverse": False} for i,(s,(trait,q)) in enumerate(mbti_question_map.items())]   

def mbti_index(Q):
    qq = [{"index": i,"question": q, "trait": trait, "reverse": False} for i,(s,(trait,q)) in enumerate(mbti_question_map.items())]
    mbti_categories = dict(Counter([a['trait'] for a in qq]))
    selected_mbti_questions = []
    no_questions = int(''.join(filter(str.isdigit, Q)))
    remaining_slots = no_questions
    select_num_questions = math.ceil(no_questions/len(mbti_categories))

    for category,count in mbti_categories.items():
        tochoose = min([select_num_questions,abs(remaining_slots),count])
        questoselect = [a for a in qq if a['trait'] == category]
        selected_questions = random.sample(questoselect, tochoose)
        selected_mbti_questions.extend(selected_questions)
        remaining_slots -= tochoose

    return selected_mbti_questions