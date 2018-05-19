import pandas as pd
pd.options.display.max_columns = 200
pd.options.mode.chained_assignment = None
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
from string import punctuation
from collections import Counter
import re
import numpy as np
#from tqdm import tqdm_notebook
#tqdm_notebook().pandas()
from matplotlib import pyplot as plt
from functools import reduce
from sklearn.manifold import TSNE
from shutil import copyfile
from IPython.display import display, HTML
from datetime import datetime

#from bokeh.io import notebook_div

#!add keyword identifier for capitalized verbs
#!if one word is capped, check to see if next word is capped
#!^ will monitor proper nouns

#add thesaurus check to consolidate similar words
#track stop word in-betweens, not just after


def run_main():
    print('Running at', str(datetime.today()))

    #adjust if change directory info
    #copyfile('/home/shartrich/DataMining/data/news.csv', '/static/Project Files/news.csv')
    copyfile('/home/shartrich/DataMining/data/news.csv', 'static/Project Files/news.csv')

    #print('Running')

    def remove_non_ascii(string):
        string = string.replace("“", "'")
        string = string.replace("”", "'")
        #string = string.replace(":", "'")
        if string == '':
            return string
        return ''.join([i if ord(i) < 128 else ' ' for i in string])

    def _removeNonAscii(s):
        return "".join(i for i in s if ord(i)<128)

    def clean_text(text):
        text = text.lower() #see if necessary
        text = re.sub(r"what's", "what is ", text)
        text = text.replace('(ap)', '')
        text = re.sub(r"\'s", " is ", text)
        text = re.sub(r"\'ve", " have ", text)
        text = re.sub(r"can't", "cannot ", text)
        text = re.sub(r"n't", " not ", text)
        text = re.sub(r"i'm", "i am ", text)
        text = re.sub(r"\'re", " are ", text)
        text = re.sub(r"\'d", " would ", text)
        text = re.sub(r"\'ll", " will ", text)
        text = re.sub(r'\W+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r"\\", "", text)
        text = re.sub(r"\'", "", text)
        text = re.sub(r"\"", "", text)
        text = re.sub('[^a-zA-Z ?!]+', '', text)
        text = _removeNonAscii(text)
        text = text.strip()
        return text

    def tokenizer(text):
        text = clean_text(text)
        tokens = [word_tokenize(sent) for sent in sent_tokenize(text)]
        tokens = list(reduce(lambda x,y: x+y, tokens))
        tokens = list(filter(lambda token: token not in (stop_words + list(punctuation)) , tokens))
        return tokens

    def keywords(category):
        tokens = data[data['category'] == category]['tokens']
        alltokens = []
        for token_list in tokens:
            alltokens += token_list
        counter = Counter(alltokens)
        return counter.most_common(10)

    #data = pd.read_csv('static/Project Files/news.csv')
    data = pd.read_csv('/home/shartrich/mysite/static/Project Files/news.csv')
    data = data[~data['description'].isnull()]
    #data = data.fillna('')
    data = data.drop_duplicates('description')

    stop_words = []

    with open('static/Project Files/stopwords.txt', 'r') as f:
        for l in f.readlines():
            stop_words.append(l.replace('\n', ''))

        additional_stop_words = ['t', 'will']
        stop_words += additional_stop_words


    data = data[(data.description.map(len) > 140) & (data.description.map(len) <= 300)]
    data.reset_index(inplace=True, drop=True)

    #data['description'] = data['description'].map(lambda d: str(d.decode('utf-8')))
    #data['tokens'] = data['description'].progress_map(lambda d: tokenizer(d))
    data['tokens'] = data['description'].apply(lambda d: tokenizer(d))



    ##for descripition, tokens in zip(data['description'].head(5), data['tokens'].head(5)):
    ##    print('description:', descripition)
    ##    print('tokens:', tokens)
    ##    print()

    ##for category in set(data['category']):
    ##    print('category :', category)
    ##    print('top 10 keywords:', keywords(category))
    ##    print('---')



    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorizer = TfidfVectorizer(min_df=5, analyzer='word', ngram_range=(1, 2), stop_words='english')
    vz = vectorizer.fit_transform(list(data['tokens'].map(lambda tokens: ' '.join(tokens))))

    #print(vz.shape)


    tfidf = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))
    tfidf = pd.DataFrame(columns=['tfidf']).from_dict(dict(tfidf), orient='index')
    tfidf.columns = ['tfidf']

    #tfidf.tfidf.hist(bins=25, figsize=(15,7))

    #plt.show()

    # from wordcloud import WordCloud
    # def plot_word_cloud(terms):
    #     text = terms.index
    #     text = ' '.join(list(text))
    #     # lower max_font_size
    #     wordcloud = WordCloud(max_font_size=40).generate(text)
    #     plt.figure(figsize=(25, 25))
    #     plt.imshow(wordcloud, interpolation="bilinear")
    #     plt.axis("off")
    #     plt.show()

    #low impact generic words
    #plot_word_cloud(tfidf.sort_values(by=['tfidf'], ascending=True).head(40))
    #plt.show()

    #high impact words
    #plot_word_cloud(tfidf.sort_values(by=['tfidf'], ascending=False).head(40))
    #plt.show()


    from sklearn.decomposition import TruncatedSVD
    svd = TruncatedSVD(n_components=50, random_state=0)
    svd_tfidf = svd.fit_transform(vz)

    run = True
    if run:
    # run this (takes times)
        tsne_model = TSNE(n_components=2, verbose=1, random_state=0, n_iter=500)
        tsne_tfidf = tsne_model.fit_transform(svd_tfidf)
        #print(tsne_tfidf.shape)
        tsne_tfidf_df = pd.DataFrame(tsne_tfidf)
        tsne_tfidf_df.columns = ['x', 'y']
        tsne_tfidf_df['category'] = data['category']
        tsne_tfidf_df['description'] = data['description']
        tsne_tfidf_df.to_csv('static/Project Files/tsne_tfidf.csv', encoding='utf-8', index=False)
    else:
    # or import the dataset directly
        tsne_tfidf_df = pd.read_csv('static/Project Files/tsne_tfidf.csv')



    groups = tsne_tfidf_df.groupby('category')
    # fig, ax = plt.subplots(figsize=(15, 10))
    # ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
    # for name, group in groups:
    #     ax.plot(group.x, group.y, marker='o', linestyle='', label=name)
    # ax.legend()
    #plt.show()



    import bokeh.plotting as bp
    from bokeh.models import HoverTool, BoxSelectTool
    from bokeh.plotting import figure, show, output_notebook, reset_output
    from bokeh.palettes import d3
    import bokeh.models as bmo
    from bokeh.io import save, output_file


    output_notebook()
    plot_tfidf = bp.figure(plot_width=700, plot_height=600, title="tf-idf clustering of the news",
        tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
        x_axis_type=None, y_axis_type=None, min_border=1)

    palette = d3['Category10'][len(tsne_tfidf_df['category'].unique())]
    color_map = bmo.CategoricalColorMapper(factors=tsne_tfidf_df['category'].map(str).unique(), palette=palette)

    plot_tfidf.scatter(x='x', y='y', color={'field': 'category', 'transform': color_map},
                       legend='category', source=tsne_tfidf_df)
    hover = plot_tfidf.select(dict(type=HoverTool))
    hover.tooltips={"description": "@description", "category":"@category"}

    #display(HTML('<div style="margin:auto">'+div+'</div>'))
    #output_file("test1.html")
    #show(plot_tfidf)


    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from sklearn.cluster import MiniBatchKMeans, KMeans
    from sklearn.metrics import silhouette_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import Normalizer


    distorsions = []
    sil_scores = []
    k_max = 40
    for k in range(2, k_max):
        kmeans_model = MiniBatchKMeans(n_clusters=k, init='k-means++', n_init=1, random_state=42,
                             init_size=1000, verbose=False, max_iter=1000)
        kmeans_model.fit(vz)
        sil_score = silhouette_score(vz, kmeans_model.labels_)
        sil_scores.append(sil_score)
        distorsions.append(kmeans_model.inertia_)



    # f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(15, 10))

    # ax1.plot(range(2, k_max), distorsions)
    # ax1.set_title('Distorsion vs num of clusters')
    # ax1.grid(True)

    # ax2.plot(range(2, k_max), sil_scores)
    # ax2.set_title('Silhouette score vs num of clusters')
    # ax2.grid(True)

    num_clusters = 40
    kmeans_model = MiniBatchKMeans(n_clusters=num_clusters, init='k-means++', n_init=1, random_state=42,
                             init_size=1000, batch_size=1000, verbose=False, max_iter=1000, )
    kmeans = kmeans_model.fit(vz)
    kmeans_clusters = kmeans.predict(vz)
    kmeans_distances = kmeans.transform(vz)

    ##for (i, desc),category in zip(enumerate(data.description),data['category']):
    ##    if(i < 5):
    ##        print("Cluster " + str(kmeans_clusters[i]) + ": " + desc +
    ##              "(distance: " + str(kmeans_distances[i][kmeans_clusters[i]]) + ")")
    ##        print('category: ',category)
    ##        print('---')


    sorted_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    all_keywords = []
    for i in range(num_clusters):
        topic_keywords = []
        for j in sorted_centroids[i, :10]:
            topic_keywords.append(terms[j])
        all_keywords.append(topic_keywords)

    keywords_df = pd.DataFrame(index=['topic_{0}'.format(i) for i in range(num_clusters)],
                               columns=['keyword_{0}'.format(i) for i in range(10)],
                               data=all_keywords)


    #print(keywords_df)



    run = True
    if run:
        #tsne_model = TSNE(n_components=2, verbose=1, random_state=0, n_iter=500)
        tsne_model = TSNE(n_components=2, verbose=1, random_state=0, n_iter=500)
        tsne_kmeans = tsne_model.fit_transform(kmeans_distances)
        kmeans_df = pd.DataFrame(tsne_kmeans, columns=['x', 'y'])
        kmeans_df['cluster'] = kmeans_clusters
        kmeans_df['cluster'] = kmeans_df['cluster'].map(str)
        kmeans_df['description'] = data['description']
        kmeans_df['category'] = data['category']
        kmeans_df.to_csv('static/Project Files/tsne_kmeans.csv', index=False, encoding='utf-8')
    else:
        kmeans_df = pd.read_csv('static/Project Files/tsne_kmeans.csv')
        kmeans_df['cluster'] = kmeans_df['cluster'].map(str)

    reset_output()
    output_notebook()
    plot_kmeans = bp.figure(plot_width=700, plot_height=600, title="KMeans clustering of the news",
        tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
        x_axis_type=None, y_axis_type=None, min_border=1)

    palette = d3['Category20'][20] + d3['Category20b'][20]
    color_map = bmo.CategoricalColorMapper(factors=kmeans_df['cluster'].unique(), palette=palette)

    plot_kmeans.scatter('x', 'y', source=kmeans_df,
                        color={'field': 'cluster', 'transform': color_map},
                        legend='cluster')
    hover = plot_kmeans.select(dict(type=HoverTool))
    hover.tooltips={"description": "@description", "cluster": "@cluster", "category": "@category"}


    #display(HTML('<div style="margin:auto">'+div+'</div>'))
    output_file("static/Project Files/test2.html")
    show(plot_kmeans)
    

    copyfile('/home/shartrich/mysite/templates/bokeh plot.html', '/home/shartrich/mysite/static/Project Files/test2.html')



    #for idx, word in enumerate(data.description):
    #   print(idx, remove_non_ascii(word))

if __name__ == '__main__':
    run_main()



