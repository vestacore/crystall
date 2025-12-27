
from exec_prompt import exec_prompt
from units.learn_facts.models import LearnFactsResponse, LearnedFact

async def learn_facts(intent: str)->list[LearnedFact]:
    
    response = await exec_prompt(
            prompt_name = "learn_facts/prompt",
            intent = "Analyze request and extract direct or indirect facts from it",
            response_model = LearnFactsResponse,
            request = intent
        )
    
    return response.learned_facts
