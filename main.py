import solpha

for file in ["sources/nightingale.json","sources/keys.json"]:
    score=solpha.create_score(file)
    score.get_music_code()
    filename=score.produce()
    print('file saved at ' + filename)

