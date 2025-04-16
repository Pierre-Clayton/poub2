def bfi_index(Q):
    bfi_config = {
        'BFI-10': {
            'questions': [
                ("I see myself as someone who is reserved.", "Extraversion", True),
                ("I see myself as someone who is generally trusting.", "Agreeableness", False),
                ("I see myself as someone who tends to be lazy.", "Conscientiousness", True),
                ("I see myself as someone who is relaxed, handles stress well.", "Neuroticism", True),
                ("I see myself as someone who has few artistic interests.", "Openness", True),
                ("I see myself as someone who is outgoing, sociable.", "Extraversion", False),
                ("I see myself as someone who tends to find fault with others.", "Agreeableness", True),
                ("I see myself as someone who does a thorough job.", "Conscientiousness", False),
                ("I see myself as someone who gets nervous easily.", "Neuroticism", False),
                ("I see myself as someone who has an active imagination.", "Openness", False),
            ]
            },
        'BFI-20': {
            'questions': [
                ("I see myself as someone who is talkative.", "Extraversion", False),
                ("I see myself as someone who is reserved.", "Extraversion", True),
                ("I see myself as someone who is full of energy.", "Extraversion", False),
                ("I see myself as someone who generates a lot of enthusiasm.", "Extraversion", False),
                ("I see myself as someone who is helpful and unselfish with others.", "Agreeableness", False),
                ("I see myself as someone who starts quarrels with others.", "Agreeableness", True),
                ("I see myself as someone who has a forgiving nature.", "Agreeableness", False),
                ("I see myself as someone who is considerate and kind to almost everyone.", "Agreeableness", False),
                ("I see myself as someone who does a thorough job.", "Conscientiousness", False),
                ("I see myself as someone who tends to be lazy.", "Conscientiousness", True),
                ("I see myself as someone who is a reliable worker.", "Conscientiousness", False),
                ("I see myself as someone who does things efficiently.", "Conscientiousness", False),
                ("I see myself as someone who gets nervous easily.", "Neuroticism", False),
                ("I see myself as someone who is emotionally stable, not easily upset.", "Neuroticism", True),
                ("I see myself as someone who can be tense.", "Neuroticism", False),
                ("I see myself as someone who worries a lot.", "Neuroticism", False),
                ("I see myself as someone who has an active imagination.", "Openness", False),
                ("I see myself as someone who has few artistic interests.", "Openness", True),
                ("I see myself as someone who is original, comes up with new ideas.", "Openness", False),
                ("I see myself as someone who is curious about many different things.", "Openness", False)
            ]
        },
        'BFI-44': {
            'questions': [
                ("Is talkative", "Extraversion", False),
                ("Tends to find fault with others", "Agreeableness", True),
                ("Does a thorough job", "Conscientiousness", False),
                ("Is depressed, blue", "Neuroticism", False),
                ("Is original, comes up with new ideas", "Openness", False),
                ("Is reserved", "Extraversion", True),
                ("Is helpful and unselfish with others", "Agreeableness", False),
                ("Can be somewhat careless", "Conscientiousness", True),
                ("Is relaxed, handles stress well", "Neuroticism", True),
                ("Is curious about many different things", "Openness", False),
                ("Is full of energy", "Extraversion", False),
                ("Starts quarrels with others", "Agreeableness", True),
                ("Is a reliable worker", "Conscientiousness", False),
                ("Can be tense", "Neuroticism", False),
                ("Is ingenious, a deep thinker", "Openness", False),
                ("Generates a lot of enthusiasm", "Extraversion", False),
                ("Has a forgiving nature", "Agreeableness", False),
                ("Tends to be disorganized", "Conscientiousness", True),
                ("Worries a lot", "Neuroticism", False),
                ("Has an active imagination", "Openness", False),
                ("Tends to be quiet", "Extraversion", True),
                ("Is generally trusting", "Agreeableness", False),
                ("Tends to be lazy", "Conscientiousness", True),
                ("Is emotionally stable, not easily upset", "Neuroticism", True),
                ("Is inventive", "Openness", False),
                ("Has an assertive personality", "Extraversion", False),
                ("Can be cold and aloof", "Agreeableness", True),
                ("Perseveres until the task is finished", "Conscientiousness", False),
                ("Can be moody", "Neuroticism", False),
                ("Values artistic, aesthetic experiences", "Openness", False),
                ("Is sometimes shy, inhibited", "Extraversion", True),
                ("Is considerate and kind to almost everyone", "Agreeableness", False),
                ("Does things efficiently", "Conscientiousness", False),
                ("Remains calm in tense situations", "Neuroticism", True),
                ("Prefers work that is routine", "Openness", True),
                ("Is outgoing, sociable", "Extraversion", False),
                ("Is sometimes rude to others", "Agreeableness", True),
                ("Makes plans and follows through with them", "Conscientiousness", False),
                ("Gets nervous easily", "Neuroticism", False),
                ("Likes to reflect, play with ideas", "Openness", False),
                ("Has few artistic interests", "Openness", True),
                ("Likes to cooperate with others", "Agreeableness", False),
                ("Is easily distracted", "Conscientiousness", True),
                ("Is sophisticated in art, music, or literature", "Openness", False)
            ]
                
        }
        }
    qq = [{"index": i,"question": q, "trait": trait, "reverse": reverse} for i,(q,trait,reverse) in enumerate(bfi_config[Q]['questions'])]
    
    return qq