import cohere

co = cohere.Client('ArCSzp9peaChzIXMLkNILdyifB0JzifENzD5DSwb')

def generate(prompt: str, precede='In five sentences, answer this:') -> str:
    response = co.generate(
    model='command-xlarge-nightly',
    prompt= f'{precede} {prompt}',
    max_tokens=300,
    temperature=0,
    k=0,
    p=0.75,
    stop_sequences=[],
    return_likelihoods='NONE')
    return response.generations[0].text
print(generate(prompt="what is the most important things i should look out for on this general aviation flight with 10kts wind and clouds at 5500 meters. CAVOK is false that is not weather"))
print(generate(prompt='lester b pearson', precede='In 4 characters, awnser what is the ICAO code of'))