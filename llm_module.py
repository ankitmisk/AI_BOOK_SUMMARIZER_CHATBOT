print('Module Loaded ')


def predict_text(seed_text, next_words = 50):
    print('Predicte Func done')
    for i in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list],maxlen=max_len-1,padding='pre')
        predicted = np.argmax(model.predict(token_list,verbose = 0),axis = -1)[0]
        output_word = ''
        for word,index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text+= ' ' + output_word
    return seed_text


def summarize_text(text, mode = 'short',predict_text = predict_text):
    if mode == 'short':
        return predict_text(text,next_words=50).title()
    elif mode == 'bullet':
        generated = predict_text(text,next_words=50)
        words = generated.split()
        bullet_points = ' '
        for i in range(len(words)):
            if len(bullet_points)>=50:
                print(bullet_points.title())
                bullet_points = ' '
            else:
                bullet_points += ' ' + words[i]
    print('Summarize Func done12344')


